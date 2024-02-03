import numpy as np
import numpy.typing as npt

# Exponential decay for comparing lists of notes.
# Inputs: The two indices
# Outputs: The exponential decay of the two indices.
def exp_decay (i, j):
    t = i + j
    return np.exp(-t/10)

# Compute the weighted cosine similarity between two arrays of floats.
# Inputs: Two arrays of floats, a weight array.
# Outputs: The weighted cosine similarity between the two arrays.
def weighted_cos_sim(a, b, weights):
    return np.dot(weights * a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Use dynamic time warping to find the distance between two 
# different sized lists/time series.
# Inputs: Two arrays, a distance function that computes the distance
# between an element of the first and an element of the second, and
# an optional weight function.
# Outputs: the DTW distance between the two lists.
# https://en.wikipedia.org/wiki/Dynamic_time_warping
def dynamic_time_warping(a_1, a_2, d, w = None):
    dtw = np.full((len(a_1) + 1, len(a_2) + 1), np.inf)
    dtw[0, 0] = 0
    for i in range(1, len(a_1) + 1):
        for j in range(1, len(a_2) + 1):
            cost = d(a_1[i - 1], a_2[j - 1])
            # Apply weight function to cost if provided, inspired by
            # https://www.sciencedirect.com/science/article/pii/S0020025520308501
            if w is not None: cost *= w(i - 1, j - 1 )
            dtw[i, j] = cost + min(dtw[i - 1,  j],
                                   dtw [i, j - 1],
                                   dtw[i - 1, j - 1])
    return dtw[-1, -1]
    
# Calculate distance between two supplied segments.
# Inputs: A pair of segments (sounds in the song).
# Outputs: A float representing the distance between the two segments.
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

# Calculate distance between two songs. 
# Inputs: A pair of songs.
# Outputs the distance between the end of the first song ad the start
# of the second.
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
    # Convert similarity to distance.
    sec_dist = 1 - weighted_cos_sim(outro_features, intro_features, weights)
    seg_dist = dynamic_time_warping(out_segs, int_segs, segment_distance, exp_decay)
    return 0.6 * sec_dist + seg_dist

# Generate pairwise (non-symmetric) distance matrix for a playlist
# of songs.
# Inputs: A list of songs, with type described below
# Outputs: The transition distance matrix, where dists[i,j] is the 'distance'
# between the end of song i and the start of song j, and a starting index.
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
# transition distances. 
# Inputs: A distance matrix representing the transition distance
# between songs.
# Outputs: A list of indices corresponding to the greedy order.
def greedy(dists : npt.NDArray[np.float_], start : int):
    out = [start]
    dist_out = []
    current = start
    length = len(dists)
    dists = np.copy(dists)
    while len (out) < length:
        nextElem = np.argmin(dists[current])
        dist_out.append(dists[current, nextElem])
        dists[:, current] = np.inf
        out.append(nextElem)
        current = nextElem
    return (out, sum(dist_out))

# Process a playlist by repeatedly solving using greedy heuristic and then
# selecting the ordering that minimizes the sum of transition distances between
# consecutive songs.
# Inputs: a list of songs, where a song is a tuple of type
# (intro_section : dict, intro segs : dict list,
#  outro_section : dict, outro segs : dict list)
# and an iteration count
# Outputs: A list of indices corresponding to the optimal order
def processPlaylist(songs, iterations : int):
    dists = make_matrix(songs)
    outputs = []
    max_dists = []
    for _ in range(iterations):
        start = np.random.randint(0, len(songs))
        order, maxDist = greedy(dists, start)
        outputs.append(order)
        max_dists.append(maxDist)
    print(outputs)
    return outputs[np.argmin(np.array(max_dists))]