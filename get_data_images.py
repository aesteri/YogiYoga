import os
import requests
from tqdm import tqdm

output_dir = "yoga_images"
os.makedirs(output_dir, exist_ok=True)
metadata_dir = "Yoga-82/yoga_dataset_links"

def parse_metadata(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            pose, url = line.strip().split('\t')
            yield pose, url

def download_images(metadata_file, output_dir):
    for pose, url in parse_metadata(metadata_file):
        # create a folder for each pose
        pose_dir = os.path.join(output_dir, pose)
        os.makedirs(pose_dir, exist_ok=True)
        
        image_name = os.path.basename(url.split('?')[0])
        image_path = os.path.join(pose_dir, image_name)
        
        # download the image
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# this only processes first 2 metadata files rn
file_count = 0
for metadata_file in os.listdir(metadata_dir):
    if metadata_file.endswith(".txt"):
        print(f"Processing file: {metadata_file}")
        full_path = os.path.join(metadata_dir, metadata_file)
        download_images(full_path, output_dir)
        file_count += 1
        if file_count == 2:
            break