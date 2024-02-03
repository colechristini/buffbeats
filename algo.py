import numpy as np

# Exponential decay for comparing lists of notes
def exp_decay (i, j):
    t = i + j
    return np.exp(-t/10)

# Compute the weighted cosine similarity between two arrays of floats
def weighted_cos_sim(a, b, weights):
    return np.dot(weights * a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# For Misho - takes in list of segments and returns tuple of segments
# corresponding to intro and outro sections
def get_segments(segments, intro_length, outro_length):
    intro_segments = []
    outro_segments = []
    accumulated_time_intro = 0
    intro_index = 0
    # Get segments corresponding to intro
    while accumulated_time_intro < intro_length:
        accumulated_time_intro += segments[intro_index]['duration']
        intro_segments.append(segments[intro_index])
        intro_index += 1
    accumulated_time_outro = 0
    outro_index = len(segments) - 1
    # Get segments corresponding to outro
    while accumulated_time_outro < outro_length:
        accucumulated_time_outro += segments[outro_index]['duration']
        outro_segments.append(segments[outro_index])
        outro_index -= 1
    return (intro_segments,outro_segments)

# Use dynamic time warping to find the distance between two 
# different sized lists/time series, using a supplied distance 
# function and an optional weight function
def dynamic_time_warping(a_1, a_2, d, w = None):
    dtw = np.full((len(a_1) + 1, len(a_2) + 1), np.inf)
    dtw[0, 0] = 0
    for i in range(1, len(a_1) + 1):
        for j in range(1, len(a_2) + 1):
            cost = d(a_1[i - 1], a_2[j - 1])
            if w is not None: cost *= w(i - 1, j - 1 )
            dtw[i, j] = cost + min(dtw[i - 1,  j],
                                   dtw [i, j - 1],
                                   dtw[i - 1, j - 1])
    return dtw[-1, -1]
    
# Calculate distance between two supplied segments
def segment_distance(s1, s2):
    s1_loudness_vec = [s1['loudness_start'], s1['loudness_max'],
                       s1['loudness_max_time'], s1['loudness_end']]
    s2_loudness_vec = [s2['loudness_start'], s2['loudness_max'],
                       s2['loudness_max_time'], s2['loudness_end']]
    weights = np.array([0.75, 1, 0.9, 0.6])
    loudness_dist = 1 - weighted_cos_sim(s1_loudness_vec, s2_loudness_vec, weights)
    dist = lambda a, b: abs(a - b)
    pitch_dist = dynamic_time_warping(s1['pitches'], s2['pitches'], dist)
    timbre_dist = dynamic_time_warping(s1['timbre'], s2['timbre'], dist)
    return 0.6 * loudness_dist + pitch_dist + 0.5 * timbre_dist

# Calculate distance between two songs
def song_dist(s1, s2):
    out_sec = s1[2]
    out_segs = s1[3]
    int_sec = s2[0]
    int_segs = s2[1]
    outro_features = [out_sec['loudness'], out_sec['tempo'],
                      out_sec['key'], out_sec['mode']]
    intro_features = [int_sec['loudness'], int_sec['tempo'],
                      int_sec['key'], int_sec['mode']]
    weights = np.array([0.6, 0.7, 1, 0.8])
    sec_dist = 1 - weighted_cos_sim(outro_features, intro_features, weights)
    # Figure out how to 
    seg_dist = dynamic_time_warping(out_segs, int_segs, segment_distance, exp_decay)
    return 0.6 * sec_dist + seg_dist

# Generate pairwise (non-symmetric) distance matrix for a playlist
# of songs
def make_matrix(songs):
    dists = np.zeros((len(songs), len(songs)))
    for i in range(len(songs)):
        for j in range(len(songs)):
            if i == j:
                dists[i,j] = np.inf
            else:
                dists[i,j] = song_dist(songs[i], songs[j])
    return dists

# Greedily solve aTSP to find a solution approximately minimizing
# transition distances
def greedy(dists, start):
    out = [start]
    dist_out = []
    current = start
    length = len(dists)
    while len (out) < length:
        nextElem = np.argmin(dists[current])
        dist_out.append(dists[current, nextElem])
        dists[:, current] = np.inf
        out.append(nextElem)
        current = nextElem
    return (out, sum(dist_out))

# Process a playlist by repeatedly solving using greedy heuristic
# and then selecting the ordering that minimizes the sum of 
# transition distances between consecutive songs
def processPlaylist(songs, iterations):
    dists = make_matrix(songs)
    outputs = []
    for _ in range(iterations):
        start = np.random.randint(0, len(songs))
        outputs.append(greedy(dists, start))
    return outputs[np.argmin(np.array(outputs)[:, 1])][0]

    

