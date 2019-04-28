import argparse
import csv

import requests

from stepic_util import util_functions

parser = argparse.ArgumentParser()
parser.add_argument("keys_file", help="File which contains your client_id and client_secret")
parser.add_argument("user_id", help="User id, if you want to get comments from the user")
parser.add_argument("--output_file", help="Output file")
args = parser.parse_args()
token = util_functions.get_token(args.keys_file)

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
          'vote', 'translations']
output_file_path = 'abuse_comments3'
if args.output_file:
    output_file_path = args.output_file

csv_output_file = csv.writer(open(output_file_path + ".csv", "a", encoding='utf-8'), dialect='excel-tab')
csv_output_file.writerow(fields)

page_number = 0

while True:
    page_number += 1
    page = requests.get("https://stepik.org:443/api/comments?user={}&page={}".format(args.user_id, page_number),
                        headers={'Authorization': 'Bearer ' + token}).json()
    for comment in page['comments']:
        csv_output_file.writerow([str(comment[field]).replace('\n', "") for field in fields])
    print("NEXT PAGE")
    if page['meta']['has_next'] is False:
        break
