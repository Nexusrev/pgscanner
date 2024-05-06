# src/gui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from scanner import search_configs  # Import the search_configs function

def run_scan_thread():
    """Handle the scan in a separate thread to keep the GUI responsive."""
    threading.Thread(target=run_scan).start()

def run_scan():
    search_root = entry.get()
    custom_configs = custom_entry.get().split(',') if custom_entry.get() else ['postgresql.conf', 'pg_hba.conf', 'pg_ident.conf']
    if not search_root:
        messagebox.showerror("Error", "Please enter a valid directory.")
        return
    progress_bar.start()
    results = search_configs(search_root, custom_configs)
    progress_bar.stop()
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, "\n".join(results) if results else "No configurations found.")

def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        messagebox.showinfo("Save", "Results saved successfully!")

def setup_gui(root):
    root.title("PostgreSQL Config Scanner")
    style = ttk.Style()
    style.theme_use('clam')  # Using a theme for a better look

    global entry, custom_entry, text_area, progress_bar
    ttk.Label(root, text="Enter directory to scan:").pack(pady=10)
    entry = ttk.Entry(root, width=50)
    entry.pack(pady=10)

    ttk.Label(root, text="Custom config names (comma separated):").pack(pady=10)
    custom_entry = ttk.Entry(root, width=50)
    custom_entry.pack(pady=10)

    scan_button = ttk.Button(root, text="Scan", command=run_scan_thread)
    scan_button.pack(pady=10)

    save_button = ttk.Button(root, text="Save Results", command=save_results)
    save_button.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
    progress_bar.pack(pady=10)

    text_area = tk.Text(root, height=15, width=60)
    text_area.pack(pady=10)

def main():
    root = tk.Tk()
    setup_gui(root)
    root.mainloop()
