import os
from dotenv import load_dotenv
import braintree


class Config(object):

    S3_BUCKET                 = os.environ.get("S3_BUCKET")
    S3_KEY                    = os.environ.get("S3_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY") 
    S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(os.environ.get("S3_BUCKET"))
    SECRET_KEY                = os.urandom(32)
    DEBUG                     = True
    PORT                      = 5000



gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)