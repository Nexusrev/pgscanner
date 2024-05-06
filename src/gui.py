import tkinter as tk
from tkinter import messagebox
from scanner import search_configs

def run_scan():
    search_root = entry.get()
    if not search_root:
        messagebox.showerror("Error", "Please enter a valid directory.")
        return
    results = search_configs(search_root)
    text_area.delete(1.0, tk.END)
    if results:
        text_area.insert(tk.END, "\n".join(results))
    else:
        text_area.insert(tk.END, "No configurations found.")

def setup_gui(root):
    global entry, text_area
    root.title("PostgreSQL Config Scanner")
    root.configure(bg='#333333')

    # Set the font
    custom_font = ('Consolas', 12)

    # Label
    label = tk.Label(root, text="Enter directory to scan:", bg='#333333', fg='lightgreen', font=custom_font)
    label.pack(pady=10)

    # Entry field
    entry = tk.Entry(root, font=custom_font, bg='black', fg='white', insertbackground='green')
    entry.pack(fill=tk.X, padx=20, pady=10)

    # Scan button
    scan_button = tk.Button(root, text="Scan", command=run_scan, font=custom_font, bg='black', fg='red')
    scan_button.pack(pady=10)

    # Text area for results
    text_area = tk.Text(root, height=15, font=custom_font, bg='black', fg='white')
    text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    setup_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
