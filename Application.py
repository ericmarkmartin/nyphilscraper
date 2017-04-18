import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import simpledialog
import queue
import re

from nyphilscraper.ThreadedTask import ThreadedTask


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.message = tk.Message(parent)
        self.message.pack()
        self.message_queue = queue.Queue()

        self.progress = ttk.Progressbar(parent,
                                        orient='horizontal',
                                        length=200,
                                        mode='indeterminate')
        self.progress.pack()
        self.progress_queue = queue.Queue()

        self.get_score_url()
        self.get_save_file()

        thread = ThreadedTask(self.message_queue,
                              self.progress_queue,
                              self.url,
                              self.file_path)
        print(thread)
        thread.start()

        self.parent.after(100, self.process_message_queue)
        self.parent.after(100, self.process_progress_queue)

    def _set_message_text(self, text):
        self.message['text'] = text

    def process_message_queue(self):
        # print('processing message queue')
        try:
            text = self.message_queue.get(0)
            print(text)
            self._set_message_text(text)
        except queue.Empty:
            pass
            # print('message queue empty')
        finally:
            self.parent.after(100, self.process_message_queue)

    def _set_progress_mode(self, mode):
        if mode not in ['determinate', 'indeterminate']:
            msg = 'mode must be \'determinate\' or \'indeterminate\''
            raise ValueError(msg)
        self._stop_progress()
        self.progress.config(mode=mode)

    def _start_progress(self):
        print('start progress')
        if self.progress['mode'].string == 'indeterminate':
            print('indeterminate progress starting')
            self.progress.start()

    def _stop_progress(self):
        if self.progress['mode'].string == 'indeterminate':
            self.progress.stop()
            self.progress.config(value=0)

    def _set_progress_value(self, value):
        if not 0 <= value <= 100:
            msg = 'value must be a valid percentage (0-100)'
            raise ValueError(msg)
        if self.progress['mode'].string == 'determinate':
            self.progress.config(value=value)

    def process_progress_queue(self):
        # print('processing progress queue')
        try:
            command = self.progress_queue.get(0)
            print(command)
            if re.match('setmode:[a-z]+', command):
                mode = command[8:]
                print('MODE INSIDE:', mode)
                self._set_progress_mode(mode)
            if command == 'start':
                self._start_progress()
            elif command == 'stop':
                self._stop_progress()
            elif re.match('set:\d+', command):
                value = int(command[4:])
                self._set_progress_value(value)
        except queue.Empty:
            pass
            # print('progress queue empty')
        finally:
            self.parent.after(100, self.process_progress_queue)

    def get_score_url(self):
        self.url = simpledialog.askstring(
            'Enter URL',
            ('Enter the URL for the score '
             'on the NY Phil archive that '
             'you want to download.')
        )

    def get_save_file(self):
        self.file_path = filedialog.asksaveasfilename(parent=self.parent)
