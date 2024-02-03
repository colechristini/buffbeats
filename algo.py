import numpy as np

def exp_decay (t): 
    return np.exp(-t/10)

# For Misho - takes in list of segments and returns tuple of segments
# corresponding to intro and outro sections
def get_segments(segments, intro_length, outro_length):
    intro_segments = []
    outro_segments = []
    accumulated_time_intro = 0
    intro_index = 0
    while accumulated_time_intro < intro_length:
        accumulated_time_intro += segments[intro_index].duration
        intro_segments.append(segments[intro_index])
        intro_index += 1
    accumulated_time_outro = 0
    outro_index = len(segments) - 1
    while accumulated_time_outro < outro_length:
        accucumulated_time_outro += segments[outro_index].duration
        outro_segments.append(segments[outro_index])
        outro_index -= 1
    return (intro_segments,outro_segments[::-1])

def dynamic_time_warping(a_1, a_2, d):
    dtw = np.full((len(a_1) + 1, len(a_2) + 1), np.inf)
    dtw[0, 0] = 0
    for i in range(1, len(a_1) + 1):
        for j in range(1, len(a_2) + 1):
            cost = d((a_1[i - 1], a_2[j - 1]))
            dtw[i, j] = cost + min(dtw[i - 1,  j],
                                   dtw [i, j - 1],
                                   dtw[i - 1, j - 1])
    return dtw[-1, -1]
    
def segment_distance(s1, s2):
    s1_loudness_vec = [s1.loudness_start, s1.loudness_max,
                       s1.loudness_max_time, s1.loudness_end]
    s2_loudness_vec = [s2.loudness_start, s2.loudness_max,
                       s2.loudness_max_time, s2.loudness_end]
    weights = np.array([0.75, 1, 0.9, 0.6])
    loudness_dist = 1 - weighted_cos_sim(s1_loudness_vec, s2_loudness_vec, weights)
    dist = lambda a, b: abs(a - b)
    pitch_dist = dynamic_time_warping(s1.pitches, s2.pitches, dist)
    timbre_dist = dynamic_time_warping(s1.timbre, s2.timbre, dist)
    return 0.6 * loudness_dist + pitch_dist + 0.5 * timbre_dist

def weighted_cos_sim(a, b, weights):
    return np.dot(weights * a, b) / (np.linalg.norm(a) * np.linalg.norm(b))




def greedy(dists, start):
    out = [start]
    current = start
    length = len(dists)
    while len (out) < length:
        nextElem = np.argmin(dists[current])
        dists[:, current] = np.inf
        out.append(nextElem)
        current = nextElem
    return out

def generateRandomMatrix(x):
    out = np.random.rand(x, x)
    for i in range(len(out)):
        out[i,i] = np.inf
    return out

    

