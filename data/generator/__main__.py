# coding: utf-8
from generator.html import generate_html
import argparse

parser = argparse.ArgumentParser(description='Generates an HTML table from a JSON file containing data.')
parser.add_argument('type', type=str, help='music or video')
parser.add_argument('file', type=str, help='file to read from')

args = parser.parse_args()
if not args.type in ['music', 'video']:
    print("type must be music or video")

print(generate_html(args.type, args.file))
