import threading
from tkinter import simpledialog

from nyphilscraper.get_image_urls import get_image_urls
from nyphilscraper.retrieve_images import retrieve_images
from nyphilscraper.make_PDF import make_PDF


class ThreadedTask(threading.Thread):
    def __init__(self, message_queue, progress_queue, url, file_path):
        super().__init__()
        self.message_queue = message_queue
        self.progress_queue = progress_queue
        self.url = url
        self.file_path = file_path

    def run(self):
        self.message_queue.put('Waiting for url')
        self.progress_queue.put('setmode:indeterminate')
        self.progress_queue.put('start')

        self.progress_queue.put('stop')
        self.message_queue.put('Collecting image URLs')
        self.progress_queue.put('start')
        img_urls = get_image_urls(self.url)
        self.progress_queue.put('stop')

        self.message_queue.put('Retrieving images')
        self.progress_queue.put('setmode:determinate')
        self.progress_queue.put('set:50')
        img_names = retrieve_images(img_urls)
        self.progress_queue.put('set:0')

        self.message_queue.put('Building PDF')
        self.progress_queue.put('set:50')
        make_PDF(self.file_path, img_names)
        self.progress_queue.put('set:100')
        self.message_queue.put('PDF Done')
