# limitations

First, you shouldn't use this project, it was just for testing and playing around with lambda and s3.

It's not really a good idea to download files using lambda since there's only a 500MB storage limit and all your ubuntu isos take up way more space.

Maybe there's a way to stream the files directly to S3, there probably is! But not in this project. Yet!

## install dependencies

in a virtualenv, please.

```shell
pip install -r requirements.txt
```

## package everything for lambda

lambda requires everything pre-packaged so it can be invoked quickly. boto3 is already provided by AWS.

example path on my mac, you'll see the path while executing `pip install`

```shell
cd ~/.pyenv/versions/3.6.3/envs/lambdas3/lib/python3.6/site-packages
zip -r9 ~/lambda-ytdl-s3/lambda-ytdl-s3.zip
```

now, add `app.py` to the zip as well (go into this folder again)

```shell
zip -g lambda-ytdl-s3.zip app.py
```

using tools like `zappa` or `serverless` will make this process way easier I guess.

## next steps

* upload the generated zip to s3
* create new lambda function
* use the s3 link for your `function code` (download from s3 URL)
* set the lambda `handler` to `app.lambda_handler`
* set an environment variable in lambda `S3_BUCKET` to your bucket name you want the videos to end up
* create an IAM role/policy so that the function is allowed to write into the S3 bucket
* create a `test` function in the lambda console and point it to a cool video to download it!
