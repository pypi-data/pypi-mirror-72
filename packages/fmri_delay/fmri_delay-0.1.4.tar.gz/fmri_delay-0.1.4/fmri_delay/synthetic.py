import numpy as np
from scipy import stats
from itertools import permutations

def piecewise_activity(n_timepoints = 1000, trans_prob = 1e-3, trans_amp = 5, noise = 0):
    time_course = np.empty((n_timepoints))
    innovation = np.zeros_like(time_course)
    time_course[0] = np.random.normal(0, 5)
    last_trans = 0
    # Storing progression of numbers of draw (in binomial)
    n_draws = []

    t_prob = trans_prob + 0

    for t in np.arange(1, n_timepoints, 1):
        #if np.random.binomial(t - last_trans, t_prob):
        if np.random.binomial(1, t_prob):
            # Computation of transition amplitude
            transition = np.random.normal(0, trans_amp)
            
            # Store the progression of n_draws
            n_draws.extend(np.arange(t - last_trans))
            
            time_course[t] = transition
            last_trans = t
            
            # Randomization of transition probablity
            t_prob = abs(np.random.normal(trans_prob, trans_prob/4))
            
            innovation[t] = transition - time_course[t-1]
        else:
            time_course[t] = time_course[t - 1]
            
    n_draws.extend(np.arange(t - last_trans))
    
    if noise:
        time_course += np.random.normal(np.zeros_like(time_course), noise)
        innovation += np.random.normal(np.zeros_like(time_course), noise)
    
    return time_course, innovation, n_draws


def gen_follower(seed, delay, activ_prob = 100, noise = 0, rand_delay = 1, z_thresh = 0.6):
    
    follower = np.zeros_like(seed)
    
    # Computation of random delay
    peaks = np.where(np.abs(stats.zscore(seed)) > z_thresh)[0]
    shift = delay + np.random.normal(np.zeros_like(peaks), rand_delay)

    # Min delay is fixed to 1 time point
    shift[shift < 1] = 1

    shifted = np.ceil(peaks + shift).astype(int)

    # Discard activity at time larger than n_timepoints
    shifted = shifted[shifted < len(seed)]

    # Assign a random value (from the value of the activity of the seed) to the followers
    follower[shifted] = np.random.choice(seed[peaks], len(shifted))

    # Randomly relocate the innovation of followers with probability "activ_prob"
    #n_rand_act = np.percentile(np.arange(len(shifted)), 100 - activ_prob,
    #                           interpolation = 'nearest')
    n_rand_act = np.random.binomial(len(shifted), 1 - activ_prob/100)

    rand_discard = np.random.choice(shifted, n_rand_act)
    
    follower[rand_discard] = 0
    
    # Add random activity (regardless of the seed activity)
    unactiv_id = np.where(follower == 0)[0]
    rand_act = np.random.choice(unactiv_id, n_rand_act)

    follower[rand_act] = np.random.choice(seed[peaks], n_rand_act)
    
    added_noise = np.random.normal(np.zeros_like(seed), noise)
    follower += added_noise
    
    return follower

def simulate_activation(n_regions = 20, n_seeds = 0, n_followers = 0, fol_levels = [],
                        n_timepoints = 400, delay = [10], activ_proba = [1e-3, 100],
                        noise = 0, rand_delay = 1, real_fMRI = None, **kwargs):

    if len(fol_levels) == 0:
        fol_levels = [n_followers]
    # Condition for multi-level interactions of followers
    elif (np.sum(fol_levels) != n_followers):
        print('Warning: Unknown followers levels structure\nn_fol: {}, levels: {}'
            .format(n_followers, fol_levels))
    # Condition for different delays at each level
    if (type(delay) == int):
        delay = [delay]
    if (len(delay) != len(fol_levels)):
        print('Warning: Un-matched length of delays with respect to follower'+
            'levels, n_delays: {}, levels: {}' .format(len(delay), fol_levels))
        print('Assuming delays of further levels as {}'.format(delay[-1]))
        delay += [delay[-1] for _ in fol_levels[len(delay):]]
        
    if real_fMRI is not None:
        n_regions = len(real_fMRI)

    # Random group allocation of region id
    non_random_id = np.random.choice(n_regions, n_seeds + n_followers, replace = False)
    
    seeds_id = non_random_id[:n_seeds]
    followers_id = non_random_id[n_seeds:n_seeds + n_followers]

    if real_fMRI is not None:
        time_course = np.copy(real_fMRI)
    else:
        # Initialization of time course
        time_course = np.empty((n_regions, n_timepoints))
        
        # Use of innovation signals from piecewise constant voxel activity
        for i in np.arange(n_regions):
            _, time_course[i], _ = piecewise_activity(n_timepoints, activ_proba[0], noise = noise)
    
    # Generation of followers states (random choice of seed)
    seed_choice = []

    fol_lvl = [0, fol_levels[0]]
    fol_levels = np.roll(fol_levels, -1)
    to_follow = seeds_id

    for i in range(n_followers):
        # Choice of followed seed
        if (i >= fol_lvl[1]):
            to_follow = followers_id[fol_lvl[0]:fol_lvl[1]]
            fol_lvl[0] = fol_lvl[1]
            fol_lvl[1] += fol_levels[0]
            fol_levels = np.roll(fol_levels, -1)
            delay = np.roll(delay, -1)

        seed_choice.append(np.random.choice(to_follow))
        chosen = time_course[seed_choice[i]]
        # Generation of follower
        time_course[followers_id[i]] = gen_follower(chosen, delay[0], activ_proba[1], noise, rand_delay)
    
    return time_course, seeds_id, followers_id, np.array(seed_choice)

def get_encoded_structure(seed_choice, fol_id, n_reg, fol_inter = False):
    # Computation of directly encoded structure
    expected = np.zeros((n_reg, n_reg))
    for f_id, chosen in zip(fol_id, seed_choice):
        expected[seed_choice, fol_id] = 1
    
    # Computation of indirectly encoded structure
    # Interaction between followers with similar seeds
    if fol_inter:
        for u_seed in np.unique(seed_choice):
            fol_sim_seed = fol_id[np.where(seed_choice == u_seed)[0]]
            for fol_inter in permutations(fol_sim_seed, 2):
                expected[fol_inter] = 0.5
        
    return expected