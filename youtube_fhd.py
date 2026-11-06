"""Interface de téléchargement YouTube jusqu'à 1080p."""
import queue
import shutil
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlsplit


def download(url, folder, events):
    def progress(info):
        if info["status"] == "downloading":
            total = info.get("total_bytes") or info.get("total_bytes_estimate")
            percent = min(100, 100 * info.get("downloaded_bytes", 0) / total) if total else 0
            stream = "Audio" if info["info_dict"].get("vcodec") == "none" else "Vidéo"
            events.put(("progress", (stream, percent)))
        elif info["status"] == "finished":
            events.put(("status", "Flux téléchargé. Préparation du fichier…"))

    try:
        from yt_dlp import YoutubeDL

        options = {
            "format": "bv[height<=1080]+ba/b[height<=1080]",
            "merge_output_format": "mp4",
            "paths": {"home": folder},
            "outtmpl": {"default": "%(title).120B [%(id)s].%(ext)s"},
            "windowsfilenames": True,
            "noplaylist": True,
            "overwrites": False,
            "quiet": True,
            "progress_hooks": [progress],
            "postprocessors": [{"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"}],
        }
        with YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=False)
            if info.get("_type") in {"playlist", "multi_video"}:
                raise ValueError("Colle le lien d'une seule vidéo.")
            info = downloader.process_ie_result(info, download=True)
        height = info.get("height")
        events.put(("done", f"Téléchargement terminé ({height}p)." if height else "Téléchargement terminé."))
    except ModuleNotFoundError as error:
        events.put(("error", f"Dépendance manquante ({error.name}). Installe yt-dlp[default]."))
    except Exception as error:
        events.put(("error", str(error)))


def main():
    root = tk.Tk()
    root.title("YouTube FHD")
    root.minsize(570, 280)
    frame = ttk.Frame(root, padding=22)
    frame.pack(fill="both", expand=True)
    frame.columnconfigure(0, weight=1)

    url = tk.StringVar()
    downloads = Path.home() / "Downloads"
    folder = tk.StringVar(value=str(downloads if downloads.is_dir() else Path.home()))
    status = tk.StringVar(value="Prêt")
    events = queue.Queue()

    def choose_folder():
        chosen = filedialog.askdirectory(initialdir=folder.get(), parent=root)
        if chosen:
            folder.set(chosen)

    def start():
        link = url.get().strip()
        try:
            parsed = urlsplit(link)
            host = parsed.hostname
        except ValueError:
            host = None
        if host not in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"} or parsed.scheme not in {"http", "https"}:
            messagebox.showerror("Lien invalide", "Colle un lien YouTube complet.", parent=root)
            return
        if parsed.path.rstrip("/") == "/playlist":
            messagebox.showerror("Lien invalide", "Colle le lien d’une seule vidéo.", parent=root)
            return
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            messagebox.showerror("FFmpeg manquant", "Installe FFmpeg puis relance l'application.", parent=root)
            return
        button.state(["disabled"])
        bar["value"] = 0
        status.set("Recherche de la vidéo…")
        threading.Thread(target=download, args=(link, folder.get(), events), daemon=True).start()
        root.after(120, poll)

    def poll():
        while not events.empty():
            kind, value = events.get_nowait()
            if kind == "progress":
                stream, percent = value
                bar["value"] = percent
                status.set(f"{stream} · {percent:.0f} %" if percent else f"{stream} · téléchargement…")
            elif kind == "status":
                status.set(value)
            else:
                button.state(["!disabled"])
                if kind == "done":
                    bar["value"] = 100
                    status.set(value)
                else:
                    bar["value"] = 0
                    status.set("Téléchargement interrompu.")
                    messagebox.showerror("Téléchargement", value, parent=root)
                return
        root.after(120, poll)

    def close():
        if not button.instate(["disabled"]) or messagebox.askyesno(
            "Quitter", "Interrompre le téléchargement et quitter ?", parent=root
        ):
            root.destroy()

    ttk.Label(frame, text="Télécharger une vidéo · Jusqu'à 1080p", font=("TkDefaultFont", 15, "bold")).grid(row=0, columnspan=2, sticky="w", pady=(0, 16))
    ttk.Label(frame, text="Lien YouTube").grid(row=1, sticky="w")
    entry = ttk.Entry(frame, textvariable=url)
    entry.grid(row=2, columnspan=2, sticky="ew", pady=(4, 12))
    ttk.Label(frame, text="Dossier de destination").grid(row=3, sticky="w")
    ttk.Entry(frame, textvariable=folder, state="readonly").grid(row=4, sticky="ew", pady=4)
    ttk.Button(frame, text="Parcourir…", command=choose_folder).grid(row=4, column=1, padx=(8, 0))
    button = ttk.Button(frame, text="Télécharger", command=start)
    button.grid(row=5, sticky="w", pady=12)
    bar = ttk.Progressbar(frame, maximum=100)
    bar.grid(row=6, columnspan=2, sticky="ew")
    ttk.Label(frame, textvariable=status).grid(row=7, columnspan=2, sticky="w", pady=(6, 0))
    root.protocol("WM_DELETE_WINDOW", close)
    entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
