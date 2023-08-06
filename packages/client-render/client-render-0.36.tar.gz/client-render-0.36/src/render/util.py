import requests

aws_url = "http://169.254.169.254/latest/user-data"


def load_user_data(url=aws_url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


user_data = load_user_data()
