import oss2
from config import BUCKET_API_ENDPOINT, BUCKET_NAME, BUCKET_API_KEY, BUCKET_API_SECRET
from pathlib import Path


def upload_to_oss(key: str, filename: str):
    auth = oss2.Auth(BUCKET_API_KEY, BUCKET_API_SECRET)
    bucket = oss2.Bucket(auth, BUCKET_API_ENDPOINT, BUCKET_NAME)
    bucket.put_object_from_file(key, filename)


def delete_file(filename: str):
    Path(filename).unlink()
