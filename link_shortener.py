import random
import string
import hashlib

class LinkShortener:
    def __init__(self):
        self.url_map = {}
        self.base_url = "http://short.url/"

    def shorten_url(self, url):
        """Shorten the given URL"""
        