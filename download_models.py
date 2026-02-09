#!/usr/bin/env python3
"""
Script to download MediaPipe models required for video analysis.
"""

import os
import urllib.request
import sys


def download_file(url: str, dest_path: str) -> bool:
    """Download a file from URL to destination path."""
    try:
        print(f"Downloading {url}...")
        print(f"To: {dest_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Download with progress
        def report_hook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r{percent}% ({count * block_size}/{total_size} bytes)")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, dest_path, reporthook=report_hook)
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\nError downloading file: {e}")
        return False


def main():
    """Download all required models."""
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    # MediaPipe Pose Landmarker model
    model_url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
    model_path = os.path.join(models_dir, "pose_landmarker_lite.task")
    
    if os.path.exists(model_path):
        print(f"Model already exists: {model_path}")
    else:
        print("Downloading MediaPipe Pose Landmarker model...")
        if not download_file(model_url, model_path):
            print("Failed to download model. The application may not work without it.")
            print("You can manually download the model from:")
            print(model_url)
            print(f"And place it in: {model_path}")
            sys.exit(1)
    
    print("\nAll models downloaded successfully!")
    print(f"Models directory: {os.path.abspath(models_dir)}")


if __name__ == "__main__":
    main()
