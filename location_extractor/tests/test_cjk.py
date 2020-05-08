import signal, unittest
from datetime import datetime
from inspect import getargspec
from location_extractor import *
from os.path import abspath, dirname, join
from requests import get
from unittest import TestCase

path_to_directory_of_this_file = dirname(realpath(__file__))

class Chinese(TestCase):
    def test_article(self):
        with open(join(path_to_directory_of_this_file, 'chinese.txt')) as f:
            text = f.read()
        locations = extract_locations_from_text(text)
        print("locations:", locations)
        
    def test_hubei(self):
        text = "4月26日，湖北大学官方微博发文表示，由于有网友反映该校文学院教授梁艳萍在个人社交媒体平台发布“不当言论”，学校已成立调查组，将视调查结果进行“严肃处理”。"
        locations = extract_locations_from_text(text)
