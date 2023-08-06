"""
Functionality to output raw data on request to files outside of the main
output (*.out) file and the restart (*.rst) file.
"""
import numpy as np
import os

import boss.io.ioutils as ioutils
from boss.keywords import stringify


def dump_input_file(new_file_path, keywords, results_header=False):
    with open(new_file_path, "w") as fd:
        for key in sorted(keywords):
            val_str = stringify(keywords[key])
            fd.write(f"{key} {val_str}\n")
        if results_header:
            fd.write("\nRESULTS:")


def dump_model(settings, dest_file, bo, mod_params, xhat):
    """
    Outputs model slice (up to 2D) mean and variance in a grid to
    models/it#.dat
    """
    model_data = np.array([[]] * (settings.dim + 2))  # coords + mu + nu
    npts = settings["pp_model_slice"][2]
    coords = np.array(
        [
            np.linspace(settings["bounds"][i, 0], settings["bounds"][i, 1], npts)
            for i in settings["pp_model_slice"][:2]
        ]
    )
    defaults = (
        xhat if settings["pp_var_defaults"] is None else settings["pp_var_defaults"]
    )
    if settings["pp_model_slice"][0] != settings["pp_model_slice"][1]:
        # 2D slice
        x1, x2 = np.meshgrid(coords[0], coords[1])
        for i in range(npts):
            for j in range(npts):
                p = np.array([x1[i, j], x2[i, j]])
                for d in range(settings.dim):
                    if d not in settings["pp_model_slice"][:2]:
                        p = np.insert(p, d, defaults[d])
                p = np.insert(p, len(p), float(bo.get_mu(p)))
                p = np.insert(p, len(p), float(bo.get_nu(p)))
                model_data = np.insert(model_data, len(model_data[0]), p, axis=1)
        titleLine = "# Model output (x mu nu)" + ", grid of %ix%i=%i pts" % (
            npts,
            npts,
            npts ** 2,
        )
    else:
        # 1D slice
        x1 = coords[0]
        for i in range(npts):
            p = np.array([x1[i]])
            for d in range(settings.dim):
                if d not in settings["pp_model_slice"][:2]:
                    p = np.insert(p, d, defaults[d])
            p = np.insert(p, len(p), float(bo.get_mu(p)))
            p = np.insert(p, len(p), float(bo.get_nu(p)))
            model_data = np.insert(model_data, len(model_data[0]), p, axis=1)
        titleLine = "# Model output (x mu nu)" + ", grid of %i pts" % (npts)

    titleLine += (
        "\n# Model parameter values (noise variance lengthscales "
        + "[periods]): "
        + str(mod_params)
    )
    ioutils.write_cols(dest_file, model_data, "    ", titleLine, "%18.8E")


def dump_acqfn(settings, dest_file, bo, acqfn, defs):
    """
    Outputs acquisition function slice (up to 2D) in a grid to
    acqfns/it#.dat
    """
    acqf_data = [[]] * (settings.dim + 1)  # coords + acqf
    npts = settings["pp_model_slice"][2]
    coords = np.array(
        [
            np.linspace(settings["bounds"][i, 0], settings["bounds"][i, 1], npts)
            for i in settings["pp_model_slice"][:2]
        ]
    )
    defaults = (
        defs if settings["pp_var_defaults"] is None else settings["pp_var_defaults"]
    )
    if settings["pp_model_slice"][0] != settings["pp_model_slice"][1]:
        # 2D slice
        x1, x2 = np.meshgrid(coords[0], coords[1])
        for i in range(npts):
            for j in range(npts):
                p = np.array([x1[i, j], x2[i, j]])
                for d in range(settings.dim):
                    if d not in settings["pp_model_slice"][:2]:
                        p = np.insert(p, d, defaults[d])
                af, daf = acqfn(p, bo.model, bo.acqfnpars)
                p = np.insert(p, len(p), float(af))
                acqf_data = np.insert(acqf_data, len(acqf_data[0]), p, axis=1)
        titleLine = "# Acquisition function  (x" + " af), grid of %i pts" % (npts ** 2)
    else:
        # 1D slice
        x1 = coords[0]
        for i in range(npts):
            p = np.array([x1[i]])
            for d in range(settings.dim):
                if d not in settings["pp_model_slice"][:2]:
                    p = np.insert(p, d, defaults[d])
            af, daf = acqfn(p, bo.model, bo.acqfnpars)
            p = np.insert(p, len(p), float(af))
            acqf_data = np.insert(acqf_data, len(acqf_data[0]), p, axis=1)
        titleLine = "# Acquisition function (x" + " af), grid of %i pts" % (npts)

    ioutils.write_cols(dest_file, acqf_data, "    ", titleLine, "%18.8E")


def dump_truef(settings, dest_file, last_xhat):
    """
    Outputs true function slice (up to 2D) in a grid
    """
    truef_data = [[]] * (settings.dim + 1)  # coords + truef
    npts = settings["pp_truef_npts"]
    coords = np.array(
        [
            np.linspace(settings["bounds"][i, 0], settings["bounds"][i, 1], npts)
            for i in settings["pp_model_slice"][:2]
        ]
    )
    defaults = (
        last_xhat
        if settings["pp_var_defaults"] is None
        else settings["pp_var_defaults"]
    )
    if settings["pp_model_slice"][0] != settings["pp_model_slice"][1]:
        # 2D slice
        x1, x2 = np.meshgrid(coords[0], coords[1])
        for i in range(npts):
            for j in range(npts):
                p = np.array([x1[i, j], x2[i, j]])
                for d in range(settings.dim):
                    if d not in settings["pp_model_slice"][:2]:
                        p = np.insert(p, d, defaults[d])
                tf = settings.f(np.atleast_2d(p))
                os.chdir(settings.dir)
                p = np.insert(p, len(p), float(tf))
                truef_data = np.insert(truef_data, len(truef_data[0]), p, axis=1)
        titleLine = "# True function output (x" + " f), grid of %ix%i=%i pts" % (
            npts,
            npts,
            npts ** 2,
        )
    else:
        # 1D slice
        x1 = coords[0]
        for i in range(npts):
            p = np.array([x1[i]])
            for d in range(settings.dim):
                if d not in settings["pp_model_slice"][:2]:
                    p = np.insert(p, d, defaults[d])
            tf = settings.f(np.atleast_2d(p))
            os.chdir(settings.dir)
            p = np.insert(p, len(p), float(tf))
            truef_data = np.insert(truef_data, len(truef_data[0]), p, axis=1)
        titleLine = "# True function output (x" + " f), grid of %i pts" % (npts)

    ioutils.write_cols(dest_file, truef_data, "    ", titleLine, "%18.8E")


def dump_mep(path):
    """
    Outputs the coordinates of each minimum energy path into files
    """
    crds = path.crds
    i = path.mi
    j = path.mj
    s = "# From minima " + str(i) + " ("
    for crd in crds[0, :]:
        s += "  %f" % crd
    s += ")\n#   to minima " + str(j) + " ("
    for crd in crds[crds.shape[0] - 1, :]:
        s += "  %f" % crd
    s += ")\n"
    s += "# Highest energy: %8.3E\n\n" % path.maxe
    s += "# coordinates, energy\n"

    for ci in range(crds.shape[0]):
        for crd in crds[ci, :]:
            s += "  %f" % crd
        s += "  %8.3E\n" % path.energy[ci]
    ioutils.overwrite("mep/pathcrds_" + str(i) + "_" + str(j) + ".dat", s)
