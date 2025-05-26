from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
        self.UPLOAD_FOLDER = "documents"
        self.ALLOWED_EXTENSIONS = {'pdf'}
        self.MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
        
        # Rate limiting configs
        self.MAX_RPM = 15  # Requests per minute
        self.MAX_TPM = 1_000_000  # Tokens per minute
        self.MAX_RPD = 1_500  # Requests per day
