import boto3, botocore
from app.config import Config
from app import app 
import os
from dotenv import load_dotenv
import braintree
from app.config import gateway
from authlib.flask.client import OAuth
import app.config


s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get("S3_KEY"),
   aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:
       s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type
        }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(Config.S3_LOCATION, file.filename)

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)

def allowed_images(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ['jpg', 'pgn', 'jpeg']

def delete_file_from_s3(file, bucket_name, acl="public-read"):
    pass


oauth = OAuth()

oauth.register('google',
    client_id= os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret= os.environ.get("GOOGLE_SECRET_CLIENT"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)


# def validation_preparation(func):
#     def wrapper(obj, key, value):
#         try:
#             obj.validation_errors
#         except AttributeError:
#             obj.validation_errors = []
#         return func(obj, key, value)

#     return wrapper