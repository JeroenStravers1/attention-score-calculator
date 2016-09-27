#!/usr/bin/python

import unittest
import os
import sys

sys.path.append("../src")
from move_incoming_images_to_processing import ImageTransporter
import utils_asc as util

class ImageTransporterTestSuite(unittest.TestCase):
    """contains tests for the move_incoming_images_to_processing module"""

    _IMAGE_TRANSPORTER_TEST_DIR_PATH = "../head_pose_extraction/images_stored/test_dir"
    _IMAGE_TRANSPORTER_TEST_IMG_PATH = "../head_pose_extraction/images_stored/test_dir/test_img.jpg"
    _IMAGE_TRANSPORTER_TEST_REMOVE_DIR_PATH = "../head_pose_extraction/images_processing/test_dir"
    _IMAGE_TRANSPORTER_TEST_REMOVE_IMG_PATH = "../head_pose_extraction/images_processing/test_dir/test_img.jpg"
    _IMAGE_TRANSPORTER_TEST_DIR_NAME = "test_dir"
    _IMAGE_TRANSPORTER_TEST_IMG_NAME = "test_img.jpg"

    def setUp(self):
        self._provision_test_image_transporter()

    def _provision_test_image_transporter(self):
        """create the test image and dir created for test_image_transporter_file_transfer test"""
        util.ensure_directory_exists(self._IMAGE_TRANSPORTER_TEST_DIR_PATH)
        try:
            open(self._IMAGE_TRANSPORTER_TEST_IMG_PATH, 'wb')
        except OSError as img_ose:
            print("mk_testimg" + str(img_ose))

    def test_image_transporter_file_transfer(self):
        """checks if (test_move/test.jpg) dir and file in images_stored are correctly moved to images_processing"""
        test_transporter = ImageTransporter(self._IMAGE_TRANSPORTER_TEST_DIR_NAME)
        transported_paths = test_transporter.transport_incoming_images_to_processing()
        transported_image_path = transported_paths[0].replace(self._IMAGE_TRANSPORTER_TEST_DIR_PATH,
                                                              self._IMAGE_TRANSPORTER_TEST_REMOVE_DIR_PATH)
        image_transported_successfully = os.path.isfile(transported_image_path)
        self.assertTrue(image_transported_successfully)

    def tearDown(self):
        self._remove_test_image_transporter_files()

    def _remove_test_image_transporter_files(self):
        """remove the test image and dir created for test_image_transporter_file_transfer test"""
        try:
            os.remove(self._IMAGE_TRANSPORTER_TEST_REMOVE_IMG_PATH)
        except OSError as del_img_ose:
            print ("rm_test_img_processing" + str(del_img_ose))
        try:
            os.rmdir(self._IMAGE_TRANSPORTER_TEST_REMOVE_DIR_PATH)
        except OSError as del_dir_proc_ose:
            print ("rm_test_dir_processing" + str(del_dir_proc_ose))
        try:
            os.remove(self._IMAGE_TRANSPORTER_TEST_IMG_PATH)
        except OSError as del_img_ose:
            print("rm_test_img_stored" + str(del_img_ose))
        try:
            os.rmdir(self._IMAGE_TRANSPORTER_TEST_DIR_PATH)
        except OSError as del_dir_stor_ose:
            print("rm_test_dir_stored" + str(del_dir_stor_ose))