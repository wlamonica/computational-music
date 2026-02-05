import pandas as pd
from pathlib import Path
from computational_music.data.load_music import fma_song_paths, beatles_song_paths

BASE_DIR = Path(__file__).resolve().parent

def fma_tracks(include_path=False):
    '''Returns the tracks dataframe from the fma_small archive, **assuming you've downloaded it** and placed it in the corresponding folder
    
    Allows you to include the corresponding paths to the audio tracks in the dataset'''
    file_path = BASE_DIR / "fma_metadata" / "tracks.csv"
    df = pd.read_csv(file_path)
    columns = [f"{a} {b}" for a, b in zip(df.columns, df.loc[0])]
    columns[0] = "track_id"
    df = df.loc[2:,:]
    df.columns = columns
    if include_path:
        song_paths = fma_song_paths(df['track_id'])
        df = pd.merge(song_paths, df, on= "track_id")
    return df.copy()

def beatles_tracks(include_path=False):
    '''Returns a dataframe of [this beatles song dataset](https://www.kaggle.com/datasets/devedzic/the-beatles-songs-dataset), **assuming you've downloaded it** and placed it in the correct folder (see load_music.py)
    
    Allows you to include the corresponding paths to the audio tracks in the dataset'''
    file_path = BASE_DIR / "beatles_metadata" / "tracks.csv"
    df = pd.read_csv(file_path)
    if include_path:
        song_paths = beatles_song_paths()
        # print(song_paths[0])
        df['paths'] =  song_paths
    return df.copy()

# df = get_beatles_tracks(True)
# print(df[['Title','paths']].head(2))