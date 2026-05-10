import os
import json

#We are opening files with secure method
def json_read_file(file_path: any):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def json_write_file(file_path: any, data: dict | str | int | None):
    temp_file = file_path + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_file, file_path)






















"""import os
import json

#We are opening files with secure method
def open_file(file_path: any):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    return data

def write_file(file_path: any, data: dict | str | int | None):
    temp_file = file_path + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(str(data) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_file, file_path)

def append_file(file_path: any, data: dict | str | int | None):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + str(data))"""