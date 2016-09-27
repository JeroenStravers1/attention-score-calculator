#!/usr/bin/python

import json
import base64

import utils_asc as util


class ImageConverter(object):
    """converts incoming DataURIs to jpg files. writes them to images_incoming, then after write moves
    them to images_stored"""

    _IMG_DATA = "data"
    _IMG_URI = "frame"
    _CLIENT_ID = "clientid"
    _SESSION_ID = "sessionid"
    _IMG_TIMESTAMP = "timestamp"
    _IMG_EXTENSION = ".jpg"

    def __init__(self, received_image):
        """receives the full JSON arg, needs to parse class name and save to that file"""
        self._image_and_metadata = json.loads(received_image)
        self.save_datauri_as_jpg()

    def save_datauri_as_jpg(self):
        """stores incoming datauris in .jpg-format in class-specific directories"""
        inc_dir_path, storage_dir_path = self._get_path_to_classdirectory()
        decoded_image, image_name = self._decode_datauri()
        self._save_image_in_images_incoming(decoded_image, image_name, inc_dir_path, storage_dir_path)

    def _get_path_to_classdirectory(self):
        """check if session-id dir exists, create it if not, skip error if folder created between check and create"""
        dirname = self._image_and_metadata[self._SESSION_ID]
        path_to_inc_dir = util.IMAGES_INCOMING + "/" + dirname
        path_to_storage_dir = util.IMAGES_STORED + "/" + dirname
        self._ensure_classdirectories_exists(path_to_inc_dir, path_to_storage_dir)
        return path_to_inc_dir, path_to_storage_dir

    def _ensure_classdirectories_exists(self, path_to_inc_dir, path_to_storage_dir):
        """ensures the session folder exists in images_incoming and images_storage"""
        util.ensure_directory_exists(path_to_inc_dir)
        util.ensure_directory_exists(path_to_storage_dir)

    def _decode_datauri(self):
        """converts a base64 datauri to a jpg image, stores it in a classroom-specific directory"""
        data_uri = self._image_and_metadata[self._IMG_DATA][self._IMG_URI]
        image = base64.b64decode(data_uri)
        client_id = self._image_and_metadata[self._CLIENT_ID]
        timestamp = self._image_and_metadata[self._IMG_TIMESTAMP]
        image_name =  str(client_id) + str(timestamp) + str(self._IMG_EXTENSION)
        return image, image_name

    def _save_image_in_images_incoming(self, image, filename, inc_dir_path, storage_dir_path):
        """saves the interpreted base64 datauri as png in images_incoming,
        moves to images_processing when write done"""
        image_path_to_write_dir = inc_dir_path + "/" + filename
        image_path_to_storage_dir = storage_dir_path + "/" + filename
        with open(image_path_to_write_dir, 'wb') as image_on_disk:
            util.write_file(image, image_on_disk)
        util.move(image_path_to_write_dir, image_path_to_storage_dir)
