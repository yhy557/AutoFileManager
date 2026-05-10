import argparse
import logging
import os
import shutil
from datetime import datetime
from utils.file_utils import open_file, write_file
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S',
    force=True
)

default_path = os.path.dirname(os.path.abspath(__file__))
backups_path = os.path.join(default_path, "backups.json")

defalt_json = {}

if not os.path.exists(backups_path):
    write_file(backups_path, defalt_json)
data = open_file(backups_path)

def _find_hierarchi(file_path: str) -> list[str]:
    logging.debug("--ORGANIZER IS STARTED--\n")
    path = Path(file_path)

    files = []
    for file in path.rglob('*'):
        if file.is_file():
            relative_path = file.relative_to(path)
            files.append(str(relative_path))
    logging.debug("FILES ARE(OLD):")
    for i in files:
        print(i)

    data[file_path] = {
        "time": str(datetime.now()),
        "folder_hierarchi": files
    }
    _make_and_move(path)
    write_file(backups_path, data)

images = [".jpg", ".png", ".gif"]
videos = [".mp4", ".mkv", ".avi"]
documents = [".pdf", ".docx", ".txt"]
codes = [".py", ".js", ".html"]
archives = [".zip", ".rar"]

def _make_and_move(path):
    images_path = os.path.join(path, "Images")
    videos_path = os.path.join(path, "Videos")
    documents_path = os.path.join(path, "documents")
    codes_path = os.path.join(path, "Codes")
    archives_path = os.path.join(path, "Archives")

    for file in path.iterdir():
        if file.is_file():
            extension = file.suffix
            if extension in images:
                os.makedirs(images_path, exist_ok=True)
                shutil.move(file, images_path)
            elif extension in videos:
                os.makedirs(videos_path, exist_ok=True)
                shutil.move(file, videos_path)
            elif extension in documents:
                os.makedirs(documents_path, exist_ok=True)
                shutil.move(file, documents_path)
            elif extension in codes:
                os.makedirs(codes_path, exist_ok=True)
                shutil.move(file, codes_path)
            elif extension in archives:
                os.makedirs(archives_path, exist_ok=True)
                shutil.move(file, archives_path)
    logging.debug("FILES ARE(NEW):")
    for file in path.rglob('*'):
        if file.is_file():
            relative_path = file.relative_to(path)
            print(str(relative_path))



parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str)
parser.add_argument("--watch", action="store_true")
parser.add_argument("--hierarchi")
args = parser.parse_args()

if args.watch:
    logging.debug("--AUTO ORGANIZER IS WORKING BACKGROUND NOW--")
    pass

if args.path:
    logging.debug("ARGS_PATH IS WORKING")
    _find_hierarchi(args.path)
