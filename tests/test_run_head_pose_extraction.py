#!/usr/bin/python

import unittest
import sys
sys.path.append("../src")

import run_head_pose_extraction as rhpe


class OpenFaceCallerScriptTestSuite(unittest.TestCase):
    """contains tests for the run_head_pose_extraction script"""

    _TARGET_SESSION = "simulated_session_id"

    _COMMAND_ARGS_1 = './../../OpenFace/build/bin/FeatureExtraction -rigid -verbose -no2Dfp -no3Dfp -noMparams ' \
                              '-noAUs -noGaze -fdir "./../head_pose_extraction/' \
                              'images_processing/'
    _COMMAND_ARGS_2 = '" -of "../head_pose_extraction/extracted_poses/'
    _COMMAND_ARGS_3 = '.txt" -world_coord 0 -q'

    def setUp(self):
        self._constructed_command = self._construct_command()
        self._desired_command = self._COMMAND_ARGS_1 + self._TARGET_SESSION + self._COMMAND_ARGS_2 + \
                                self._TARGET_SESSION + self._COMMAND_ARGS_3

    def _construct_command(self):
        return rhpe.construct_openface_command(self._TARGET_SESSION)

    def test_correct_command_constructed(self):
        """tests if the construct_openface_command method generates the correct command, based on the name of the
        target output.txt file"""
        self.assertEqual(self._constructed_command, self._desired_command)