import json
import urllib.request as request

aws_url = "http://169.254.169.254/latest/user-data"


def load_user_data(url=aws_url):
    with request.urlopen(url) as req:
        if req.status != 200:
            raise ValueError("User data is incorrect")
        content = req.read()
        return json.loads(content)


user_data = load_user_data()
assert user_data.get('aws_access_key_id'), "aws_access_key_id must be defined"
assert user_data.get('aws_secret_access_key'), "aws_secret_access_key must be defined"
assert user_data.get('aws_endpoint'), "aws_endpoint must be defined"
assert user_data.get('aws_bucket'), "aws_bucket must be defined"
assert user_data.get('instance_s3_key'), "instance_s3_key must be defined"
