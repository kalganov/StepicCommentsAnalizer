import csv
import re
import sys
import pandas as pd


def standardize_text(df, text_field):
    df[text_field] = re.sub(r'@[a-zA-Zа-яА-Я]*[_[a-zA-Zа-яА-Я]*]*', '', df[text_field])
    df[text_field] = re.sub(r'[^а-яА-Я ]', '', df[text_field])
    df[text_field] = re.sub(r'http\S+', '', df[text_field])
    df[text_field] = re.sub(r'http', '', df[text_field])
    df[text_field] = re.sub(r'@\S+', '', df[text_field])
    df[text_field] = re.sub(r'(<(/?[^>]+)>)', '', df[text_field])
    df[text_field] = re.sub(r'[-.?!)(,:]', '', df[text_field])
    df[text_field] = df[text_field].lower()
    return df


intLimitInPython = 2147483647
csv.field_size_limit(intLimitInPython)

with open('D:\StepicCommentsAnalizer\datasets\comment_pos.csv', "r", encoding='utf-8') as csvfile:
    with open('clean_comments.csv', "a", encoding='utf-8') as clean_comment_file:
        comments_reader = csv.DictReader(csvfile, dialect='excel-tab')
        clean_comment = csv.writer(clean_comment_file, dialect='excel-tab')

        for comment in comments_reader:
            text = standardize_text(comment, "text")
            clean_comment.writerow([str(comment[field]).replace('\n', "") for field in text.keys()])

