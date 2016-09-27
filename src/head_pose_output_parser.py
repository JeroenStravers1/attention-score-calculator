#!/usr/bin/python

import utils_asc as util
import logging

class HeadPoseOutputParser(object):
    """OpenFace outputs head poses and other data as a non-formatted csv. This class splits the file into individual
    elements, and extracts the indices of elements required for further analysis."""

    _SUCCESS = "success"
    _RX = "pose_Rx"
    _RY = "pose_Ry"
    _RZ = "pose_Rz"
    _DELIMITER = ", "
    _INDEX_INCREMENT = 1
    _ONE_STEP_BACK = 1
    _HEADER = 0
    _SUCCESSFUL_READ_VALUE = 1

    def __init__(self):
        self._index_success = 0
        self._index_rx = 0
        self._index_ry = 0
        self._index_rz = 0
        self._line_length = 0
        self._split_output_file = list()
        self._failed_to_read_output_file = False

    def extract_valid_head_poses_from_output_file(self, file_location):
        """opens the entire file in a single line (openface returns an unformatted csv as output (no \n))
        returns a generator (rx,ry,rz), removes the parsed output file"""
        with open(file_location, "r") as estimated_head_poses:
            head_poses_output_as_single_line = estimated_head_poses.read()
            self._parse_unformatted_head_poses(head_poses_output_as_single_line)
        extracted_poses = self._extract_head_pose_values()
        util.remove_file(file_location)
        log_message = util.construct_log_message(util.LOG_HEAD_POSE_EXTRACTION_COMPLETE, file_location)
        logging.info(log_message)
        return extracted_poses

    def _parse_unformatted_head_poses(self, poses_output):
        """"splits the output file by ', ' -> leaving only the values"""
        poses_output_without_breaks = poses_output.replace("\n", ", ")
        self._split_output_file = poses_output_without_breaks.split(self._DELIMITER)
        self._extract_index_of_success_rx_ry_rz_values()

    def _extract_index_of_success_rx_ry_rz_values(self):
        """extract indices of success, rx, ry, rz and the length of the header (where the values start)"""
        current_index = 0
        for item in self._split_output_file:
            if item == self._SUCCESS:
                self._index_success = current_index
            elif item == self._RX:
                self._index_rx = current_index
            elif item == self._RY:
                self._index_ry = current_index
            elif item == self._RZ:
                self._index_rz = current_index
            elif util.is_numeric(item):
                self._line_length = current_index
                if not self._all_indices_extracted():
                    self._failed_to_read_output_file = True
                break
            current_index += self._INDEX_INCREMENT

    def _all_indices_extracted(self):
        """check if all required indices have been successfully extracted from the output file"""
        if all(index > 0 for index in (self._index_success, self._index_rx,
                                       self._index_ry, self._index_rz, self._line_length)):
            log_message = util.construct_log_message(util.LOG_ALL_INDICES_EXTRACTED)
            logging.info(log_message)
            return True
        log_message = util.construct_log_message(util.LOG_NOT_ALL_INDICES_EXTRACTED)
        logging.error(log_message)
        return False

    def _extract_head_pose_values(self):
        """yields rx,ry,rz from output file line by line"""
        if not self._failed_to_read_output_file:
            number_of_lines = 0
            if self._line_length > 0:
                number_of_lines = int(len(self._split_output_file) / self._line_length)
            for row_number in range(number_of_lines):
                current_position = self._line_length* row_number
                if self._is_valid_head_pose_data(current_position):
                    rx_index_in_text = current_position + self._index_rx
                    ry_index_in_text = current_position + self._index_ry
                    rz_index_in_text = current_position + self._index_rz
                    current_rx = float(self._split_output_file[rx_index_in_text])
                    current_ry = float(self._split_output_file[ry_index_in_text])
                    current_rz = float(self._split_output_file[rz_index_in_text])
                    yield current_rx, current_ry, current_rz
        else:
            yield None, None, None

    def _is_valid_head_pose_data(self, current_position):
        """ensures that the header line and unsuccessful pose estimations are skipped"""
        current_success_index = current_position + self._index_success
        success_result_value_in_line = self._split_output_file[current_success_index]
        if not util.is_numeric(success_result_value_in_line):
            return False
        elif int(success_result_value_in_line) != self._SUCCESSFUL_READ_VALUE:
            return False
        return True
