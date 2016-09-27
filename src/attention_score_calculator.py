#!/usr/bin/python

import time
import os
import logging

import utils_asc as util
from thread_attention_score_calculation import AttentionCalculationThread


class AttentionScoreProcessManager:
    """the Main, so to speak. Triggers all events every _INTERVAL seconds. Starts a new thread per sessionid dir
    with content. These threads calculate the attention score for the session, post it to ClientManager and
    self-terminate."""

    _THREAD = "thread:"
    _EMPTY = 0
    _INTERVAL = 15
    _LOG_PATH = "../logs"
    _LOG_NAME = "asc_log"
    _GITKEEP = ".gitkeep"

    def __init__(self):
        self._list_of_empty_dirs = list()
        self._time_to_check_empty_dirs_for_removal = False
        util.initialize_logging(util.LOG_PATH)

    def trigger_attention_score_calculation_every_interval(self):
        """calls all methods every _INTERVAL seconds, adjusts for drift."""
        next_call = time.time()
        log_message = util.construct_log_message(util.LOG_MANAGER_START)
        logging.info(log_message)
        while True:
            next_call = next_call + self._INTERVAL
            time.sleep(next_call - time.time())
            self._remove_all_empty_dirs()
            timestamp = next_call
            self._calculate_attention_score_on_dirs_with_content(timestamp)
            log_message = util.construct_log_message(util.LOG_CHECKING_DIRS)
            logging.info(log_message)

    def _remove_all_empty_dirs(self):
        """checks all dirs in file system for removal, uses a boolean to ensure this function is run once every
        (2 * _INTERVAL seconds) as a safety measure."""
        if self._time_to_check_empty_dirs_for_removal:
            self._clean_up_empty_dirs(util.IMAGES_INCOMING)
            self._clean_up_empty_dirs(util.IMAGES_STORED)
            self._clean_up_empty_dirs(util.IMAGES_PROCESSING)
            self._time_to_check_empty_dirs_for_removal = False
        else:
            self._time_to_check_empty_dirs_for_removal = True

    def _clean_up_empty_dirs(self, target_parent_dir_path):
        """adds empty subdirs to a list, deletes them if they are already in that list at the moment of adding.
        This ensures the file system doesn't get cluttered, as sessionids are not persistent across classes/lessons"""
        for subdir in os.listdir(target_parent_dir_path):
            subdir_path = target_parent_dir_path + "/" + subdir
            if self._GITKEEP not in subdir:
                if not self._dir_has_content(subdir_path):
                    if subdir_path in self._list_of_empty_dirs:
                        util.remove_dir(subdir_path)
                        self._list_of_empty_dirs.remove(subdir_path)
                        log_message = util.construct_log_message(util.LOG_REMOVE, subdir_path)
                        logging.info(log_message)
                    else:
                        self._list_of_empty_dirs.append(subdir_path)
                        log_message = util.construct_log_message(util.LOG_NOMINATED_FOR_REMOVAL, subdir_path)
                        logging.info(log_message)

    def _dir_has_content(self, path_to_target_dir):
        """checks if a directory has items in it"""
        if self._GITKEEP not in path_to_target_dir:
            dir_content = os.listdir(path_to_target_dir)
            if len(dir_content) > self._EMPTY:
                return True
        return False

    def _calculate_attention_score_on_dirs_with_content(self, timestamp):
        """runs attention score calculation on dirs with content by starting a thread, manages dirs incorrectly
        labelled as contentless"""
        for session_id in os.listdir(util.IMAGES_STORED):
            if self._GITKEEP not in session_id:
                subdir_path = util.IMAGES_STORED + "/" + session_id
                if self._dir_has_content(subdir_path):
                    thread_name = self._THREAD + session_id
                    asc_thread = AttentionCalculationThread(thread_name, session_id, timestamp, self._INTERVAL)
                    asc_thread.start()
                    if subdir_path in self._list_of_empty_dirs:
                        self._list_of_empty_dirs.remove(subdir_path)
                        log_message = util.construct_log_message(util.LOG_THREAD_ATTENTION_SCORE_PUBLISHED)
                        logging.info(log_message)


if __name__ == "__main__":
    attention_score_calculator = AttentionScoreProcessManager()
    attention_score_calculator.trigger_attention_score_calculation_every_interval()

