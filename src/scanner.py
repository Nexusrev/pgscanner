# src/scanner.py

import subprocess
import logging
from multiprocessing import Pool

# Set up basic configuration for logging
logging.basicConfig(filename='/Users/nicolasramirez/Nexus/NxLab/scripts/pg_config_scanner/pg_config_scanner/src/scan_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def find_config(config, search_root):
    """Use subprocess to run find command and locate PostgreSQL config files."""
    try:
        result = subprocess.run(['find', search_root, '-name', config], capture_output=True, text=True)
        if result.stdout:
            return result.stdout.strip().split('\n')
        else:
            return []
    except subprocess.SubprocessError as e:
        logging.error(f"Error during search for {config}: {str(e)}")
        return []

def search_configs(search_root, configs=['postgresql.conf', 'pg_hba.conf', 'pg_ident.conf']):
    """Search for configurations using multiprocessing for speed improvement."""
    with Pool(processes=len(configs)) as pool:
        results = pool.starmap(find_config, [(config, search_root) for config in configs])
    return [path for sublist in results for path in sublist if path]
