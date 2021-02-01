import requests, io

from typing import List


def getSession():
    return requests.session()


def downloadContentFromUrlList(url_list: List[str]) -> List[io.BytesIO]:
    print("\n################# Downloading ###############################")
    print("open session")
    session = getSession()

    responses_content_list: List[io.BytesIO] = []

    for file_number, file_url in enumerate(url_list, start=1):
        print(f"\niteration: {file_number}")
        print(f"...Downloading file {file_number} from ===> {file_url}")
        response = session.get(file_url)

        if not response.ok:
            print(f"Sorry, could not download file from url: {file_url}")
            continue

        # read zip file binary:
        print("\nReading content from response")
        try:
            responses_content_list.append(io.BytesIO(response.content))
        except:
            print("Failed to read content from response")

    print("close session")
    session.close()
    return responses_content_list
