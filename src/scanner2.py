import os
import time
import logging
from multiprocessing import Pool

# Setup for the logs directory
base_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(base_dir, '..', 'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, 'scan_log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def find_config(config, search_root):
    """Tailored search for PostgreSQL config files using os.walk(), with performance and progress logging."""
    start_time = time.time()
    file_count = 0
    found_files = []
    for root, dirs, files in os.walk(search_root):
        file_count += len(files)  # Increment the file count
        for file in files:
            if config in file:
                full_path = os.path.join(root, file)
                found_files.append(full_path)
                logging.info(f"Found {config}: {full_path}")
        # Log progress for every 1000 files checked
        if file_count % 1000 == 0:
            logging.info(f"Checked {file_count} files so far in {search_root}...")
    elapsed_time = time.time() - start_time
    logging.info(f"Scanned {len(found_files)} files for {config} in {elapsed_time:.2f} seconds. Total files checked: {file_count}")
    return found_files

def search_configs(search_root, configs):
    """Search for configurations using multiprocessing for speed improvement."""
    with Pool(processes=len(configs)) as pool:
        results = pool.starmap(find_config, [(config, search_root) for config in configs])
    return [path for sublist in results for path in sublist if path]

if __name__ == "__main__":
    # Define the directory to scan and configuration files to look for
    test_search_root = '/Users/nicolasramirez'  # Modify this path to a suitable test location
    test_configs = ['postgresql.conf', 'pg_hba.conf', 'pg_ident.conf']
    
    # Call the search_configs function
    found_configs = search_configs(test_search_root, test_configs)
    
    # Print the results
    print("Found configuration files:")
    for config in found_configs:
        print(config)
