import requests
import json


def get_token():
    # 1. Get your keys at https://stepik.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)
    client_id = "FuWvulYVOGKp4lXRKTASUDdIs4D7Xlwl5IqxAaQ6"
    client_secret = "3GAUQ3fwwm37oieh95dm0duaImHupHnezwexlFBO5p62DMlhfY1mFRX6W0nJh8L4hFaFg3V7TxkC2wX7np3ytV0FifkrHm5I7X6rM45PJ9pTA4MdpXGxOjTa1LicUNUI"

    # 2. Get a token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        print('Unable to authorize with provided credentials')
        exit(1)
    return token


token = get_token()


def get_course_page(course, page):
    api_url = 'https://stepik.org:443/api/lessons?page={}&course={}'.format(page, course)
    course_page = requests.get(api_url,
                               headers={'Authorization': 'Bearer ' + token}).json()
    return course_page


def get_comments_page(step, page):
    api_url = 'https://stepik.org:443/api/comments?page={}&target={}'.format(page, step)
    comments_page = requests.get(api_url,
                                 headers={'Authorization': 'Bearer ' + token}).json()
    return comments_page


def get_lessons(course):
    page_number = 0
    has_next_lessons_page = True
    list_of_lessons = []

    while has_next_lessons_page:
        page_number += 1
        page_content = get_course_page(course, page_number)
        has_next_lessons_page = page_content['meta']['has_next']

        for lesson in page_content['lessons']:
            list_of_lessons.append(lesson)
    return list_of_lessons


# course_number = input()
# # 3. Call API (https://stepik.org/api/docs/) using this token.
# api_url = 'https://stepik.org:443/api/lessons?course={}'.format(course_number)

lessons = get_lessons(3678)
comments_list = []

for lesson in lessons:
    for step in lesson['steps']:
        page_number = 0
        has_next_page = True
        while has_next_page:
            page_number += 1
            page = get_comments_page(step, page_number)
            has_next_page = page['meta']['has_next']

            for comment in page['comments']:
                comments_list.append(comment)

f = open('comments.txt', 'a', encoding='utf8')
for comment in comments_list:
    print(comment)
    f.write(json.dumps(comment))

# print(list_of_lessons)
