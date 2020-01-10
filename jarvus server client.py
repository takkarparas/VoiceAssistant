from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="tablet-gtamwu-2f9cc58f7ebf.json"
storage_client = storage.Client()
buckets = list(storage_client.list_buckets())
print(buckets)
