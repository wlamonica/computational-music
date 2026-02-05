# HERE YOU SHOULD IMPORT THE FUNCTION YOU WANT TO USE
from computational_music.data.load_data import *
from computational_music.features.time_features import bsm_meter_estimator_path
import pandas as pd
import multiprocessing as mp
import time
import pickle
import warnings
from pathlib import Path
import datetime

# Suppress only DeprecationWarning
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Configure the following before running
EXPENSIVE_FUNCTION = bsm_meter_estimator_path
RESULTS_SUBFOLDER = 'time_signature_bsm'
OUTPUT_FILE_NAMES = [f'results_{datetime.datetime.now().strftime('%Y_%m_%d_%H')}.csv','bsms.pkl']


def apply_multiprocessing(iterable, func, column_name=None, n_cores=None, function_name="func"):
    if column_name and isinstance(iterable, pd.DataFrame):
        iterable = iterable[column_name]
    
    if n_cores is None:
        n_cores = mp.cpu_count()
    
    with mp.Pool(n_cores) as pool:
        result = pool.map(func, iterable)
    
    return result


# May need to configure some stuff when running the script
if __name__ == "__main__":
    print("Entered main")
    df = beatles_tracks(include_path=True)

    before = time.time()
    results = apply_multiprocessing(df, EXPENSIVE_FUNCTION, column_name='paths')
    after = time.time()
    print(f"With mp: {after - before} seconds")

    meters = [result[0] for result in results]
    bsms = [result[1] for result in results]

    df['estimated_meters'] = pd.Series(meters)
    
    # Get the directory where THIS script is located
    script_dir = Path(__file__).parent
    results_dir = script_dir.parent / 'results' / RESULTS_SUBFOLDER
    results_dir.mkdir(parents=True, exist_ok=True)
    output_file = results_dir / OUTPUT_FILE_NAMES[0]

    df.to_csv(output_file, index=False)

    output_file = results_dir / OUTPUT_FILE_NAMES[1]
    with open(output_file, 'wb') as file:
        pickle.dump(bsms,  file, protocol=pickle.HIGHEST_PROTOCOL)
