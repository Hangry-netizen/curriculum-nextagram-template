import boto3, botocore
import braintree
from app import app
from flask_login import current_user

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config.get("S3_KEY"),
    aws_secret_access_key=app.config.get("S3_SECRET")
)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config.get("BT_MERCHANT_ID"),
        public_key=app.config.get("BT_KEY"),
        private_key=app.config.get("BT_SECRET")
    )
)


def upload_file_to_s3(file, folder_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            app.config.get("S3_BUCKET"),
            f"{folder_name}/id_{current_user.id}/{file.filename}",
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    return f"{folder_name}/id_{current_user.id}/{file.filename}"


def get_client_token():
    return gateway.client_token.generate()

def create_transaction(amount, nonce):
  return gateway.transaction.sale({
    "amount": "10.00",
    "payment_method_nonce": nonce,
    "options": {
      "submit_for_settlement": True
    }
})
