#!/usr/bin/env python
# coding: utf-8


from .synthetic import *
from .delay import *
from .validation import *
from .innovation import *

from itertools import repeat

def gen_sim_data(n_reg = 100, n_timep = 800, n_max_perm = 400, fol_inter = False, v = False,
                 jitter = 0, pre_thresh = 0.7, parallel = True, chunksize = 2, n_cores = None, **kwargs):
    if v:
        print('Generation of synthetic data:')
        print('{} regions, {} timepoints, {} random samples'.format(n_reg,
                                                                    n_timep,
                                                                    n_max_perm))
    
        all_par = ['{}={}'.format(kw, kwargs.get(kw)) for kw in kwargs]
        print(*(all_par))
    # Structured Simulation
    simulation, seed_id, fol_id, seed_choice = simulate_activation(
        n_regions = n_reg, n_timepoints = n_timep, **kwargs)

    sim_tresh = isig_threshold(simulation, z_thresh = pre_thresh)

    if v:
        print('Measurement on structured data...')
    # Delay measurement on structured data

    del_std_pattern = delay_measure(sim_tresh, parallel = parallel, n_cores = n_cores, v = v)
    
    # Computation of ideal results from encoded structure
    expected = get_encoded_structure(seed_choice, fol_id, n_reg, fol_inter = fol_inter)

    if type(jitter) in [int, float]:
        jitter = [jitter]
    
    n_jit = len(jitter)
    del_std_perm = np.empty((n_jit, n_max_perm, n_reg, n_reg))

    for jit_id, jit in enumerate(jitter):

        # Shuffling of innovations
        sim_perm = permute_innovations(sim_tresh, n_max_perm, jitter = jit, noise = False)
        
        if v:
            print('Jitter {} out of {}'.format(jit_id + 1, n_jit))
            print('Measurement on shuffled data...')

        if parallel == False:
            with Pool(processes = None) as pool:
                for permut_id, pool_res in enumerate(pool.istarmap(delay_measure, zip(sim_perm, repeat(pre_thresh)),
                                                                    chunksize = chunksize)):
                    del_std_perm[jit_id, permut_id] = pool_res

                #pares = pool.starmap(delay_measure, zip(sim_perm, repeat(pre_thresh)), chunksize = chunksize)
                #del_std_perm[jit_id] = pool.starmap(delay_measure, zip(sim_perm, repeat(pre_thresh)), chunksize = 4)

            #del_std_perm[jit_id] = pares
        else:
            # Delay measurement on shuffled data
            for permut_id, permut in enumerate(sim_perm):
                del_std_perm[jit_id, permut_id] = delay_measure(permut, parallel = parallel,
                                                                chunksize = chunksize, n_cores = n_cores)

    if n_jit == 1:
        del_std_perm = del_std_perm.reshape((n_max_perm, n_reg, n_reg))
    
    return del_std_pattern, del_std_perm, expected, seed_choice