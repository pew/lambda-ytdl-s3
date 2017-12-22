"""aws lambda function to download videos using youtube-dl to a S3 bucket.
use it for read/watch-it-later things or for archiving."""
import boto3
import youtube_dl
import os

# define s3 bucket
s3_bucket = os.environ.get('s3_bucket')

# define boto client
s3 = boto3.client('s3', region_name='us-east-1')

# define youtube-dl options
ytdl_options = {
    # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'outtmpl': '/tmp/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'cachedir': False
}


def download_file(video):
    ytdl = youtube_dl.YoutubeDL(ytdl_options)
    info = ytdl.extract_info(video, download=True)
    return ytdl.prepare_filename(info)


def s3_upload(filename):
    """upload file to s3"""
    print('uploading {} to s3'.format(filename))
    s3.upload_file(filename, s3_bucket, os.path.basename(filename))

    return True  # fix at some point


def lambda_handler(event, context):
    """aws lambda handler to down/upload files."""
    input_url = event
    filename = download_file(input_url)

    download_file(input_url)

    if download_file:
        upload = s3_upload(filename)  # trigger s3 upload
        if upload:
            return True

# invoke like this: "https://www.youtube.com/watch?v=oHg5SJYRHA0"
