import sys
import os
import datetime
import traceback

LOG_FILE = os.path.expanduser("~/mmff/crash.log")

def log_error(exception):
    """Записывает ошибку в файл с датой и временем"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_msg = "".join(traceback.format_exception(None, exception, exception.__traceback__))
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*30}\n")
        f.write(f"CRASH REPORT: {timestamp}\n")
        f.write(f"{ '='*30}\n")
        f.write(error_msg)
        f.write("\n")
    
    return LOG_FILE

def install_handler():
    """Перехватывает системные ошибки"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        log_path = log_error(exc_value)
        print(f"\n\033[91m[CRITICAL ERROR] Программа упала!\nЛог записан в: {log_path}\033[0m")
        
    sys.excepthook = handle_exception
