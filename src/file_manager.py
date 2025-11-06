import os
import shutil

class FileManager:
    STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
    
    @staticmethod
    def init_storage():
        if not os.path.exists(FileManager.STORAGE_DIR):
            os.makedirs(FileManager.STORAGE_DIR)

    @staticmethod
    def save_file(file_path): 
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        
        FileManager.init_storage()
        filename = os.path.basename(file_path)
        dest_path = os.path.join(FileManager.STORAGE_DIR, filename)
        
        if os.path.abspath(file_path) == os.path.abspath(dest_path):
            return dest_path
        
        counter = 1
        original_dest = dest_path
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(FileManager.STORAGE_DIR, f"{name}_{counter}{ext}")
            counter = counter + 1
        
        shutil.copy(file_path, dest_path) 
        return dest_path

    @staticmethod
    def delete_file(filename):
        try:
            path = os.path.join(FileManager.STORAGE_DIR, filename)
            
            if not os.path.exists(path):
                print(f"El archivo '{filename}' no existe.")
                return False
            
            if not os.path.isfile(path):
                print(f"'{filename}' no es un archivo valido.")
                return False
            
            os.remove(path)
            print(f"Archivo '{filename}' eliminado.")
            return True
            
        except:
            print(f"Error al eliminar '{filename}'")
            return False

    @staticmethod 
    def get_file_info(filename):
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
        FileManager.init_storage()
        return os.listdir(FileManager.STORAGE_DIR)

    @staticmethod
    def extract_text(file_path):
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
        except:
            return f"Error extrayendo texto de {file_path}"

    @staticmethod
    def _extract_text_file(file_path):
        file = open(file_path, 'r', encoding='utf-8')
        texto = file.read()
        file.close()
        return texto

    @staticmethod
    def _extract_json_file(file_path):
        import json
        file = open(file_path, 'r', encoding='utf-8')
        data = json.load(file)
        file.close()
        return f"Contenido JSON: {json.dumps(data, indent=2, ensure_ascii=False)}"

    @staticmethod
    def _extract_csv_file(file_path):
        import csv
        content = []
        file = open(file_path, 'r', encoding='utf-8')
        reader = csv.reader(file)
        for row in reader:
            content.append(" | ".join(row))
        file.close()
        return "Contenido CSV:\n" + "\n".join(content)

    @staticmethod
    def get_supported_extensions():
        return ['.txt', '.md', '.py', '.json', '.csv', '.mp3', '.wav']