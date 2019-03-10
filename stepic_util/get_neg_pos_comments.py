import argparse
import csv

from stepic_util import util_functions

page_number = 13747
comments_count = 10842

parser = argparse.ArgumentParser()
parser.add_argument("keys_file", help="File which contains your client_id and client_secret")
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

csv_output_neg = csv.writer(open("datasets/comment_neg.csv", "a", encoding='utf-8'), dialect='excel-tab')
csv_output_pos = csv.writer(open("datasets/comment_pos.csv", "a", encoding='utf-8'), dialect='excel-tab')
csv_output_neg.writerow(fields)
csv_output_pos.writerow(fields)

while True:
    page = util_functions.get_comments_page(token, page=page_number)
    page_number += 1
    for comment in page['comments']:

        if comment['epic_count'] > 1:
            csv_output_pos.writerow([str(comment[field]).replace('\n', "") for field in fields])
            # csv_output_pos.writerow([str(comment['text']).replace('\n', "")])
            print('Positive: ' + comment['text'])
            comments_count = comments_count + 1

        if comment['abuse_count'] > 1:
            csv_output_neg.writerow([str(comment[field]).replace('\n', "") for field in fields])
            # csv_output_neg.writerow([str(comment['text']).replace('\n', "")])
            print('Negative: ' + comment['text'])
            comments_count = comments_count + 1

    if not page['meta']['has_next']:
        break
    csv_output_neg = csv.writer(open("datasets/comment_neg.csv", "a", encoding='utf-8'), dialect='excel-tab')
    csv_output_pos = csv.writer(open("datasets/comment_pos.csv", "a", encoding='utf-8'), dialect='excel-tab')
    print("NEXT PAGE: " + str(page_number) + ", COMMENTS COUNT:" + str(comments_count))
