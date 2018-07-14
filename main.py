import requests
import csv
import json
import argparse
from tqdm import tqdm


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

parser = argparse.ArgumentParser()
parser.add_argument("keys_file", help="File which contains your client_id and client_secret")
parser.add_argument("course_id", help="Id course for parsing", type=int)
parser.add_argument("--output_file", help="Id course for parsing")
args = parser.parse_args()

token = get_token(args.keys_file)

lessons = get_lessons(args.course_id)
output_file_path = 'comments'
if args.output_file:
    output_file_path = args.output_file

# output_file = open(output_file_path + ".txt", 'a', encoding='utf-8')

csv_output_file = csv.writer(open(output_file_path + ".csv", "a", encoding='utf-8'))

lessons_count = 0
for lesson in lessons:
    for step in lesson['steps']:
        lessons_count += 1

progress_bar = tqdm(total=lessons_count)

for lesson in lessons:
    for step in lesson['steps']:
        page_number = 0
        has_next_page = True
        while has_next_page:
            page_number += 1
            page = get_comments_page(step, page_number)
            has_next_page = page['meta']['has_next']

            for comment in page['comments']:
                #output_file.write(str(comment))
                csv_output_file.writerow(
                    [comment['id'],
                     comment['user'],
                     comment['text'],
                     comment['time'],
                     comment['last_time']])
        progress_bar.update(1)

progress_bar.close()