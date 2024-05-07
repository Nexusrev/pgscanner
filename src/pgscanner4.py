import os
import time
import logging
from multiprocessing import Pool
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.logging import RichHandler

# Create a console object for rich output
console = Console()

# ASCII Art for pgscanner
PGSCANNER_LOGO = """
██████╗ ██████╗  ██████╗ ████████╗ █████╗ ███╗   ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔══██╗████╗  ██║██╔════╝██╔══██╗
██████╔╝██████╔╝██║   ██║   ██║   ███████║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██╔══██╗██║   ██║   ██║   ██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╔╝   ██║   ██║  ██║██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""

# Setup logging to file with RichHandler for better terminal output
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)

def find_config(config, search_root, progress, task_id):
    """Tailored search for PostgreSQL config files using os.walk(), with performance logging."""
    start_time = time.time()
    found_files = []
    for root, dirs, files in os.walk(search_root):
        for file in files:
            if config in file:
                full_path = os.path.join(root, file)
                found_files.append(full_path)
                logging.info(f"Found {config}: {full_path}")
                progress.advance(task_id)
    elapsed_time = time.time() - start_time
    logging.info(f"Scanned {len(found_files)} files for {config} in {elapsed_time:.2f} seconds")
    return found_files

def search_configs(search_root, configs):
    """Search configurations using multiprocessing, updating a progress bar."""
    total_files = sum([len(files) for _, _, files in os.walk(search_root)])
    with Progress(console=console) as progress:
        task_id = progress.add_task("[cyan]Scanning...", total=total_files)
        with Pool(processes=len(configs)) as pool:
            results = pool.starmap(find_config, [(config, search_root, progress, task_id) for config in configs])
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
    
    console.print(PGSCANNER_LOGO, style="bold green")
    console.print("Starting pgscanner...\n", style="bold yellow")
    
    found_configs = search_configs(args.path, args.configs)
    
    if found_configs:
        console.print("Found configuration files:", style="bold green")
        for config in found_configs:
            console.print(config, style="bold cyan")
    else:
        console.print("No configuration files found.", style="bold red")

if __name__ == "__main__":
    main()
