import os
import sys
from minio import Minio

minio_client = Minio(
    "127.0.0.1:9000",
    access_key="sicilius_admin",
    secret_key="sicilius_secret_2024",
    secure=False
)

bucket = "company-gazettes"

try:
    if not minio_client.bucket_exists(bucket):
        print("Bucket does not exist yet (Scraper is probably still loading pages).")
        sys.exit(0)
        
    objects = list(minio_client.list_objects(bucket, recursive=True))
    if not objects:
        print("No files found in bucket.")
        sys.exit(0)
    
    files = objects[:10]
    out_dir = "/Users/turgaykirkil/Apps/TSG_Platform/sicilius/backend/test_eval_downloads"
    os.makedirs(out_dir, exist_ok=True)
    
    for obj in files:
        if not obj.object_name.endswith('.pdf'): continue
        fname = os.path.basename(obj.object_name)
        out_path = os.path.join(out_dir, fname)
        print(f"Downloading {obj.object_name} to {out_path}...")
        minio_client.fget_object(bucket, obj.object_name, out_path)
        
    print("Download complete.")
except Exception as e:
    print(f"Error: {e}")
