import os
import boto3


class BucketClient:
  def __init__(self):
    self.url = os.environ.get("BUCKET_URL")
    self._region = os.environ.get("AWS_REGION")
    self._client = boto3.client(
      's3',
      aws_access_key_id=os.environ.get("BUCKET_ACCESS_KEY"),
      aws_secret_access_key=os.environ.get("BUCKET_SECRET_KEY"),
      region_name=self._region
    )
    self._bucket = os.environ.get("BUCKET_NAME")
    self._check_bucket()
  
  def _check_bucket(self):
    if self._bucket not in self._get_buckets():
      self._client.create_bucket(Bucket=self._bucket)
      print("BUCKET CREATED...")
    else:
      print("BUCKET ALREADY EXISTS...")

  def _get_buckets(self):
    response = self._client.list_buckets().get("Buckets")
    if response:
      buckets = [bucket["Name"] for bucket in self._client.list_buckets().get("Buckets")]
    else:
      buckets = []
    return buckets
    
  def upload_file(self, file, user_id, folder:str = None):
    object_name = f"{folder}/{user_id}_{file.filename}"
    try:
      self._client.upload_fileobj(
        file.stream,
        self._bucket,
        object_name,
        ExtraArgs={"ContentType": "image/jpeg"})

      if os.environ.get("ENVIRONMENT") == "local":
        return f"{self.url.replace("ninja", "localhost")}{object_name}?noAuth=true"
      else:
        return f"{self.url}{object_name}"
    except Exception as e:
      print(f"An error occurred: {e}")
      return None