import os
import shutil
from typing import Optional

class FileManager:
    STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
    
    @staticmethod
    def init_storage():
        if not os.path.exists(FileManager.STORAGE_DIR):
            os.makedirs(FileManager.STORAGE_DIR)

    @staticmethod
    def save_file(file_path): 
        """ Guarda archivo en almacenamiento """ 
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        
        FileManager.init_storage()
        filename = os.path.basename(file_path)
        dest_path = os.path.join(FileManager.STORAGE_DIR, filename)
        
        # Si el archivo ya está en storage, solo retornar la ruta
        if os.path.abspath(file_path) == os.path.abspath(dest_path):
            return dest_path
        
        # Si el archivo ya existe en destino, agregar número
        counter = 1
        original_dest = dest_path
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(FileManager.STORAGE_DIR, f"{name}_{counter}{ext}")
            counter += 1
        
        shutil.copy(file_path, dest_path) 
        return dest_path

    @staticmethod
    def delete_file(filename):
        """ Elimina archivo de almacenamiento """ 
        path = os.path.join(FileManager.STORAGE_DIR, filename) 
        if os.path.exists(path):
            os.remove(path) 
            return True 
        return False


    @staticmethod 
    def get_file_info(filename): 
        """ Obtiene información de un archivo """ 
        path = os.path.join(FileManager.STORAGE_DIR, filename) 
        if os.path.exists(path):
            size = os.path.getsize(path)  
            return {
                "name": filename,
                "size": size,
                "path": path
            }
        return None

    @staticmethod
    def list_files():
        """ Lista archivos en almacenamiento """ 
        FileManager.init_storage()
        return os.listdir(FileManager.STORAGE_DIR)

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extrae texto de diferentes tipos de archivos.
        Soporta: .txt, .md, .py, .json, .csv
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension in ['.txt', '.md', '.py']:
                return FileManager._extract_text_file(file_path)
            elif file_extension == '.json':
                return FileManager._extract_json_file(file_path)
            elif file_extension == '.csv':
                return FileManager._extract_csv_file(file_path)
            else:
                return f"[Archivo {file_extension}] Contenido no procesable directamente"
        except Exception as e:
            return f"Error extrayendo texto de {file_path}: {str(e)}"

    @staticmethod
    def _extract_text_file(file_path: str) -> str:
        """Extrae texto de archivos de texto plano"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _extract_json_file(file_path: str) -> str:
        """Extrae texto de archivos JSON"""
        import json
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return f"Contenido JSON: {json.dumps(data, indent=2, ensure_ascii=False)}"

    @staticmethod
    def _extract_csv_file(file_path: str) -> str:
        """Extrae texto de archivos CSV"""
        import csv
        content = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                content.append(" | ".join(row))
        return "Contenido CSV:\n" + "\n".join(content)

    @staticmethod
    def get_supported_extensions() -> list[str]:
        """Retorna las extensiones de archivo soportadas"""
        return ['.txt', '.md', '.py', '.json', '.csv', '.mp3', '.wav']