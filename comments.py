import argparse
import csv

from tqdm import tqdm

import util_functions

parsed_users = {}

parser = argparse.ArgumentParser()
parser.add_argument("keys_file", help="File which contains your client_id and client_secret")
parser.add_argument("course_id", help="Id course for parsing", type=int)
parser.add_argument("--user_id", help="User id, if you want to get comments from the user")
parser.add_argument("--output_file", help="Output file")
parser.add_argument("--fields", help="File with fields, which needed from comments")
args = parser.parse_args()

util_functions.get_token(args.keys_file)

course_id = args.course_id
lessons = util_functions.get_lessons(course_id)

user = ""
if args.user_id:
    user = args.user_id

output_file_path = 'comments'
if args.output_file:
    output_file_path = args.output_file

fields = ['id', 'parent', 'user',
          'user_role', 'time', 'last_time',
          'text', 'reply_count', 'is_deleted',
          'deleted_by', 'deleted_at', 'can_edit',
          'can_moderate', 'can_delete', 'actions',
          'target', 'replies', 'subscriptions',
          'is_pinned', 'pinned_by', 'pinned_at',
          'is_staff_replied', 'is_reported', 'attachments',
          'thread', 'submission', 'edited_by',
          'edited_at', 'epic_count', 'abuse_count',
          'vote', 'translations', 'certificate']

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
            page = util_functions.get_comments_page(step, page_number, user, course_id)
            has_next_page = page['meta']['has_next']

            for comment in page['comments']:
                if 'certificate' in fields:
                    comment_user_id = comment['user']
                    if comment_user_id in parsed_users:
                        comment['certificate'] = parsed_users[comment_user_id]
                    else:
                        certificate_id = util_functions.get_certificate_grade(course_id, comment_user_id)
                        comment['certificate'] = certificate_id
                        parsed_users[comment_user_id] = certificate_id

                csv_output_file.writerow([str(comment[field]).replace('\n', "") for field in fields])

        progress_bar.update(1)

progress_bar.close()