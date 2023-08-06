import numpy as np
from scipy import stats

def locate_innovations(signal, thresh = None):
    '''
    Localization of innovations based on a z-score threshold of the innovation
    signal.
    '''
    if thresh is None:
        inno_tp = np.where(signal != 0)
        rest = np.where(signal == 0)
    else:
        # Location of innovations
        inno_tp = np.where(abs(stats.zscore(signal, axis = 1)) > thresh)
        # Location of the rest
        rest = np.where(abs(stats.zscore(signal, axis = 1)) <= thresh)
    
    return inno_tp, rest

def permute_innovations(signal, n_perm = 1, jitter = 0, noise = True, **kwargs):
    '''
    Shuffling voxel assignment of innovations.
    '''
    JITTER_SCALE = 5
    n_r, n_tp = signal.shape

    inno_tp, rest = locate_innovations(signal, **kwargs)

    if noise:
        # Computation of fluctuation "outside" of the innovations
        std = np.std(signal[rest])
        # Shuffling of innovation signals
        permuted = np.random.normal(np.zeros((n_perm, n_r, n_tp)), std)
    else:
        permuted = np.zeros((n_perm, n_r, n_tp))

    if jitter != 0:
        for perm in permuted:
            jit = np.random.normal(np.full_like(inno_tp[1], jitter), jitter/JITTER_SCALE)\
                    * np.sign(np.random.normal(np.zeros_like(inno_tp[1]), 1))

            shift = inno_tp[1] + jit.astype(int)

            shift[shift >= n_tp] -= n_tp
            shift[shift < 0] += n_tp

            perm[inno_tp[0], shift] = signal[inno_tp]
    else:
        for perm in permuted:
            perm[np.random.permutation(inno_tp[0]), inno_tp[1]] = signal[inno_tp]
    
    return permuted

def significant_results(real_meas, rand_meas, corr = True, return_t = False):
    '''
    Evaluation of the statistical significance of delay consistency by
    comparing each individual result with its multiple corresponding 
    measurement on shuffled data.
    '''
    n_reg, n_perm = len(real_meas), len(rand_meas)
    
    real_vect = real_meas.reshape(1, -1)
    rand_vect = rand_meas.reshape(n_perm, -1)
    
    # Computation of the expected number of results by chance (no correction)
    multiple_tests = (n_reg * n_reg - n_reg)
    #print(int(0.05 * multiple_tests), 'results are expected by chance.')
    
    # One sample t-test between real measurement and random results
    tval, pval = stats.ttest_1samp(rand_vect, real_vect, axis = 0)

    # /!\ Converting to one-sided test /!\
    if return_t:
        return tval.reshape(n_reg, n_reg), pval.reshape(n_reg, n_reg)

    
    # Condition for Bonferroni correction of p-values
    if corr:
        signif = np.where(pval < (0.05)/multiple_tests, 1, 0)
    else:
        signif = np.where(pval < (0.05), 1, 0)
    
    n_sig = signif.sum()
    #print(n_sig, 'results show significance.')

    return signif.reshape(n_reg, n_reg)

def binarize_results(real_meas, rand_meas, thresh = 1):
    '''
    Binarization of delay consistency matrix based on a relative z-score
    threshold.
    '''
    n_reg, n_perm = len(real_meas), len(rand_meas)
    
    real_vect = real_meas.reshape((-1, 1))
    rand_vect = rand_meas.reshape(n_perm, -1).T
    
    # Computation of relative z-scores
    rel_z = stats.zmap(real_vect, rand_vect, axis = 1).reshape(n_reg, n_reg)
    binary_z = np.where(rel_z > thresh, 1, 0)
    
    return binary_z, rel_z

def empirical_null_dist(real_meas, rand_meas, per_voxel = False, alpha_level = 95):
    '''
    Binarization of delay consistency matrix based on a empirical Null distribution
    from shuffled data.
    '''

    n_rand, n_reg, _ = rand_meas.shape
    
    if per_voxel:
        real_vec = real_meas.reshape(-1)
        rand_vec = rand_meas.reshape((n_rand, -1)).T

        empirical_bound = np.percentile(rand_vec, 1, axis = 1)

        bin_results = (real_vec < empirical_bound).reshape((n_reg, -1)).astype(int)
    else:
        nonan = rand_meas[~np.isnan(rand_meas)]

        empirical_bound = np.percentile(nonan, alpha_level)
        bin_results = (real_meas < empirical_bound).astype(int)

    return bin_results

def recovery_score(bin_results, expectations, fol_inter = False):
    '''
    Estimation of a recovery score by computing the number of false positive and
    negatives from the encoded structure (expectations).
    '''
    diff = bin_results - expectations
    
    if fol_inter:
        n_FN = [len(diff[diff == -1]), len(diff[diff == -0.5])]
        n_FP = [len(diff[diff == 1]), len(diff[diff == 0.5])]
    else:
        n_FN = len(diff[diff < 0])
        n_FP = len(diff[diff > 0])

    return n_FN, n_FP