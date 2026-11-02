import os
import ctypes
from pathlib import Path

# Путь к папке с nvidia библиотеками в вашем venv
nvidia_root = Path(r"C:\myRAG\venv\Lib\site-packages\nvidia") 

# Порядок загрузки: сначала runtime, потом cublas, потом остальное
# Для CUDA 13 имена файлов содержат _13
preload_order = [
    "cudart64_13.dll",
    "cublasLt64_13.dll",
    "cublas64_13.dll",
]

for dll_name in preload_order:
    # Ищем файл во всех подпапках nvidia
    for dll_path in nvidia_root.rglob(dll_name):
        try:
            # Загружаем с флагом по умолчанию, чтобы сработал add_dll_directory
            ctypes.CDLL(str(dll_path))
            print(f"Preloaded: {dll_path}") 
            break
        except OSError as e:
            print(f"Failed to load {dll_path}: {e}")

