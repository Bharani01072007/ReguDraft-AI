import os
import shutil
from typing import BinaryIO
from backend.config import settings

class S3Service:
    def __init__(self):
        # In a real environment, we would initialize boto3 client:
        # self.s3 = boto3.client(...)
        # For ease of testing and deployment, we'll store local files under a temp storage path 
        # when we run in local mock mode, and log the action.
        self.local_storage_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage_temp")
        os.makedirs(self.local_storage_dir, exist_ok=True)

    def upload_fileobj(self, file_obj: BinaryIO, object_name: str) -> str:
        """Uploads a file object to S3 or saves locally as a fallback"""
        # Local mock behavior
        target_path = os.path.join(self.local_storage_dir, object_name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, "wb") as f_out:
            shutil.copyfileobj(file_obj, f_out)
        
        # Return a simulated URL
        return f"{settings.BACKEND_URL}/static/storage/{object_name}"

    def upload_bytes(self, data: bytes, object_name: str) -> str:
        """Uploads bytes to S3 or saves locally as a fallback"""
        target_path = os.path.join(self.local_storage_dir, object_name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, "wb") as f_out:
            f_out.write(data)
            
        return f"{settings.BACKEND_URL}/static/storage/{object_name}"

    def get_presigned_url(self, object_name: str) -> str:
        """Generates a simulated link to access the object"""
        return f"{settings.BACKEND_URL}/static/storage/{object_name}"

s3_service = S3Service()
