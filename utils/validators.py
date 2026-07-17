import re
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class Validator:
    """Validates input data and files."""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain number"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain special character"
        return True, ""
    
    @staticmethod
    def validate_project_name(name: str) -> Tuple[bool, str]:
        """Validate project name."""
        if not name or len(name) < 3:
            return False, "Project name must be at least 3 characters"
        if len(name) > 255:
            return False, "Project name must not exceed 255 characters"
        if not re.match(r'^[a-zA-Z0-9\s\-_.()\']+$', name):
            return False, "Project name contains invalid characters"
        return True, ""
    
    @staticmethod
    def validate_file(file) -> Tuple[bool, str]:
        """Validate uploaded file."""
        from config.settings import get_settings
        settings = get_settings()
        
        if not file:
            return False, "No file provided"
        
        # Check file size
        file_size = len(file.getbuffer()) if hasattr(file, 'getbuffer') else file.size
        max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
        if file_size > max_bytes:
            return False, f"File size exceeds {settings.MAX_UPLOAD_MB}MB limit"
        
        # Check file type
        file_ext = Path(file.name).suffix.lower() if hasattr(file, 'name') else ''
        if file_ext not in settings.SUPPORTED_FORMATS:
            return False, f"Unsupported file format: {file_ext}"
        
        return True, ""
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
        """Validate GPS coordinates."""
        if not -90 <= latitude <= 90:
            return False, "Invalid latitude"
        if not -180 <= longitude <= 180:
            return False, "Invalid longitude"
        return True, ""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage."""
        # Remove special characters
        filename = re.sub(r'[^\w\s.-]', '', filename)
        # Replace spaces with underscores
        filename = re.sub(r'\s+', '_', filename)
        # Remove multiple dots
        filename = re.sub(r'\.+', '.', filename)
        return filename
