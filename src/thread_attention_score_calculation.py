#!/usr/bin/python

import threading
import logging
import time

from move_incoming_images_to_processing import ImageTransporter
import run_head_pose_extraction as pose_extractor
from head_pose_processor import HeadPoseProcessor
from attention_score_publisher import AttentionScorePublisher
import utils_asc as util

class AttentionCalculationThread (threading.Thread):
    """self-terminating thread, extracts head poses from a session-id folder, calculates attention scores
    and POSTs them to external ClientsHandler application"""

    _EXIT_CODE = 0

    def __init__(self, thread_id, session_id, timestamp, interval):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self._session_id = session_id
        self._timestamp = timestamp
        self._interval = interval

    def run(self):
        self._run_attention_score_calculation()
        time_elapsed = time.time() - self._timestamp
        log_message = util.construct_log_message(util.LOG_THREAD_TERMINATING, util.LOG_THREAD_TIME_ELAPSED, time_elapsed)
        if time_elapsed <= self._interval:
            logging.info(log_message)
        else:
            logging.error(log_message)
        return self._EXIT_CODE

    def _run_attention_score_calculation(self):
        """runs modules required for attention score calculation"""
        log_message = util.construct_log_message(util.LOG_THREAD_START, self.thread_id, self._session_id)
        logging.info(log_message)
        images_being_processed = self._move_session_images_to_processing_directory()
        attention_score = self._extract_attention_score_from_session_images_in_processing(images_being_processed)
        self._output_result(attention_score)

    def _move_session_images_to_processing_directory(self):
        """moves session-images to the images_processing folder"""
        images_to_processing_mover = ImageTransporter(self._session_id)
        images_being_processed = images_to_processing_mover.transport_incoming_images_to_processing()
        log_message = util.construct_log_message(util.LOG_THREAD_IMAGES_PROCESSED)
        logging.info(log_message)
        return images_being_processed

    def _extract_attention_score_from_session_images_in_processing(self, images_being_processed):
        """extracts the attention score from session-images"""
        pose_extractor.extract_head_poses(self._session_id, images_being_processed)
        extracted_poses_processor = HeadPoseProcessor(self._session_id)
        attention_score = extracted_poses_processor.get_attention_score_from_head_poses()
        log_message = util.construct_log_message(util.LOG_THREAD_ATTENTION_SCORE_CALCULATED)
        logging.info(log_message)
        return attention_score

    def _output_result(self, attention_score):
        """POSTS the session's attention score to the external ClientsManager application"""
        result_publisher = AttentionScorePublisher()
        result_publisher.publish_results(attention_score, self._session_id, self._timestamp)
        log_message = util.construct_log_message(util.LOG_THREAD_ATTENTION_SCORE_PUBLISHED)
        logging.info(log_message)
