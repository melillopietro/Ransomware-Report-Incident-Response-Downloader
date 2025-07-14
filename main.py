
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import pandas as pd
import json
from ddgs import DDGS

top_gangs = [
    "LockBit", "Conti", "REvil", "Clop", "BlackCat", "Black Basta", "RansomHub", "PLAY", "Akira", "Hunters International",
    "DarkSide", "Maze", "Ryuk", "Hive", "NetWalker", "MountLocker", "Avaddon", "DoppelPaymer", "Vice Society", "Egregor",
    "Medusa", "SunCrypt", "Snatch", "Pysa", "Ragnar Locker", "HelloKitty", "Lorenz", "Everest", "NoEscape", "Trigona"
]

preferences_file = "gang_preferences.json"

def save_preferences(selected_gangs):
    with open(preferences_file, "w") as f:
        json.dump(selected_gangs, f)

def load_preferences():
    if os.path.exists(preferences_file):
        with open(preferences_file, "r") as f:
            return json.load(f)
    return []

def fetch_links(engine, query, max_results=50):
    if engine == "DuckDuckGo":
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            return [r['href'] for r in results if 'href' in r and r['href']]
    else:
        raise NotImplementedError(f"Search engine '{engine}' is not supported.")

def download_pdfs(engine, query, year, gang, category, max_results, download_dir, summary, progress_label, total, count):
    output_dir = os.path.join(download_dir, str(year), gang, category)
    os.makedirs(output_dir, exist_ok=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        links = fetch_links(engine, query, max_results)
    except NotImplementedError as e:
        messagebox.showerror("Motore di ricerca non supportato", str(e))
        return 0

    for url in links:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if "html" in content_type:
                    continue

                ext = os.path.splitext(url)[-1].lower()
                if not ext or len(ext) > 5 or any(x in ext for x in ['?', '&', '=']):
                    ext = ".pdf"
                filename = f"{year}_{gang.replace(' ', '_')}_{category}_{count[0]+1}{ext}"
                filepath = os.path.join(output_dir, filename)

                if os.path.exists(filepath):
                    continue

                with open(filepath, "wb") as f:
                    f.write(response.content)

                summary.append({
                    "Anno": year,
                    "Gang": gang,
                    "Tipologia": category,
                    "Link": url,
                    "Nome File": filename
                })

                count[0] += 1
                progress_label.config(text=f"Download completati: {count[0]} / {total} ({(count[0]/total)*100:.1f}%)")
                progress_label.update_idletasks()

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Errore scaricando {url}: {e}")
            continue

        if count[0] >= total:
            break

def start_download():
    try:
        selected_engine = engine_var.get()
        selected_gangs = [g for g, var in gang_vars.items() if var.get()]
        selected_categories = [cat for cat, var in category_vars.items() if var.get()]

        if not selected_gangs or not selected_categories:
            messagebox.showerror("Errore", "Seleziona almeno una gang e una categoria.")
            return

        save_preferences(selected_gangs)

        directory = filedialog.askdirectory()
        if not directory:
            return

        total = len(selected_gangs) * len(selected_categories) * 5
        count = [0]
        summary = []
        for year in range(2020, 2025):
            for gang in selected_gangs:
                for category in selected_categories:
                    if category == "Report":
                        query = f"{gang} ransomware report whitepaper analysis {year}"
                    elif category == "Incident Response":
                        query = f"{gang} ransomware incident response IR case study forensics {year}"
                    download_pdfs(selected_engine, query, year, gang, category, 50, directory, summary, progress_label, total, count)

        df = pd.DataFrame(summary)
        df.to_excel(os.path.join(directory, "report_summary.xlsx"), index=False)
        messagebox.showinfo("Completato", f"Totale report scaricati: {len(summary)}")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

# GUI
root = tk.Tk()
root.title("Ransomware Report & IR Downloader")
root.geometry("850x800")

tk.Label(root, text="Motore di ricerca:").pack()
engine_var = tk.StringVar(value="DuckDuckGo")
tk.OptionMenu(root, engine_var, "DuckDuckGo").pack()

tk.Label(root, text="Tipologia da cercare:").pack()
category_vars = {cat: tk.BooleanVar(value=True) for cat in ["Report", "Incident Response"]}
for cat, cat_var in category_vars.items():
    tk.Checkbutton(root, text=cat, variable=cat_var).pack(anchor="w")

tk.Label(root, text="Seleziona le gang ransomware:").pack()

canvas = tk.Canvas(root, height=250)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas)
scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

gang_vars = {}
stored = load_preferences()
for gang in top_gangs:
    var = tk.BooleanVar(value=(gang in stored))
    gang_vars[gang] = var
    tk.Checkbutton(scroll_frame, text=gang, variable=var).pack(anchor="w", padx=5)

progress_label = tk.Label(root, text="Download non avviato.")
progress_label.pack(pady=5)

tk.Button(root, text="Avvia download", command=start_download, bg="green", fg="white").pack(pady=10)

root.mainloop()
