#!/usr/bin/python

import hug
from image_converter import ImageConverter


PULSE = "I'm alive!"
IMAGE_RECEIVED = "ok"
UNABLE_TO_PARSE = "not_ok: "


@hug.get('/pulse')
def test_response():
    """used for manually checking the api is up and running"""
    return PULSE


@hug.post('/post')
def receive_image(body):
    """stores the incoming datauri as png"""
    try:
        imageconverter = ImageConverter(body)
        return IMAGE_RECEIVED
    except Exception as failed_to_read:
        return UNABLE_TO_PARSE + failed_to_read
