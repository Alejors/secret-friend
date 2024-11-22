import os
import boto3


class BucketClient:
  def __init__(self):
    self.url = os.environ.get("BUCKET_URL")
    self._client = boto3.client(
      's3',
      endpoint_url=self.url,
      aws_access_key_id=os.environ.get("BUCKET_ACCESS_KEY"),
      aws_secret_access_key=os.environ.get("BUCKET_SECRET_KEY")    
    )
    self._bucket = os.environ.get("BUCKET_NAME")
    
    if self._bucket not in self._get_buckets():
      self._client.create_bucket(Bucket=self._bucket)
      print("BUCKET CREATED...")
    else:
      print("BUCKET ALREADY EXISTS...")
    
  def _get_buckets(self):
    return self._client.list_buckets()
    
  def upload_file(self, file, user_id, bucket_name:str = None):
    object_name = f"{user_id}_{file.filename}"
    bucket = bucket_name or self._bucket
    try:
      self._client.upload_fileobj(file.stream, bucket, object_name, ExtraArgs={"ACL": "public-read"})
      return f"{self.url}/{bucket}/{object_name}?noAuth=true"
    except Exception as e:
      print(f"An error occurred: {e}")
      return None