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
