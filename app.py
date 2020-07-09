"""aws lambda function to download videos using youtube-dl to a S3 bucket.
use it for read/watch-it-later things or for archiving."""
import boto3
import youtube_dl
import os

# define s3 bucket
s3_bucket = os.environ["S3_BUCKET"]
region = os.environ["AWS_REGION"]

# define boto client
s3 = boto3.client("s3", region_name=region)

# define youtube-dl options
ytdl_options = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "outtmpl": "/tmp/%(title)s.%(ext)s",
    "restrictfilenames": True,
    "cachedir": False,
}


def download_file(video):
    try:
        ytdl = youtube_dl.YoutubeDL(ytdl_options)
    except:
        raise
    info = ytdl.extract_info(video, download=True)
    return ytdl.prepare_filename(info)


def s3_upload(filename):
    """upload file to s3"""
    try:
        print("uploading {} to s3".format(filename))
        s3.upload_file(filename, s3_bucket, os.path.basename(filename))
    except:
        raise
    return True


def lambda_handler(event, context):
    """aws lambda handler to down/upload files."""
    input_url = event

    try:
        filename = download_file(input_url)
    except:
        raise
    try:
        upload = s3_upload(filename)  # trigger s3 upload
    except:
        raise

    return True


if __name__ == "__main__":
    lambda_handler("https://www.youtube.com/watch?v=7bXjWRXDFV8", None)
