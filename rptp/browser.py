import time
from http.client import CannotSendRequest, ResponseNotReady
from threading import Thread
from urllib.parse import urlencode

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from rptp.watcher import VideoWatcher
from .config import LOGIN, PASSWORD
from .data.urls import VK_BASE_URL, VK_VIDEO_URL

DEFAULT_SEARCH_PARAMS = {
    'hd': 1,
    'len': 2,
    'notsafe': 1,
    'order': 0,
}


class Browser(Thread):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.query = ''
        self.watcher = VideoWatcher(self)

    def __enter__(self):
        if not self.driver:
            self.driver = webdriver.Chrome()

        self.login_to_vk()

        if not self.watcher.is_alive():
            self.watcher.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def login_to_vk(self, login=LOGIN, password=PASSWORD):
        self.driver.get(VK_BASE_URL)
        self.driver.find_element_by_id("index_email").send_keys(login)
        self.driver.find_element_by_id("index_pass").send_keys(password)
        self.driver.find_element_by_id('index_login_form').submit()
        time.sleep(2)

    def search_videos(self, search_query):
        self.query = search_query

        try:
            if VK_VIDEO_URL in self.current_url:
                search_field = self.driver.find_element_by_id('video_search_input')
                search_field.clear()
                search_field.send_keys(search_query)
                # search_field.submit()
            else:
                # https://vk.com/video?hd=1&len=2&notsafe=1&order=0&q=Lika
                params = DEFAULT_SEARCH_PARAMS.copy()
                params['q'] = search_query

                url = '{}?{}'.format(VK_VIDEO_URL, urlencode(params))
                self.driver.get(url)

            return True
        except WebDriverException:
            return False
        except CannotSendRequest:
            time.sleep(1)
            self.search_videos(search_query)

    def close(self):
        try:
            self.driver.close()
        except WebDriverException:
            pass

    @property
    def current_url(self):
        try:
            return self.driver.current_url
        except (CannotSendRequest, ResponseNotReady):
            time.sleep(1)
            return self.current_url

    def get_info(self):
        try:
            return self.query, self.current_url
        except WebDriverException:
            return ()
