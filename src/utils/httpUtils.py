import requests


def getSession():
    return requests.session()


# TODO: working incorrectly
def check_if_downloadable(url):
    headers = requests.head(url).headers
    is_downloadable = 'attachment' in headers.get('Content-Disposition', '')
    return is_downloadable
