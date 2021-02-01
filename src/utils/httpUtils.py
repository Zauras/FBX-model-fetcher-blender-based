import requests, io

from typing import List


def getSession():
    return requests.session()


def downloadContentFromUrlList(url_list: List[str]) -> List[io.BytesIO]:
    session = getSession()
    print("open session")

    responses_content_list: List[io.BytesIO] = []

    for file_number, file_url in enumerate(url_list, start=1):
        print(f"iteration: {file_number}")

        response = session.get(file_url)
        print(f"...Downloading file {file_number} from ===> {file_url}")

        if not response.ok:
            print(f"Sorry, could not download file from url: {file_url}")
            continue

        # read zip file binary:
        print("reading content from response")
        responses_content_list.append(io.BytesIO(response.content))

    print("close session")
    session.close()
    return responses_content_list
