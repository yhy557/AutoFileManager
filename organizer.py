import argparse
import logging
import shutil
import signal
import time
import os
from datetime import datetime
from pathlib import Path
from utils.file_utils import json_read_file, json_write_file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))
BACKUPS_PATH = os.path.join(DEFAULT_PATH, "backups.json")
LOGS_PATH = os.path.join(DEFAULT_PATH, "AutoFileManager.log")


class WatchFile:
    def __init__(self, folder_path, data):
        self.path = Path(folder_path)
        self.observer = Observer()
        self.data = data

    def run(self):
        self.event_handler = Handler(self.path, self.data)
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        logging.debug("Observer running. Press Ctrl+C to stop.")
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, folder_path, data):
        super().__init__()
        self.folder_path = Path(folder_path)
        self.data = data

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == "created":
            self.find_hierarchi()
        elif event.event_type == "deleted":
            path = Path(event.src_path)
            logging.debug(f"FOR NOW: {path}")
            main_folder = list(path.parts)
            deleted_file_path = Path(*main_folder[:-1])
            file_count = 0
            with os.scandir(deleted_file_path) as it:
                for entry in it:
                    if entry.is_file():
                        file_count += 1
            if file_count <= 0:
                try:
                    logging.debug(f"FOLDER IS DELETING: {deleted_file_path}")
                    deleted_file_path.rmdir()
                except Exception as e:
                    logging.debug(f"ERROR: {e}")

    def find_hierarchi(self) -> list[str]:
        """
        In here, we are getting files in the folder
        """
        logging.debug("--ORGANIZER IS STARTED--\n")
        path = Path(self.folder_path)

        files = []
        for file in path.rglob("*"):
            if file.is_file():
                relative_path = file.relative_to(path)
                files.append(str(relative_path))
        logging.debug("FILES ARE(OLD):")
        for i in files:
            logging.debug(i)

        self.data[str(self.folder_path)] = {
            "time": str(datetime.now()),
            "folder_hierarchi": files,
        }
        self._make_and_move()
        json_write_file(BACKUPS_PATH, self.data)

    def _make_and_move(self):
        """
        In here, we are creating folder and moving added file into folder
        """
        extensions = {
            (".jpg", ".png", ".gif"): self.folder_path / "Images",
            (".mp4", ".mkv", ".avi"): self.folder_path / "Videos",
            (".pdf", ".docx", ".txt"): self.folder_path / "documents",
            (".py", ".js", ".html"): self.folder_path / "Codes",
            (".zip", ".rar"): self.folder_path / "Archives",
        }

        for file in self.folder_path.iterdir():
            if not file.is_file():
                continue
            extension = file.suffix
            for key, values in extensions.items():
                if extension in key:
                    os.makedirs(values, exist_ok=True)
                    try:
                        shutil.move(file, values)
                    except shutil.Error as e:
                        logging.debug(f"Destination path is already exists: {e}")

        logging.debug("FILES ARE(NEW):")
        for file in self.folder_path.rglob("*"):
            if file.is_file():
                relative_path = file.relative_to(self.folder_path)
                logging.debug(str(relative_path))


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )

    defalt_json = {}

    if not os.path.exists(BACKUPS_PATH):
        json_write_file(BACKUPS_PATH, defalt_json)
    data = json_read_file(BACKUPS_PATH)

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--logs", action="store_true")
    args = parser.parse_args()

    if args.logs:
        logging.basicConfig(
            filename=LOGS_PATH,
            level=logging.DEBUG,
            format="%(asctime)s - [%(levelname)s] - %(message)s",
            datefmt="%H:%M:%S",
            force=True,
        )

    if args.watch:
        logging.debug("--AUTO ORGANIZER IS WORKING BACKGROUND NOW--")
        WatchFile(args.path, data).run()
    else:
        Handler(args.path, data).find_hierarchi()


if __name__ == "__main__":
    main()
