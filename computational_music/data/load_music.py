import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

def fma_song_paths(track_ids):
    def fma_song_path(track_id):
        id = str(track_id)
        id = "".join(["0" for idx in range(0,6 - len(id),1)]) + id
        path = BASE_DIR / "music_audio" / f"{id}.mp3"
        return str(path) if os.path.isfile(path) else None
    results = [fma_song_path(id) for id in track_ids]
    return pd.DataFrame({"track_id": track_ids, 
                         "path": results})

def beatles_song_paths():
    def list_file_paths(folder):
        path = BASE_DIR / folder
        return [str(p) for p in path.iterdir() if p.is_file()]
    paths = list_file_paths("beatles_audio")
    sorted_paths = sorted(
        paths,
        key=lambda p: int(Path(p).stem)
    )
    return sorted_paths

# if __name__ == "__main__":
#     print(f"result: {get_song_path("1039")}")
