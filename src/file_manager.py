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
        """ Guarda archivo en almacenamiento """ 
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        FileManager.init_storage()
        filename = os.path.basename(file_path)
        dest_path  = os.path.join(FileManager.STORAGE_DIR, filename) 
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