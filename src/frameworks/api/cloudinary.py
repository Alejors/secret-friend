import os
import time
import hashlib
import requests


class CloudinaryUploader:
  def __init__(self):
    self._api_key = os.environ.get("CLOUDINARY_API_KEY")
    self._api_secret = os.environ.get("CLOUDINARY_SECRET")
    self._url = f"https://api.cloudinary.com/v1_1/{os.environ.get('CLOUDINARY_NAME')}/image/upload"
    
  def upload(self, file):
    timestamp = time.time()
    upload_data = {
      "timestamp": int(timestamp),
      "file": file,
      "api_key": self._api_key,
      "signature": self._get_signature({"timestamp": int(timestamp)})
    }
    
    upload_result = requests.post(self._url, data=upload_data)
    
    return upload_result["secure_url"]
  
  def _get_signature(self, data: dict):
    # se genera una lista de tuplas ordenadas alfabéticamente
    sorted_params = sorted(data.items())
    concatenated_params = "&".join([f"{key}={value}" for key, value in sorted_params])
    final_string = concatenated_params + self._api_secret
    
    return hashlib.sha1(final_string.encode('utf-8')).hexdigest()