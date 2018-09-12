import requests

token = ""


def get_token(key_file):
    # 1. Get your keys at https://stepik.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)3
    with open(key_file) as file:
        client_id = file.readline().strip()
        client_secret = file.readline().strip()

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


def get_course_page(course, page):
    api_url = 'https://stepik.org:443/api/lessons?page={}&course={}'.format(page, course)
    course_page = requests.get(api_url,
                               headers={'Authorization': 'Bearer ' + token}).json()
    return course_page


def get_comments_page(step, page, user_id, course):
    api_url = 'https://stepik.org/api/comments?page={}&target={}&user={}&course={}' \
        .format(page, step, user_id, course)
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


def get_certificate_grade(course, user_id):
    api_url = 'https://stepik.org/api/certificates?user={}'.format(user_id)
    certificates = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}).json()['certificates']
    id = -1
    for certificate in certificates:
        if certificate['course'] == course:
            id = certificate['id']
            break
    return id
