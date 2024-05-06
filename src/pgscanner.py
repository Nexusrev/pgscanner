import os
import time
import logging
from multiprocessing import Pool
import argparse
from colorama import Fore, Style, init

# Initialize colorama to make terminal text color work on all platforms
init(autoreset=True)

# Setup for the logs directory
base_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(base_dir, '..', 'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, 'scan_log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def find_config(config, search_root):
    """Tailored search for PostgreSQL config files using os.walk(), with performance logging."""
    start_time = time.time()
    found_files = []
    for root, dirs, files in os.walk(search_root):
        for file in files:
            if config in file:
                full_path = os.path.join(root, file)
                found_files.append(full_path)
                logging.info(f"Found {config}: {full_path}")
    elapsed_time = time.time() - start_time
    logging.info(f"Scanned {len(found_files)} files for {config} in {elapsed_time:.2f} seconds")
    return found_files

def search_configs(search_root, configs):
    """Search for configurations using multiprocessing for speed improvement."""
    with Pool(processes=len(configs)) as pool:
        results = pool.starmap(find_config, [(config, search_root) for config in configs])
    return [path for sublist in results for path in sublist if path]

def setup_arg_parser():
    """Setup CLI argument parser."""
    parser = argparse.ArgumentParser(description='PostgreSQL Configuration File Scanner')
    parser.add_argument('-p', '--path', type=str, required=True, help='Root directory to start the scan')
    parser.add_argument('-c', '--configs', nargs='+', default=['postgresql.conf', 'pg_hba.conf'], help='List of config files to scan for')
    return parser

def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    print(Fore.YELLOW + Style.BRIGHT + "Starting pgscanner...")
    found_configs = search_configs(args.path, args.configs)
    
    if found_configs:
        print(Fore.GREEN + Style.BRIGHT + "Found configuration files:")
        for config in found_configs:
            print(Fore.CYAN + config)
    else:
        print(Fore.RED + "No configuration files found.")

if __name__ == "__main__":
    main()
