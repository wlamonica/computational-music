# Computational Music
An exploration and collection of projects related to Music Information Retrieval (MIR) and Computational Music Analysis in general  
**Start Date**: January 2026  
**Last Major Development**: January 2026, Time Signature Estimation Paper Implementation

## Goals
### Paper Replication
Especially at the start of this project, I want to replicate papers on various MIR tasks in order to understand the techniques being used. When many of these early papers have no source code, having to implement these techniques is an excellent tool for learning.  
When possible, I also want to take liberties in the implementation of the paper paper to improve results
### Development of MIR modules
Using the techniques learned from replicating and reading papers, I want to be able to develop my own modules to perform common MIR tasks. My greatest areas of interest are **Meter/Time Signature Detection** and **Chord Recognition**. 
## Recently Completed 
### Beat Similarity Matrix Based Time Signature Estimator - Alpha version
Created an untested (I currently lack data) version of the time signature estimator [in this paper](https://ieeexplore.ieee.org/abstract/document/4959587), which does the following:
- Uses a spectrogram of the STFT of the audio
- Uses onset correlation to estimate the beat times in the piece 
- To create the BSM, for every pair of beats:
    - Get the subset of the spectrogram within the beats' time-frames
    - Compute the distance between each frame between the two beats to create an audio similarity matrix (ASM)
    - Run a dynamic time warping algorithm to get a value for the minimized difference between the two beats (dtw allows you to account for asychronicities between the two beats)
    - Set its corresponding place in the matrix to that value
- For every positive horizontal offset, compute the average of the diagonal values of the BSM (wrt to the offset). Call this array $d$
- Use a comb filter (see code) to pick the best out of a set of candidates for meter by picking candidates whose multiples have indices in $d$ that are consistently high

Next steps:
- Use beatles dataset containing meter combined with Itunes audio to test meter detection

