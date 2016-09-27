#!/usr/bin/python

import logging

import utils_asc as util
from head_pose_output_parser import HeadPoseOutputParser


class HeadPoseProcessor(object):

    _DELIMITER = ", "
    _OUTPUT_FILE_EXTENSION = ".txt"
    # min and max observed values taken from dataset
    _RX_MIN = -0.66152
    _RX_MAX = 0.227974
    _RY_MIN = -0.62082
    _RY_MAX = 0.767781
    _RZ_MIN = -0.19357
    _RZ_MAX = 0.215416
    # SVM weights taken from weka output
    _WEIGHT_RX = 0.8263
    _WEIGHT_RY = -0.3339
    _WEIGHT_RZ = 2.0768
    _WEIGHT = -1.5134
    _CUT_OFF_VALUE = 1.5445160234619718
    _PAYING_ATTENTION = 1
    _NOT_PAYING_ATTENTION = 0
    _NO_STUDENTS = 0

    # average observed attention scores during classes
    # TODO: future developer: adjust the values below when more data becomes available, the current basis for these
    # numbers is too small to be reliable.
    _AVERAGE_ATTENTION_RATIO = 0.376
    _RANGE_SCALE_ABOVE_AVERAGE = 0.624
    _RELATIVE_ATTENTION_SCORE_MINIMUM = 0
    _RANGE_SCALE_BELOW_AVERAGE = 0.752
    _FIFTY_PERCENT = 0.5

    def __init__(self, target_dir):
        self._path_to_class_dir = util.EXTRACTED_POSES + "/" + target_dir + self._OUTPUT_FILE_EXTENSION
        self._failed_read = False

    def get_attention_score_from_head_poses(self):
        """calculates and returns the average attention score of the supplied sample"""
        attention_score = self._get_current_attention_score(self._path_to_class_dir)
        log_message = util.construct_log_message(util.LOG_ATTENTION_SCORE_CALCULATED)
        logging.info(log_message)
        return attention_score

    def _get_current_attention_score(self, output_file_location):
        """gets the asc, gets head poses, calls calculation method. returns none if failed to read output"""
        openface_output_parser = HeadPoseOutputParser()
        extracted_head_poses = openface_output_parser.extract_valid_head_poses_from_output_file(output_file_location)
        attention_score = self._interpret_all_head_poses(extracted_head_poses)
        return attention_score

    def _interpret_all_head_poses(self, extracted_head_poses):
        """interprets all head poses found in the currently targetted session's head pose output file"""
        list_of_classifications = list()
        for rx, ry, rz in extracted_head_poses:
            if rx is not None:
                self._determine_if_paying_attention(rx, ry, rz, list_of_classifications)
            else:
                self._failed_read = True
                break
        attention_score = self._calculate_average_attention_score(list_of_classifications)
        relative_attention_score = self._calculate_relative_attention_score(attention_score)
        return relative_attention_score

    def _determine_if_paying_attention(self, rx, ry, rz, list_of_classifications):
        """uses a trained SVM classifier to determine if a student is paying attention. Stores this boolean
        in list_of_classifications."""
        normalized_rx = self._normalize_score(rx, self._RX_MIN, self._RX_MAX)
        normalized_ry = self._normalize_score(ry, self._RY_MIN, self._RY_MAX)
        normalized_rz = self._normalize_score(rz, self._RZ_MIN, self._RZ_MAX)
        attention_classification = (self._WEIGHT_RX * normalized_rx) + \
                                   (self._WEIGHT_RY * normalized_ry) + \
                                   (self._WEIGHT_RZ + normalized_rz) + \
                                    self._WEIGHT
        converted_classification = self._convert_to_boolean(attention_classification)
        list_of_classifications.append(converted_classification)

    def _normalize_score(self, score, min, max):
        """normalizes a given score in relation to a given max and min score"""
        normalized_score = ((score - min) / (max - min))
        return normalized_score

    def _convert_to_boolean(self, numeric_classification):
        """converts a numeric classification to a 1 or 0. This eliminates the effect of possible numeric_classification
        outliers skewing the total attention score."""
        if numeric_classification > self._CUT_OFF_VALUE:
            return self._NOT_PAYING_ATTENTION
        else:
            return self._PAYING_ATTENTION

    def _calculate_average_attention_score(self, list_of_classifications):
        """takes the average of the contents of the list as attention score if it's not empty or an incomplete read"""
        average_attention_score = None
        if list_of_classifications:
            if list_of_classifications[0] is not None:
                divisor = len(list_of_classifications)
                dividend = 0
                for classification in list_of_classifications:
                    dividend += classification
                average_attention_score = float((dividend / divisor))
        return average_attention_score

    def _calculate_relative_attention_score(self, attention_score):
        """compares the attention score to how much attention a class pays on average. The average attention in classes
        is 0.376; this represents 50%, neutral. The negative half of this scale (0-50%) is represented by values from 0
        to 0.376, the positive half (50-100%) values from 0.376 to 1."""
        relative_attention_score = None
        if attention_score is not None:
            if attention_score > self._AVERAGE_ATTENTION_RATIO:
                deviation_from_average = attention_score - self._AVERAGE_ATTENTION_RATIO
                deviation_relative_to_scale = deviation_from_average / self._RANGE_SCALE_ABOVE_AVERAGE
                relative_attention_score = self._FIFTY_PERCENT + (deviation_relative_to_scale * self._FIFTY_PERCENT)
            else:
                relative_attention_score = attention_score / self._RANGE_SCALE_BELOW_AVERAGE
        return relative_attention_score
