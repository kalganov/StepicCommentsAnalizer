import argparse

import matplotlib.pyplot as plt

import util_functions

parser = argparse.ArgumentParser()
parser.add_argument("keys_file", help="File which contains your client_id and client_secret")
args = parser.parse_args()
token = util_functions.get_token(args.keys_file)

courses = [187, 73, 363]

page_number = 1
average_length = 0
comments_count = 0
length_distribution = []
user_comment_count = {}
parents_childes_count = {}

for course in courses:
    while True:
        page = util_functions.get_comments_page(token, "", page_number, "", course)
        page_number += 1
        for comment in page['comments']:
            comments_count = comments_count + 1

            comment_text_length = len(comment['text'])
            average_length = average_length + comment_text_length

            length_distribution.append(comment_text_length)

            comment_user = comment['user']
            if comment_user in user_comment_count:
                user_comment_count.update(
                    {comment_user: user_comment_count.get(comment_user) + 1})
            else:
                user_comment_count.update({comment_user: 1})

            page_parent = comment['parent']
            if page_parent is not None:
                if page_parent in parents_childes_count:
                    parents_childes_count.update({page_parent: parents_childes_count.get(page_parent) + 1})
                else:
                    parents_childes_count.update({page_parent: 1})

        if not page['meta']['has_next']:
            break
        print("NEXT PAGE, COMMENTS COUNT:" + str(comments_count))
    print("NEXT COURSE")
    page_number = 1

print("Число комментариев: " + str(comments_count))
print("Средняя длинна: " + str(average_length / comments_count))
user_comment_count_distribution = []
sum = 0
c = 0
for count in user_comment_count.values():
    sum += count
    c += 1
    user_comment_count_distribution.append(count)
print("Средняя длинна цепочки: " + str(sum / c))

plt.hist(length_distribution, 75000)
xmarks = [i for i in range(1, 500 + 1, 50)]
plt.xticks(xmarks)
plt.xlim(0, 500)
plt.show()

comment_tread_length_distribution = []
for count in parents_childes_count.values():
    comment_tread_length_distribution.append(count)
plt.hist(comment_tread_length_distribution, 100)
plt.show()

user_comment_count_distribution = []
for count in user_comment_count.values():
    user_comment_count_distribution.append(count)
plt.hist(user_comment_count_distribution, 75000)
plt.xlim(0, 40)
plt.show()
