#!/usr/bin/python

import os
import shutil
import logging
import inspect

import logging.handlers

EXTRACTED_POSES = "../head_pose_extraction/extracted_poses"
IMAGES_INCOMING = "../head_pose_extraction/images_incoming"
IMAGES_STORED = "../head_pose_extraction/images_stored"
IMAGES_PROCESSING = "../head_pose_extraction/images_processing"

LOG_PATH = "../logs"
ERROR_LOG_NAME = "asc_log_errors"
INFO_LOG_NAME = "asc_log_info"
MAX_DISK_SPACE_PER_LOG = 102400 # 100MB, 1GB maximum usage.
NUMBER_OF_BACKUPS = 5

LOG_MESSAGE_DELIMITER = " --- "
PARENT = 1
CALLER_OF_CALLER = "parent method: "
PARENT_OF_PARENT = 2
CALLER = ", current method: "
NAME = 3

LOG_MANAGER_START                       = "ATTENTION SCORE PROCESS MANAGER BOOTING UP"
LOG_CHECKING_DIRS                       = "ATTENTION SCORE PROCESS MANAGER: checking images_stored for new content"
LOG_THREAD_ATTENTION_SCORE_CALCULATED   = "THREAD: attention score calculated"
LOG_THREAD_ATTENTION_SCORE_PUBLISHED    = "THREAD: attention score published"
LOG_THREAD_IMAGES_PROCESSED             = "THREAD: image processing completed"
LOG_THREAD_START                        = "THREAD: starting thread: "
LOG_THREAD_TERMINATING                  = "THREAD: terminating thread"
LOG_THREAD_TIME_ELAPSED                 = "THREAD: finished in: "

LOG_ALL_INDICES_EXTRACTED               = "all indices extracted"
LOG_ATTENTION_SCORE                     = "publishing attention score: "
LOG_ATTENTION_SCORE_CALCULATED          = "attention score calculated"
LOG_ATTENTION_SCORE_PUBLISH_FAILED      = "failed to publish attention score "
LOG_DELETING_FILE                       = "deleting file post-processing: "
LOG_DIR_BECAME_ACTIVE                   = "dir became active, withdrawing removal nomination: "
LOG_HEAD_POSE_EXTRACTION_COMPLETE       = "completed head pose extraction from file: "
LOG_IMAGE_DECODED                       = "image converted to .jpg from datauri: "
LOG_NOMINATED_FOR_REMOVAL               = "dir nominated for removal due to inactivity: "
LOG_NOT_ALL_INDICES_EXTRACTED           = "HeadPoseOutputParser failed to extract all required indices"
LOG_OPENFACE_CALLED                     = "openface head pose extraction called for: "
LOG_OPENFACE_COMMAND                    = "openface command generated: "
LOG_PROVIDED_PROCESSING_DIR             = "provided directory in: "
LOG_REMOVE                              = "removing: "


def move(original_location, new_location):
    """safely moves a file"""
    try:
        shutil.move(original_location, new_location)
    except OSError as move_exception:
        log_message = construct_log_message(move_exception, original_location, new_location)
        logging.error(log_message)


def write_file(content, container):
    """safely writes to a file"""
    try:
        container.write(content)
    except Exception as write_exception:
        log_message = construct_log_message(write_exception, container)
        logging.error(log_message)


def remove_dir(dir_path):
    """safely removes a directory"""
    try:
        shutil.os.rmdir(dir_path)
    except OSError as remove_dir_error:
        log_message = construct_log_message(remove_dir_error, dir_path)
        logging.error(log_message)


def remove_file(file_path):
    """safely removes a file"""
    try:
        os.remove(file_path)
    except OSError as remove_file_error:
        log_message = construct_log_message(remove_file_error, file_path)
        logging.error(log_message)
    return file_path


def ensure_directory_exists(dir_path):
    """safely ensures a directory exists"""
    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError as create_dir_error:
            log_message = construct_log_message(create_dir_error, dir_path)
            logging.error(log_message)


def construct_log_message(*args):
    """construct a log message, make it contain at least the calling function and it's parent"""
    caller_parent = inspect.stack()[PARENT_OF_PARENT][NAME]
    caller = inspect.stack()[PARENT][NAME]
    log_message = CALLER_OF_CALLER + caller_parent + CALLER + caller
    for additional_information in args:
        log_message += LOG_MESSAGE_DELIMITER + str(additional_information)
    return log_message


def is_numeric(item_to_check):
    """checks if the item can be converted to float (should be faster than regex or similar methods)"""
    try:
        float(item_to_check)
        return True
    except ValueError:
        return False


def initialize_logging(log_file_path):
    """initializes logging, ensuring timestamp and owning thread are always mentioned. Uses a rotating file system
    to store logs in. initiates a separate errorlogger and infologger."""
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    info_file_handler = set_file_handler(log_file_path, INFO_LOG_NAME, logging.INFO, log_formatter)
    error_file_handler = set_file_handler(log_file_path, ERROR_LOG_NAME, logging.ERROR, log_formatter)
    console_handler = set_console_handler(log_formatter)

    logger.addHandler(info_file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(console_handler)


def set_file_handler(log_file_path, log_name, log_level, formatter):
    """returns a logging filehandler"""
    file_handler = logging.handlers.RotatingFileHandler("{0}/{1}.log".format(log_file_path, log_name),
                                                              maxBytes=MAX_DISK_SPACE_PER_LOG,
                                                              backupCount=NUMBER_OF_BACKUPS)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    return file_handler


def set_console_handler(log_formatter):
    """sets a console handler for logging"""
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    return console_handler
