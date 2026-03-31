import csv
import os
import shutil
import sys
from pathlib import Path
from Utilities.logger_config import get_logger


logger = get_logger(__name__)
FIELDNAMES = [
    "attendance_id", "employee_id", "date", "check_in_time", "check_out_time",
    "status", "working_hours", "leave_type", "leave_reason"
]


def _resolve_storage_paths():
    if getattr(sys, "frozen", False):
        runtime_base = Path(sys.executable).resolve().parent
        bundled_base = Path(getattr(sys, "_MEIPASS", runtime_base))
    else:
        runtime_base = Path(__file__).resolve().parent
        bundled_base = runtime_base

    storage_dir = runtime_base / "storage"
    file_path = storage_dir / "attendance.csv"
    bundled_file = bundled_base / "storage" / "attendance.csv"
    return storage_dir, file_path, bundled_file


def _initialize_storage():
    storage_dir, file_path, bundled_file = _resolve_storage_paths()
    storage_dir.mkdir(parents=True, exist_ok=True)

    if file_path.exists():
        return file_path

    if bundled_file.exists() and bundled_file.resolve() != file_path.resolve():
        shutil.copyfile(bundled_file, file_path)
        logger.info(f"Initialized storage file from bundled data: {file_path}")
        return file_path

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
    logger.info(f"Created new storage file with headers: {file_path}")
    return file_path


FILE_PATH = _initialize_storage()
FILE_NAME = os.fspath(FILE_PATH)

def generate_attendance_id(data):
    if not data:
        return "ATT0001"
    
    max_num = 0
    for row in data:
        att_id = row.get("attendance_id", "")
        if att_id.startswith("ATT") and att_id[3:].isdigit():
            num = int(att_id[3:])
            if num > max_num:
                max_num = num
                
    if max_num > 0:
        return f"ATT{max_num + 1:04d}"
    
    return f"ATT{len(data) + 1:04d}"

def read_data():
    logger.info(f"Reading data from {FILE_NAME}")
    data = []
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        logger.debug(f"Successfully read {len(data)} records")
    except FileNotFoundError:
        logger.warning(f"{FILE_NAME} not found. Returning empty list.")
    except Exception as e:
        logger.error(f"Error reading data from {FILE_NAME}: {e}")
    return data

def write_data(data):
    logger.info(f"Writing {len(data)} records to {FILE_NAME}")
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(data)
        logger.debug(f"Successfully wrote {len(data)} records to {FILE_NAME}")
    except Exception as e:
        logger.error(f"Error writing data to {FILE_NAME}: {e}")
