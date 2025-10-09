# Simple Video Downloader
# This program asks for a URL and downloads the video in the lowest quality

import yt_dlp
import os

def download_video():
    """Downloads a video from a URL in the lowest quality"""
    
    # Ask the user for the URL
    print("Welcome to the Simple Video Downloader!")
    print("This program will download videos in the lowest quality to save space.")
    print()
    
    url = input("Please enter the video URL: ").strip()
    
    # Check if URL is not empty
    if not url:
        print("Error: Please enter a valid URL.")
        return
    
    # Configure yt-dlp to download in lowest quality
    ydl_opts = {
        'format': 'worst',  # Downloads the worst/lowest quality
        'outtmpl': '%(title)s.%(ext)s',  # Output filename format
    }
    
    try:
        print(f"Starting download from: {url}")
        print("This might take a few moments...")
        
        # Create yt-dlp object and download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Download completed successfully!")
        print("The video has been saved to your current folder.")
        
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        print("Please check that the URL is correct and try again.")

if __name__ == "__main__":
    download_video()
