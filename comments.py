import argparse
import csv
import requests
from tqdm import tqdm

import util_functions


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


parser = argparse.ArgumentParser()
parser.add_argument("keys_file", help="File which contains your client_id and client_secret")
parser.add_argument("course_id", help="Id course for parsing", type=int)
parser.add_argument("--output_file", help="output file")
parser.add_argument("--fields", help="File with fields, which needed from comments")
args = parser.parse_args()

token = util_functions.get_token(args.keys_file)

lessons = get_lessons(args.course_id)
output_file_path = 'comments'
if args.output_file:
    output_file_path = args.output_file

fields = ['id', 'user', 'text', 'time', 'last_time']
if args.fields:
    fields.clear()
    with open(args.fields) as file:
        fields = [line.rstrip('\n') for line in file]

csv_output_file = csv.writer(open(output_file_path + ".csv", "a", encoding='utf-8'), dialect='excel-tab')
csv_output_file.writerow(fields)

lessons_count = 0
for lesson in lessons:
    for step in lesson['steps']:
        lessons_count += 1
print("Parsing commentary pages...")
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
                if 'text' in fields:
                    comment['text'] = str(comment['text']).replace('\n',"")
                csv_output_file.writerow([comment[field] for field in fields])

        progress_bar.update(1)

progress_bar.close()
