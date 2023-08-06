import os

import GPy
import numpy as np

from pathlib import Path

from scipy.spatial.distance import euclidean

from boss.bo.acq.explore import explore
from boss.bo.hmc import HMCwrapper
from boss.bo.initmanager import InitManager
from boss.bo.kernel_factory import KernelFactory
from boss.bo.model import Model
from boss.bo.rstmanager import RstManager
from boss.io.main_output import MainOutput
import boss.io.parse as parse
from boss.settings import Settings, standardize_signature
from boss.utils.minimization import Minimization
from boss.utils.timer import Timer
from boss.bo.results import BOResults
import boss.keywords as bkw


class BOMain:
    """
    Class for handling Bayesian Optimization
    """

    def __init__(self, f, bounds, **keywords):
        keywords["bounds"] = bounds
        settings = Settings(keywords, f=f)
        self.settings = settings
        self.rst_manager = None
        self._setup()

    @classmethod
    def from_file(cls, ipfile, f=None, **new_keywords):
        """Initialize BOMain from a BOSS input or rst file.

        Parameters
        ----------
        ipfile : path_like
            The input file to initialize from, can be either a boss input or rst file.
        **new_keywords
            Any new BOSS keywords.
        """
        self = cls.__new__(cls)
        input_data = parse.parse_input_file(ipfile)
        rst_data = input_data.get("rst_data", np.array([]))
        keywords = input_data.get("keywords", {})
        keywords.update(new_keywords)
        self.settings = Settings(keywords, f=f)
        self.rst_manager = RstManager(self.settings, rst_data)
        cls._setup(self)
        return self

    @classmethod
    def from_settings(cls, settings, rst_data=None):
        """Construction from a Settings object. """
        self = cls.__new__(cls)
        self.settings = settings
        self.rst_manager = RstManager(self.settings, rst_data)
        cls._setup(self)
        return self

    def _setup(self):
        """Common setup for all factory methods. """
        settings = self.settings
        self.main_output = MainOutput(settings)
        if not self.rst_manager:
            self.rst_manager = RstManager(settings)

        self.init_manager = InitManager(
            settings["inittype"], settings["bounds"], settings["initpts"]
        )

        self.dim = settings.dim
        self.initpts = settings["initpts"]
        self.iterpts = settings["iterpts"]
        self.updatefreq = settings["updatefreq"]
        self.initupdate = settings["initupdate"]
        self.updateoffset = settings["updateoffset"]
        self.updaterestarts = settings["updaterestarts"]
        self.hmciters = settings["hmciters"]
        self.cores = settings["cores"]
        self.f = settings.f
        self.periods = settings["periods"]
        self.bounds = settings["bounds"]
        self.acqfn = settings.acqfn
        self.acqfnpars = settings["acqfnpars"]
        self.acqtol = settings["acqtol"]
        self.min_dist_acqs = settings["min_dist_acqs"]
        self.minzacc = settings["minzacc"]
        self.kerntype = settings["kernel"]
        self.noise = settings["noise"]
        self.timer = Timer()
        self.dir = settings.dir
        self.gm_tol = settings["gm_tol"]

        self.kernel = KernelFactory.construct_kernel(settings)
        self.model = None
        self.initX = np.array([]).reshape(0, self.dim)
        self.initY = np.array([]).reshape(0, 1)
        self.convergence = np.array([]).reshape(0, 5)
        self.normmean = 0
        self.normsd = 1
        self.est_yrange = 0
        self.hmcsample = []

        self.unfixed_model_params = np.array([]).reshape(0, self.dim + 1)
        self.exit_ok = False  # successful exit from main loop

    def get_x(self):
        """
        Returns the points where the objective function has been evaluated,
        in order of acquisition.
        """
        if self.model == None:
            return self.initX
        else:
            return self.model.X

    def get_y(self):
        """
        Returns the evaluated values of the objective function, in order of
        acquisition. This method should always be called instead of
        BOMain.model.Y for any use outside of the BOMain class.
        """
        if self.model == None:
            return self.initY
        else:
            return self.model.Y * self.normsd + self.normmean

    def get_mu(self, x):
        """
        Returns the model prediction at point x. This method should always be
        called instead of BOMain.model.mu for any use outside of the BOMain
        class.
        """
        if self.model == None:
            return None
        else:
            return self.model.mu(x) * self.normsd + self.normmean

    def get_nu(self, x):
        """
        Returns the variance of the model prediction at point x, with added
        noise (model variance).
        """
        if self.model == None:
            return None
        else:
            return self.model.nu(x) * self.normsd

    def get_grad(self, x):
        """
        Returns the predictive gradients. If the implemented mean shift is
        a constant, should just wrap self.model.predictive_gradients.
        """
        g = self.model.predictive_gradients(x)
        return np.array([g[0] * self.normsd, None])

    def _add_xy(self, xnew, ynew):
        """
        Internal functionality for saving a new acquisition (x, y), accounting
        for model mean shift. Initializes the GP model when the number of
        acquisitions meets the pre-specified number of initialization points.
        """
        if self.model == None:
            self.initX = np.vstack([self.initX, xnew])
            self.initY = np.vstack([self.initY, ynew])
            if self.get_x().shape[0] == self.initpts:
                self._init_model()
        else:
            X = np.vstack([self.get_x(), np.atleast_2d(xnew)])
            Y = np.vstack([self.get_y(), ynew])
            self.normmean = np.mean(Y)
            # if self.settings['ynorm']:
            #     self.normsd = np.std(Y)  # NORMALIZATION
            self.normsd = 1.0
            self.est_yrange = np.max(Y) - np.min(Y)
            self.model.redefine_data(X, (Y - self.normmean) / self.normsd)

    def add_xy_list(self, xnew, ynew):
        """
        Saves multiple acquisitions, accounting for model mean shift.
        Initializes the GP model when the number of acquisitions meets the
        pre-specified number of initialization points.
        """
        for i in range(xnew.shape[0]):
            self._add_xy(xnew[i, :], ynew[i])

    def _init_model(self):
        """
        Initializes the GP model. This should be called when all initialization
        points have been evaluated. Further acquisition locations can then be
        queried by optimizing an acquisition function.
        """
        self.normmean = np.mean(self.initY)
        # if self.settings['ynorm']:
        #     self.normsd = np.std(self.initY)  # NORMALIZATION
        self.normsd = 1.0
        self.est_yrange = np.max(self.initY) - np.min(self.initY)
        self.model = Model(
            self.initX,
            (self.initY - self.normmean) / self.normsd,
            self.bounds,
            self.min_dist_acqs,
            self.minzacc,
            self.kerntype,
            self.kernel,
            self.dim,
            self.noise,
        )

    def _should_optimize(self, i_iter):
        """
        Returns True if the model should be optimized at iteration i.
        """
        bo_i = np.max([0, i_iter + 1 - self.initpts])  # == 0 means initial iters

        # No model -> no optimization
        if self.model == None:
            return False

        # Check if initialization has just completed and we want to optimize
        elif bo_i == 0:
            if self.initupdate:
                return True
            else:
                return False

        # Check if optimization threshold and interval have passed
        elif bo_i >= self.updateoffset and bo_i % self.updatefreq == 0:
            return True

        # Otherwise there is no need to optimize
        else:
            return False

    def run(self):
        """
        The Bayesian optimization main loop. Evaluates first the initialization
        points, then creates a GP model and uses it and an acquisition function
        to locate the next points where to evaluate. Stops when a pre-specified
        number of initialization points and BO points have been acquired or a
        convergence criterion is met.

        Returns
        -------
        BOResults
            An object that provides convenient access to the most
            important results from the optimization.
        """
        self.main_output.new_file()
        self.rst_manager.new_file()

        initpts = self.settings["initpts"]
        iterpts = self.settings["iterpts"]
        minfreq = self.settings["minfreq"]

        totalpts = initpts + iterpts

        xnext = self._get_xnext(0)

        # BO main loop
        for i_iter in range(totalpts):

            self.main_output.iteration_start(i_iter + 1)
            self.timer.startLap()

            # Evaluation
            xnew, ynew = self._evaluate(i_iter, xnext)

            # Store new data and refit model.
            #  - Create the model when all initial data has been acquired.
            for i in range(len(ynew)):
                self._add_xy(xnew[i], ynew[i])
                self.rst_manager.new_data(xnew[i], ynew[i])

            # Optimize model if needed.
            if self._should_optimize(i_iter):
                self._optimize_model(i_iter)

            # Find next acquisition point.
            xnext = self._get_xnext(i_iter + 1)

            # Add model parameters to rst-file.
            if self.model != None:
                mod_unfixed_par = self.model.get_unfixed_params()
                self.rst_manager.new_model_params(mod_unfixed_par)

                # Also store model parameters directly on BOMain
                self.unfixed_model_params = np.vstack(
                    (self.unfixed_model_params, mod_unfixed_par)
                )
            else:
                mod_unfixed_par = None

            # Convergence diagnostics, calculate iteration specific info
            iconv = i_iter - initpts + 1
            write_conv = iconv >= 0 and (
                iconv == iterpts or (minfreq > 0 and (iconv % minfreq == 0))
            )
            if write_conv:
                self._add_convergence()

            # Output to boss outfile
            # Print a summary of important iteration data
            self.main_output.iteration_summary(
                i_iter,
                self.get_y().size,
                xnew,
                ynew,
                self.convergence,
                xnext,
                self.est_yrange,
                mod_unfixed_par,
                self.timer,
            )

            # Stopping criterion: convergence
            if self._has_converged(i_iter):
                self.main_output.convergence_stop()
                break

        # If we get here, the optimization finished successfully.
        self.exit_ok = True
        res = self.get_results()
        return res

    def resume(self, iterpts):
        """Resumes an optimization.

        If the BOMain object still exists and has an initialized model,
        this method will continue where the previous optimization left off
        for a given number of new iterations. Existing out and rst files will
        be updated with data form the new iterations, but changes done to the settings upon
        resuming will not be reflected in the beginning of these files.

        Parameters
        ----------
        iterpts : int
            The number of iterations for the resumed optimization.
            This includes the number of iterations from the previous run,
            thus if you first ran for 10 iterations and now want 10 more,
            you should set iterpts=20.

        Returns
        -------
        BOResults
            A dict-like object that provides convenient access to the most
            important results from the optimization.
        """
        i_curr = self.model.X.shape[0]
        totalpts = iterpts + self.settings["initpts"]
        minfreq = self.settings["minfreq"]
        self.settings["iterpts"] = iterpts

        for i_iter in range(i_curr + 1, totalpts + 1):

            self.main_output.iteration_start(i_iter)
            self.timer.startLap()

            # Acquisition
            xnext, acqfn = self._acqnext(i_iter)

            # Evaluation
            xnew, ynew = self._evaluate_xnew(xnext)

            # Store new data and refit model.
            #  - Create the model when all initial data has been acquired.
            for i in range(len(ynew)):
                self._add_xy(xnew[i], ynew[i])
                self.rst_manager.new_data(xnew[i], ynew[i])

            # Optimize model if needed.
            if self._should_optimize(i_iter):
                self._optimize_model(i_iter)

            # Add model parameters to rst-file.
            if self.model != None:
                mod_unfixed_par = self.model.get_unfixed_params()
                self.rst_manager.new_model_params(mod_unfixed_par)

                # Also store model parameters directly on BOMain
                self.unfixed_model_params = np.vstack(
                    (self.unfixed_model_params, mod_unfixed_par)
                )
            else:
                mod_unfixed_par = None

            # Convergence diagnostics, calculate iteration specific info
            if (minfreq > 0 and i_iter % minfreq == 0) or i_iter == totalpts:
                self._add_convergence()

            # Output to boss outfile
            # Print a summary of important iteration data
            self.main_output.iteration_summary(
                i_iter,
                self.get_y().size,
                xnew,
                ynew,
                self.convergence,
                xnext,
                self.est_yrange,
                mod_unfixed_par,
                self.timer,
            )

            # Stopping criterion: convergence
            if self._has_converged(i_iter):
                self.main_output.convergence_stop()
                break

        # If we get here, the optimization finished successfully.
        self.exit_ok = True
        res = self.get_results()
        return res

    def get_results(self):
        return BOResults(self)

    def _has_converged(self, i_iter):
        """
        Checks whether dxhat has been within tolerance for long enough
        TODO: should use dxmuhat instead?
        """
        if self.gm_tol is not None:
            conv_tol, conv_it = self.gm_tol
            if i_iter > self.initpts + conv_it:
                curr_xhat = self.convergence[-1, -3]
                within_tol = True
                for test_i in range(2, conv_it - 1):
                    if euclidean(self.convergence[-test_i, -3], curr_xhat) > conv_tol:
                        within_tol = False
                return within_tol
        return False

    def _get_xnext(self, i_iter):
        """
        Get a new point to evaluate by either reading it from the rst-file or,
        in case it doesn't contain the next point to evaluate, by obtaining
        a new initial point (when run is in initialization stage) or
        minimizing the acquisition function (when the run is in BO stage).
        """
        xnext = self.rst_manager.get_x(i_iter)
        if np.any(xnext == None):
            if i_iter < self.initpts:
                xnext = self.init_manager.get_x(i_iter)
            else:
                xnext, acqfn = self._acqnext(i_iter)
        return xnext

    def _acqnext(self, i_iter):
        """
        Selects the acquisition function to use and returns its xnext location
        as well as the used acquisition function.
        """
        if self.hmciters == 0:
            acqfn = self.acqfn
            expfn = explore
        else:
            hmc = HMCwrapper(self.hmcsample)
            acqfn = hmc.averageacq(self.acqfn, self.cores)
            expfn = hmc.averageacq(explore, self.cores)

        xnext = self._minimize_acqfn(acqfn)

        # check if xnext indicates we should trigger pure exploration
        if self._location_overconfident(xnext):
            xnext = self._minimize_acqfn(expfn)
            return xnext, expfn
        else:
            return xnext, acqfn

    def _minimize_acqfn(self, acqfn):
        """
        Minimizes the acquisition function to find the next
        sampling location 'xnext'.
        """

        nof_stdp = len(np.where(np.array(self.kerntype) == "stdp")[0])

        # Calculate the number of local minimizers to start. This has two
        # steps:

        # 1. Estimate the number of local minima in the surrogate model.
        # For the ith dimension, the number of local minima along a slice
        # is approximately n(i) = boundlength(i)/(2*lengthscale(i)). Note
        # that periodic kernels operate on normalised distances: distance
        # between inputs that are period(i)/2 apart is 1. To get the total
        # number of minima for all of the search space, multiply together
        # n(i) over all i.
        lengthscale_numpts = 1
        for i in range(self.dim):
            lengthscale = self.model.get_unfixed_params()[i + 1]
            if self.kerntype[i] == "stdp":
                bound_distance = 1
            else:
                bound_distance = self.periods[i] / 2
            lengthscale_numpts *= max(1, bound_distance / lengthscale)

        # 2. Increase the estimate to approximate the number of local
        # minima in the acquisition function. Here we assume that the
        # increase is proportional to the estimated number of local minima
        # per dimension.
        minima_multiplier = 1.7
        lengthscale_numpts = (minima_multiplier ** self.dim) * lengthscale_numpts

        num_pts = min(len(self.model.X), int(lengthscale_numpts))

        # minimize acqfn to obtain sampling location
        gmin = Minimization.minimize_from_random(
            acqfn,
            self.bounds,
            num_pts=num_pts,
            shift=0.1 * np.array(self.periods),
            args=[self.model, self.acqfnpars],
        )
        return np.atleast_1d(np.array(gmin[0]))

    def _location_overconfident(self, xnext):
        """
        Checks is model variance is lower than tolerance at suggested xnext.
        """
        if self.acqtol is None:
            return False
        else:
            if self.model.nu(xnext) >= self.acqtol:
                return False
            else:
                self.main_output.progress_msg(
                    "Acquisition location " + "too confident, doing pure exploration", 1
                )
                return True

    def _evaluate(self, i_iter, xnext):
        """
        Get a new evaluation either from the rst-file or, in case it doesn't
        contain the corresponding evaluation, by evaluating the user function
        """
        ynew = self.rst_manager.get_y(i_iter)
        if np.any(ynew == None):
            return self._evaluate_xnew(xnext)
        else:
            return np.atleast_2d(xnext), np.atleast_1d(ynew)

    def _evaluate_xnew(self, xnew):
        """
        Evaluates user function at given location 'xnew'
        to get the observation scalar 'ynew'.
        Later also gradient 'ydnew' should be made possible.
        """
        # run user script to evaluate sample
        self.main_output.progress_msg(
            "Evaluating objective function at x ="
            + self.main_output.utils.oneDarray_line(xnew.flatten(), self.dim, float),
            1,
        )

        local_timer = Timer()
        xnew = np.atleast_2d(xnew)  # X-data expected to be 2d-array
        ynew = np.atleast_1d(self.f(xnew))  # call the user function
        # os.chdir(self.dir)  # in case the user function changed the dir
        self.main_output.progress_msg(
            "Objective function evaluated,"
            + " time [s] %s" % (local_timer.str_lapTime()),
            1,
        )

        # return new data
        for i in range(len(xnew) - 1):
            ynew = np.insert(ynew, -1, ynew[0])

        return xnew, ynew

    def _optimize_model(self, i_iter):
        """
        Optimize the GP model or, if the next hyperparameters are contained in
        the rst-file, just use them.
        """
        if self.hmciters > 0:
            hmc = GPy.inference.mcmc.HMC(self.model)
            burnin = hmc.sample(int(self.hmciters * 0.33))
            self.hmcsample = hmc.sample(self.hmciters)

        n = self.model.get_unfixed_params().size
        theta = self.rst_manager.get_theta(i_iter, n)
        if np.any(theta == None):
            self.model.optimize_controlrstr(self.updaterestarts)
        else:
            self.model.set_unfixed_params(theta)
            # This is required for the model to properly update.
            self.model.redefine_data(self.model.X, self.model.Y)

    def _add_convergence(self):
        """
        Updates self.convergence with a new row containing
        bestx, besty, xhat, muhat, nuhat (in this order).
        """
        # if self.model == None:
        #     conv = np.atleast_2d(np.repeat(np.nan, 5))
        # else:
        bestx, besty = self.model.get_bestxy()
        xhat, muhat, nuhat = self.model.min_prediction()
        besty = besty * self.normsd + self.normmean
        muhat = muhat * self.normsd + self.normmean
        conv = np.atleast_2d([bestx, besty, xhat, muhat, nuhat])
        self.convergence = np.vstack((self.convergence, conv))
