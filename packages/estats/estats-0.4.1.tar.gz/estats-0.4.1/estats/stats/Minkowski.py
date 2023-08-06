# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'multi'

    required = ['Minkowski_max', 'Minkowski_min', 'Minkowski_steps',
                'Minkowski_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'no_V0']
    defaults = [2.0, -2.0, 100, 16, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], False]
    types = ['float', 'float', 'int', 'int', 'int', 'list', 'list', 'bool']
    return required, defaults, types, stat_type


def Minkowski(kappa, weights, ctx):
    """
    Calculates Minkowski functionals on a convergence map.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Minkowski functionals as V0,V1,V2 concatinated.
    """

    thresholds = np.linspace(ctx['Minkowski_min'],
                             ctx['Minkowski_max'], ctx['Minkowski_steps'])

    # do not use neighbouring pixels that are too close to estimate
    # derivatives (numerically unstable)
    mean_dist = np.sqrt(hp.pixelfunc.nside2pixarea(ctx['NSIDE']))
    min_dist = mean_dist * 0.1

    ell = kappa.size
    nside = hp.get_nside(kappa)
    ran = np.arange(ell, dtype=np.int)

    # remove masked pixels
    ran = ran[kappa > hp.pixelfunc.UNSEEN]
    neighbours = hp.get_all_neighbours(nside, ran)
    edges = np.all(kappa[neighbours] > hp.pixelfunc.UNSEEN, axis=0)
    ran = ran[edges]

    V1_tot = np.zeros(0, dtype=ctx['prec'])
    V2_tot = np.zeros(0, dtype=ctx['prec'])
    num_chunks = 1
    for r in np.array_split(ran, num_chunks):
        deriv_phi = np.zeros(ell, dtype=ctx['prec'])
        deriv_theta = np.zeros(ell, dtype=ctx['prec'])

        neighbours = hp.get_all_neighbours(nside, r)
        t_neigh, p_neigh = hp.pixelfunc.pix2ang(nside, neighbours)

        delta_kappa = kappa[neighbours] - kappa[r]

        t_pos, p_pos = hp.pixelfunc.pix2ang(nside, r)
        t_dist = t_neigh - t_pos
        p_dist = p_neigh - p_pos
        dist = np.sqrt(t_dist**2 + p_dist**2)
        t_perc = t_dist / dist
        p_perc = p_dist / dist

        delta_kappa = np.divide(delta_kappa, dist)

        mask = dist < min_dist

        # Now calculate gradients
        mx = np.ma.masked_array(delta_kappa * p_perc,
                                mask=mask, dtype=ctx['prec'])
        deriv_phi[r] = np.ma.mean(mx, axis=0)

        mx = np.ma.masked_array(delta_kappa * t_perc,
                                mask=mask, dtype=ctx['prec'])
        deriv_theta[r] = np.ma.mean(mx, axis=0)

        # calculate V2 part by part to save RAM
        #######################################
        # term 1
        delta_phi_kappa = deriv_phi[neighbours] - deriv_phi[r]

        deriv_phi_theta = np.zeros(ell, dtype=ctx['prec'])
        mx = np.ma.masked_array(delta_phi_kappa * t_perc,
                                mask=mask, dtype=ctx['prec'])
        deriv_phi_theta[r] = np.ma.mean(mx, axis=0)

        V2 = 2. * deriv_phi * deriv_phi_theta * deriv_theta

        # term 2
        deriv_phi_phi = np.zeros(ell, dtype=ctx['prec'])
        mx = np.ma.masked_array(delta_phi_kappa * p_perc,
                                mask=mask, dtype=ctx['prec'])
        deriv_phi_phi[r] = np.ma.mean(mx, axis=0)

        V2 -= deriv_theta**2. * deriv_phi_phi

        # term 3
        delta_theta_kappa = deriv_theta[neighbours] - deriv_theta[r]

        deriv_theta_theta = np.zeros(ell, dtype=ctx['prec'])
        mx = np.ma.masked_array(
            delta_theta_kappa * t_perc, mask=mask, dtype=ctx['prec'])
        deriv_theta_theta[r] = np.ma.mean(mx, axis=0)

        V2 -= deriv_phi**2. * deriv_theta_theta

        # calculate V1
        ##############
        V1 = deriv_theta**2. + deriv_phi**2.

        V2 /= V1
        V1 = np.sqrt(V1)
        V1_tot = np.append(V1_tot, V1[r])
        V2_tot = np.append(V2_tot, V2[r])

    # mask kappa
    kappa = kappa[ran]

    # averaged standard deviation and normalization
    sigma_0 = np.sqrt(np.mean(kappa**2.))
    thresholds *= sigma_0
    denom = np.sum(kappa > hp.pixelfunc.UNSEEN)
    bin_width = np.mean(thresholds[1:] - thresholds[:-1])

    # Minkowski calculation
    res = np.zeros(0)
    for ii, thres in enumerate(thresholds):
        # tolerance for dirac delta function is 10% of the width of each bin
        tolerance = 0.1 * bin_width / 2.
        delta_func = np.isclose(kappa, thres, rtol=0.0, atol=tolerance)
        V0_ = np.nansum(kappa >= thres) / denom
        V1_ = np.nansum(V1_tot[delta_func]) / (4. * denom)
        V2_ = np.nansum(V2_tot[delta_func]) / (2. * np.pi * denom)
        res = np.append(res, [V0_, V1_, V2_])

    # reordering
    V0 = res[0::3]
    V1 = res[1::3]
    V2 = res[2::3]
    res = np.append(V0, np.append(V1, V2))
    return res


def process(data, ctx, scale_to_unity=False):
    if scale_to_unity:
        data *= 1e10

    num_of_scales = len(ctx['scales'])

    new_data = np.zeros(
        (int(data.shape[0] / num_of_scales), data.shape[1]
         * num_of_scales))
    for jj in range(int(data.shape[0] / num_of_scales)):
        new_data[jj, :] = data[jj * num_of_scales:
                               (jj + 1) * num_of_scales, :].ravel()
    return new_data


def slice(ctx):
    # number of datavectors for each scale
    mult = 3
    # number of scales
    num_of_scales = len(ctx['scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'mean'

    n_bins_sliced = ctx['Minkowski_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # For Minkowski perform simple equal bin width splitting.
    # Same splitting for each smoothing scale.
    range_edges = [ctx['Minkowski_min'], ctx['Minkowski_max']]
    n_bins_original = ctx['Minkowski_steps']
    num_of_scales = len(ctx['scales'])
    n_bins_sliced = ctx['Minkowski_sliced_bins']
    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

    orig_bin_values = np.linspace(
        range_edges[0], range_edges[1], n_bins_original)

    per_bin = n_bins_original // n_bins_sliced
    remain = n_bins_original % n_bins_sliced
    remain_front = remain // 2
    remain_back = remain_front + remain % 2

    # Get edge indices
    bin_edge_indices_temp = np.arange(
        remain_front, n_bins_original - remain_back, per_bin)
    bin_edge_indices_temp[0] -= remain_front
    bin_edge_indices_temp = np.append(
        bin_edge_indices_temp, n_bins_original)

    # Get bin central values
    bin_centers_temp = np.zeros(0)
    for jj in range(len(bin_edge_indices_temp) - 1):
        bin_centers_temp = np.append(bin_centers_temp, np.nanmean(
            orig_bin_values[bin_edge_indices_temp[jj]:
                            bin_edge_indices_temp[jj + 1]]))

    # Assign splitting to each scale
    for scale in range(num_of_scales):
        bin_centers[scale, :] = bin_centers_temp
        bin_edge_indices[scale, :] = bin_edge_indices_temp

    return bin_edge_indices, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['Minkowski_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['Minkowski_sliced_bins']
            f = np.asarray(f)

        f = np.tile(f, 3)
        if ctx['no_V0']:
            f[:ctx['Minkowski_sliced_bins']] = False
        filter = np.append(filter, f)
    return filter
