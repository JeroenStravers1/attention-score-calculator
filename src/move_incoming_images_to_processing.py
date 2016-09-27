#!/usr/bin/python

import shutil
import os
import errno
import logging

import utils_asc as util


class ImageTransporter(object):
    """transports images from a session_id from images_stored to images_processing"""

    _GITKEEPFILE = ".gitkeep"

    def __init__(self, session_id):
        self._target_directory = session_id
        self._target_dir_with_path_in_stored = util.IMAGES_STORED + "/" + self._target_directory
        self._target_dir_with_path_in_processing = util.IMAGES_PROCESSING + "/" + self._target_directory

    def transport_incoming_images_to_processing(self):
        """clears sessionid-dir in processing folder, lists images to move there, moves them"""
        self._provide_cleared_processing_classdir()
        images_to_move = self._make_list_of_incoming_images()
        self._move_to_processing(images_to_move)
        return images_to_move

    def _provide_cleared_processing_classdir(self):
        """clears the classdir in processing if this dir already exists,
        create the dir if it does not. Log errors in creation and removal"""
        if os.path.isdir(self._target_dir_with_path_in_processing):
            for image_name in os.listdir(self._target_dir_with_path_in_processing):
                self._delete_item_in_images_processing_dir(image_name)
        else:
            util.ensure_directory_exists(self._target_dir_with_path_in_processing)
        log_message = util.construct_log_message(util.LOG_PROVIDED_PROCESSING_DIR,
                                                 self._target_dir_with_path_in_processing)
        logging.info(log_message)

    def _delete_item_in_images_processing_dir(self, item_name):
        """deletes an item in the images_processing folder"""
        image_with_path = self._target_dir_with_path_in_processing + "/" + item_name
        util.remove_file(image_with_path)

    def _make_list_of_incoming_images(self):
        """store all head_pose_extraction in the folder in a list"""
        images_to_transfer = list()
        for image_name in os.listdir(self._target_dir_with_path_in_stored):
            image_and_path = self._target_dir_with_path_in_stored + "/" + image_name
            images_to_transfer.append(image_and_path)
        return images_to_transfer

    def _move_to_processing(self, images_to_move):
        """moves all items in the list to the processing folder (in a class-specific folder)"""
        for current_item_path in images_to_move:
            new_item_path = current_item_path.replace(util.IMAGES_STORED, util.IMAGES_PROCESSING)
            util.move(current_item_path, new_item_path)
