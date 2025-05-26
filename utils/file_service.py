import os
from werkzeug.utils import secure_filename
from typing import Optional

class FileService:
    def __init__(self, upload_folder: str, allowed_extensions: set):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        os.makedirs(upload_folder, exist_ok=True)
        
    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
        
    def save_file(self, file, custom_filename: Optional[str] = None) -> str:
        if not file or not self.allowed_file(file.filename):
            raise ValueError("Invalid file type")
            
        filename = secure_filename(custom_filename or file.filename)
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        return filepath
