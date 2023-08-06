import numpy as np
from scipy import stats
import h5py

def read_TA_data(directory, unthresholded = False):
    # Loading innovations signals
    innov_file = directory + 'Innovation.mat'
    innov_h5py = h5py.File(innov_file, 'r')
    
    i_sig_file = directory + 'SignInnov.mat'
    i_sig_h5py = h5py.File(i_sig_file, 'r')
    
    par_file = directory + 'param.mat'
    param = h5py.File(par_file, 'r')['param']
    
    i_sig = i_sig_h5py[list(i_sig_h5py.keys())[0]][()]
    
    if unthresholded:
        innov = innov_h5py[list(innov_h5py.keys())[0]][()]

        return i_sig, param, innov
    else:
        return i_sig, param

def fix_temporal_dim(inno_sigs, icaps_param):
    '''
    Method to fix the temporal dimension of innovation signals after two-step thresholding.
    As frames with less than 500 active voxel are discarded, two consecutive frames may be
    temporally separated by more than one time point.
    '''
    n_timepoints = icaps_param['mask_threshold2pos'].shape[1]
    
    mask_pos = icaps_param['mask_threshold2pos'][()][0]
    mask_neg = icaps_param['mask_threshold2neg'][()][0]
    
    fixed_isig = np.zeros((len(inno_sigs), n_timepoints))
    
    fixed_isig[:, np.where(mask_pos > 0)[0]] += inno_sigs[:, :mask_pos.sum()]
    fixed_isig[:, np.where(mask_neg > 0)[0]] += inno_sigs[:, mask_pos.sum():]

    return fixed_isig

def isig_threshold(isig, z_thresh = 1, v = False):
    '''
    Method to threshold the innovation signal based on a z-score threshold.
    '''
    #bin_isig_z = (np.abs(stats.zscore(isig, axis = 1)) > z_thresh)
    bin_isig_z = (stats.zscore(np.abs(isig), axis = 1) > z_thresh)
    
    isig_t = np.zeros_like(isig)
    isig_t[bin_isig_z] = isig[bin_isig_z]
    
    return isig_t
    
def local_max_filter(signals, window = 1, v = False):
    '''
    Method to filter the innovation signals by only keeping local maximas within a window.
    '''
    zero_pad = np.zeros((len(signals), window))
    
    fltrd = np.hstack((zero_pad, signals, zero_pad))
    
    for i in range(len(signals[0])):
        is_local_max = (signals[:, i] == np.max(fltrd[:, i:i+2+window], axis = 1))
        fltrd[:, i + window] = is_local_max * signals[:, i]
    
    return fltrd[:, window:-window]
