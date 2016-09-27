#!/usr/bin/python

import os
import utils_asc as util
import logging

_OPENFACE_FEATURE_EXTRACTOR = './../../OpenFace/build/bin/FeatureExtraction '
_OPENFACE_OUTPUT_ARGS = '-rigid -verbose -no2Dfp -no3Dfp -noMparams -noAUs -noGaze -fdir "'
_OPENFACE_PATH_TO_IMAGES = './../head_pose_extraction/images_processing/'
_OPENFACE_OUTPUT = '" -of "'
_OPENFACE_OUTPUT_FILE_LOCATION = '../head_pose_extraction/extracted_poses/'
_OPENFACE_ADDITIONAL_OUTPUT_ARGS = '.txt" -world_coord 0 -q'


def construct_openface_command(target_session_id):
    """constructs the commandline argument required to run the openface build.
    target_dir == just the dirname (session_id), no path"""
    call_openface_on_dir = _OPENFACE_FEATURE_EXTRACTOR + _OPENFACE_OUTPUT_ARGS + _OPENFACE_PATH_TO_IMAGES \
                           + target_session_id + _OPENFACE_OUTPUT + _OPENFACE_OUTPUT_FILE_LOCATION + target_session_id \
                           + _OPENFACE_ADDITIONAL_OUTPUT_ARGS
    log_message = util.construct_log_message(util.LOG_OPENFACE_COMMAND, call_openface_on_dir)
    logging.info(log_message)
    return call_openface_on_dir


def clean_processed_files(processed_images):
    """removes image files that have been processed"""
    for image_file in processed_images:
        image_in_processing = image_file.replace(util.IMAGES_STORED, util.IMAGES_PROCESSING)
        util.remove_file(image_in_processing)
        log_message = util.construct_log_message(util.LOG_DELETING_FILE, image_in_processing)
        logging.info(log_message)


def extract_head_poses(target_session_id, processed_images):
    """constructs a commandline arg, executes openface head pose extraction. Output files are placed
    in 'extracted_poses', named by session_id."""
    command_run_openface = construct_openface_command(target_session_id)
    os.system(command_run_openface)
    clean_processed_files(processed_images)
    log_message = util.construct_log_message(util.LOG_OPENFACE_CALLED, target_session_id)
    logging.info(log_message)

