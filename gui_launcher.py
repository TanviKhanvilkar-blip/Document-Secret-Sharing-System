# ==================== GUI LAUNCHER ====================
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import time  # Add this import

CHUNK_SIZE = 132  

def run_generator(input_file, output_dir, num_shares, threshold, output_text):
    try:
        start_time = time.time()  # Start timing
        result = subprocess.run(
            ["python", "part1_generator.py", input_file, output_dir, str(num_shares), str(threshold)],
            capture_output=True, text=True, encoding='utf-8'
        )
        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time  # Calculate elapsed time
        
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, f"\n\nTime taken: {elapsed_time:.2f} seconds")  # Display timing
        if result.stderr:
            output_text.insert(tk.END, "\nErrors:\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_reconstructor(input_dir, output_file, num_shares, threshold, output_text):
    try:
        start_time = time.time()  # Start timing
        result = subprocess.run(
            ["python", "part2_reconstructor.py", input_dir, output_file, str(num_shares), str(threshold)],
            capture_output=True, text=True, encoding='utf-8'
        )
        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time  # Calculate elapsed time
        
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, f"\n\nTime taken: {elapsed_time:.2f} seconds")  # Display timing
        if result.stderr:
            output_text.insert(tk.END, "\nErrors:\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_file(entry):
    path = filedialog.askopenfilename()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_dir(entry):
    path = filedialog.askdirectory()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def save_as_file(entry):
    path = filedialog.asksaveasfilename(defaultextension=".pdf")
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

# === GUI SETUP ===
root = tk.Tk()
root.title("Secret Sharing Tool")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# === TAB 1: Generator ===
gen_tab = tk.Frame(notebook)
notebook.add(gen_tab, text="Generate Shares")

tk.Label(gen_tab, text="Input File:").grid(row=0, column=0, sticky='e')
input_entry = tk.Entry(gen_tab, width=60)
input_entry.grid(row=0, column=1)
tk.Button(gen_tab, text="Browse", command=lambda: browse_file(input_entry)).grid(row=0, column=2)

tk.Label(gen_tab, text="Output Directory:").grid(row=1, column=0, sticky='e')
output_entry = tk.Entry(gen_tab, width=60)
output_entry.grid(row=1, column=1)
tk.Button(gen_tab, text="Browse", command=lambda: browse_dir(output_entry)).grid(row=1, column=2)

tk.Label(gen_tab, text="Num Shares:").grid(row=2, column=0, sticky='e')
shares_entry = tk.Entry(gen_tab)
shares_entry.grid(row=2, column=1, sticky='w')

tk.Label(gen_tab, text="Threshold:").grid(row=3, column=0, sticky='e')
threshold_entry = tk.Entry(gen_tab)
threshold_entry.grid(row=3, column=1, sticky='w')

gen_output = tk.Text(gen_tab, height=10)
gen_output.grid(row=5, column=0, columnspan=3, sticky='nsew')

tk.Button(gen_tab, text="Generate Shares", command=lambda: run_generator(
    input_entry.get(), output_entry.get(), int(shares_entry.get()), int(threshold_entry.get()), gen_output
)).grid(row=4, column=1)

# === TAB 2: Reconstructor ===
rec_tab = tk.Frame(notebook)
notebook.add(rec_tab, text="Reconstruct File")

tk.Label(rec_tab, text="Input Directory:").grid(row=0, column=0, sticky='e')
rec_input_entry = tk.Entry(rec_tab, width=60)
rec_input_entry.grid(row=0, column=1)
tk.Button(rec_tab, text="Browse", command=lambda: browse_dir(rec_input_entry)).grid(row=0, column=2)

tk.Label(rec_tab, text="Output File:").grid(row=1, column=0, sticky='e')
rec_output_entry = tk.Entry(rec_tab, width=60)
rec_output_entry.grid(row=1, column=1)
tk.Button(rec_tab, text="Browse", command=lambda: save_as_file(rec_output_entry)).grid(row=1, column=2)

tk.Label(rec_tab, text="Num Shares:").grid(row=2, column=0, sticky='e')
rec_shares_entry = tk.Entry(rec_tab)
rec_shares_entry.grid(row=2, column=1, sticky='w')

tk.Label(rec_tab, text="Threshold:").grid(row=3, column=0, sticky='e')
rec_threshold_entry = tk.Entry(rec_tab)
rec_threshold_entry.grid(row=3, column=1, sticky='w')

rec_output = tk.Text(rec_tab, height=10)
rec_output.grid(row=5, column=0, columnspan=3, sticky='nsew')

tk.Button(rec_tab, text="Reconstruct File", command=lambda: run_reconstructor(
    rec_input_entry.get(), rec_output_entry.get(), int(rec_shares_entry.get()), int(rec_threshold_entry.get()), rec_output
)).grid(row=4, column=1)

root.mainloop()