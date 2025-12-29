import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import time
from collections import Counter

# ------------------ STATE ------------------
logging_enabled = True   # auto-start for submission
keystrokes = []
start_time = None
key_counter = Counter()

# ------------------ LOGIC ------------------
def normalize_key(event):
    if event.char and event.char.isprintable():
        return event.char
    return f"[{event.keysym}]"

def start_logging():
    global logging_enabled, start_time
    logging_enabled = True
    start_time = time.time()
    status.set("Logging: ON")

def stop_logging():
    global logging_enabled
    logging_enabled = False
    status.set("Logging: OFF")

def log_key(event):
    if not logging_enabled:
        return

    key = normalize_key(event)
    timestamp = datetime.now().strftime("%H:%M:%S")

    keystrokes.append((timestamp, key))
    key_counter[key] += 1

    log_box.insert(tk.END, f"{timestamp} : {key}\n")
    log_box.see(tk.END)

    update_stats()

def update_stats():
    total_keys.set(f"Total Keystrokes: {len(keystrokes)}")
    unique_keys.set(f"Unique Keystrokes: {len(key_counter)}")

    if start_time:
        minutes = max((time.time() - start_time) / 60, 0.01)
        wpm = int((len([k for _, k in keystrokes if len(k) == 1]) / 5) / minutes)
        typing_speed.set(f"Typing Speed: {wpm} WPM")

def save_log():
    with open("keystroke_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Key"])
        writer.writerows(keystrokes)

    with open("key_frequency.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Key", "Count"])
        for k, v in key_counter.items():
            writer.writerow([k, v])

    messagebox.showinfo("Saved", "Logs saved (keystroke_log.csv, key_frequency.csv)")

# ------------------ GUI ------------------
root = tk.Tk()
root.title("Keystroke Logging Demonstration")
root.geometry("760x500")

status = tk.StringVar(value="Logging: ON")
total_keys = tk.StringVar(value="Total Keystrokes: 0")
unique_keys = tk.StringVar(value="Unique Keystrokes: 0")
typing_speed = tk.StringVar(value="Typing Speed: 0 WPM")

tk.Label(
    root,
    text="Keystroke Logging Demonstration",
    font=("Arial", 15, "bold")
).pack(pady=6)

entry = tk.Entry(root, width=70)
entry.pack(pady=8)
entry.focus()
entry.bind("<Key>", log_key)

btns = tk.Frame(root)
btns.pack(pady=6)

ttk.Button(btns, text="Start", command=start_logging).pack(side="left", padx=5)
ttk.Button(btns, text="Stop", command=stop_logging).pack(side="left", padx=5)
ttk.Button(btns, text="Save Logs", command=save_log).pack(side="left", padx=5)

stats = tk.Frame(root)
stats.pack(pady=6)

tk.Label(stats, textvariable=status, fg="green").pack()
tk.Label(stats, textvariable=total_keys).pack()
tk.Label(stats, textvariable=unique_keys).pack()
tk.Label(stats, textvariable=typing_speed).pack()

log_box = tk.Text(root, height=14, width=90)
log_box.pack(pady=8)

start_logging()
root.mainloop()
