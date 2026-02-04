import numpy as np
import librosa

def diag_bsm_averages(bsm):
        bsm_shortened = bsm[:, 1:-1]
        diags = np.zeros(bsm_shortened.shape[1])
        for i in range(diags.shape[0]):
            diags[i] = bsm_shortened.diagonal(offset = i).mean()
        diags_inv = diags.max() - diags
        for i in range(diags_inv.shape[0]):
            is_peak =  not(i > 0 and diags_inv[i] < diags_inv[i - 1]) and \
                        not(i < (diags_inv.shape[0] - 1) and diags_inv[i] < diags_inv[i + 1])
            diags_inv[i] = diags_inv[i] * 1.5 if is_peak else diags_inv[i]
        return diags_inv

def compute_bsm(audio, sr):
        tempo, beat_times = librosa.beat.beat_track(y=audio, sr=sr, units="time")
        n_fft = 1024
        hop_length = 512
        spectrogram = librosa.stft(y=audio, n_fft=n_fft, hop_length=hop_length)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
        spectrogram = spectrogram[freqs <= 5000]
        logS = abs(spectrogram)

        def get_asm_val(beat1_frame, beat2_frame, beat_frame_length):
            max_frame1 = min(beat1_frame + beat_frame_length, logS.shape[1]) 
            max_frame2 = min(beat2_frame + beat_frame_length, logS.shape[1]) 
            frames_1 = logS[: , beat1_frame : max_frame1]
            frames_2 = logS[: , beat2_frame : max_frame2]

            comparison_width_pct = 0.2
            D, wp = librosa.sequence.dtw(X=frames_1.T, Y=frames_2.T, metric = 'cosine', band_rad=comparison_width_pct)
            final_val = D[-1,-1]
            return final_val    

        beat_frames = beat_times * sr / hop_length
        beat_frame_length = int((60 / tempo) * sr / hop_length)

        bsm = np.zeros((len(beat_frames), len(beat_frames)))

        for i in range(len(beat_frames) - 1):
            for j in range(len(beat_frames) - 1):
                try: 
                    bsm[i,j] = get_asm_val(int(beat_frames[i]), int(beat_frames[j]), beat_frame_length)
                except Exception as e:
                    print(f"comparison failed at beats: {i,j}: {e}")

        return bsm

def bsm_meter_estimator(audio, sr, candidates = [2,3,4,5,6,7,8,9,11,12]):
    def pick_meter(diag_similarity_avg, candidates = [2,3,4,5,6,7,8,9,11,12]):
        def tc(diag_similarity_avg, c):
            if diag_similarity_avg.shape[0] // c <= 1:
                    return 0
            p_array = np.arange(1, diag_similarity_avg.shape[0] // c)
            pick_idx = p_array * c
            picks = diag_similarity_avg[pick_idx]
            denom = 1 / p_array**(1.2)
            return (picks * denom).sum()
        max_candidate = candidates[0]
        max_tc = 0
        for c in candidates:
            for i in range(0,int(diag_similarity_avg.shape[0] // 2)):
                d = diag_similarity_avg[i:]
                tc_new = tc(d, c)
                if max_tc < tc_new:
                    max_tc = tc_new
                    max_candidate = c

        return max_candidate
    
    bsm = compute_bsm(audio, sr)
    diags = diag_bsm_averages(bsm)
    return pick_meter(diags, candidates=candidates), bsm