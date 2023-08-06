from __future__ import unicode_literals

from datetime import datetime
from tkinter.messagebox import showerror, askokcancel
from tkinter import *
from threading import Lock, Thread

import os
import logging


class LogHandle(object):
    __file_dir = None
    __base_name = None
    __gui_console = None

    """
    Logging that becomes easier and more uniformed
    """

    def __init__(self, file_dir=None, base_name=None):
        """
        Logging settings not forgotten!

        :param file_dir: File directory of where log files will be saved
        :param base_name: A base filename that log files will be saved as
        """

        self.file_dir = file_dir
        self.base_name = base_name

    @property
    def file_dir(self):
        return self.__file_dir

    @file_dir.setter
    def file_dir(self, file_dir):
        if not isinstance(file_dir, (str, type(None))):
            raise Exception("'file_dir' is missing")
        if file_dir and not os.path.exists(file_dir):
            raise Exception("'file_dir' does not exist")

        self.__file_dir = file_dir

    @property
    def base_name(self):
        return self.__base_name

    @base_name.setter
    def base_name(self, base_name):
        if not isinstance(base_name, (str, type(None))):
            raise Exception("'base_name' is missing")

        self.__base_name = base_name

    @staticmethod
    def __clean_handlers():
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    def gui_console(self, destroy=False, turn_off=False):
        if self.__gui_console and destroy:
            self.__gui_console.destroy()
            self.__gui_console = None
        elif self.__gui_console and turn_off:
            self.__gui_console = None
        else:
            self.__gui_console = GUIConsole()

    def write_to_log(self, message, action='info'):
        """
        Logging becomes more organized!

        :param message: Message that you would like to write to log
        :param action: What kind of action would you like the entry to be marked as?
            (debug, info, warning, error, critical)
        """

        if self.__base_name and self.__file_dir:
            if not message:
                raise Exception("'message' is missing")

            self.__clean_handlers()
            filepath = os.path.join(self.__file_dir,
                                    "{0}_{1}_Log.txt".format(datetime.now().__format__("%Y%m%d"), self.__base_name))

            logging.basicConfig(filename=filepath,
                                level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

        if self.__gui_console:
            self.__gui_console.print_gui('{0} - {1} - {2}'.format(datetime.now(), action.upper(), message))
        else:
            print('{0} - {1} - {2}'.format(datetime.now(), action.upper(), message))

        if self.__base_name and self.__file_dir:
            if action.lower() == 'debug':
                logging.debug(message)
            elif action.lower() == 'info':
                logging.info(message)
            elif action.lower() == 'warning':
                logging.warning(message)
            elif action.lower() == 'error':
                logging.error(message)
            elif action.lower() == 'critical':
                logging.critical(message)

    def __del__(self):
        logging.shutdown()


class GUIConsole(Toplevel):
    __print_lock = Lock()
    __print_queue = list()
    __console_text = None

    """
        Class to show logging in a GUI window by using Toplevel in tkinter
    """

    def __init__(self):
        Toplevel.__init__(self)
        self.__build()
        self.__start_idle()

    def __start_idle(self):
        self.after(5, self.__on_idle)

    def print_gui(self, msg, sep='\n'):
        with self.__print_lock:
            self.__print_queue.append(str(msg) + sep)

    def __build(self):
        my_frame = Frame(self)
        my_frame.pack()

        self.__console_text = Text(my_frame, bg="black", fg="white")
        self.__console_text.pack()

    def __on_idle(self):
        with self.__print_lock:
            for msg in self.__print_queue:
                self.__console_text.insert(END, msg)
                self.__console_text.see(END)

            self.__print_queue = []

        self.after(5, self.__on_idle)
