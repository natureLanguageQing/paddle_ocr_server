import base64
import logging
import os
import time
from urllib import request

import cv2
import numpy as np

from ocr_center import ocr

LOG_LEVEL = logging.INFO
LOG_DIR = "log"
LOG_FILE = "ocr.log"


def get_logger(name, log_file=LOG_FILE, level=LOG_LEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logsh = logging.StreamHandler()
    logsh.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    logsh.setFormatter(formatter)
    logger.addHandler(logsh)

    # file log
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)
    logfl = logging.FileHandler(os.path.join(LOG_DIR, log_file),
                                mode="w+", encoding="utf-8")
    logfl.setLevel(level)
    logfl.setFormatter(formatter)
    logger.addHandler(logfl)
    return logger


logger = get_logger(__name__)


def get_ocr_answer(urls=None, base64=""):
    images = []
    if urls and isinstance(urls, str):
        img_ndarray = _cvimg_from_url(urls)
        images.append(img_ndarray)
    if urls and isinstance(urls, list):
        for i in urls:
            img_ndarray = _cvimg_from_url(i)
            images.append(img_ndarray)
    if base64 and isinstance(base64, str):
        img_nd_array = _cvimg_from_base64(base64)
        images.append(img_nd_array)

    start_time = time.time()
    if images:
        print("start ocr")
        result = []
        for i in images:
            ocr_result = ocr.ocr(i)
            print("ocr_result", ocr_result)
            result.append(ocr_result)
        print("end_time", time.time() - start_time)
        return result


def _cvimg_from_path(image_path):
    try:
        img = cv2.imread(image_path)
        return img

    except Exception as e:
        logger.error("can't read image file!error{}", e)


def _cvimg_from_base64(image):
    try:
        if image.startswith("data:image/"):
            image = image.split(",")[1]
        img = base64.b64decode(image)
        img = np.fromstring(img, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    except:
        logger.error("base64 decode failed!")


def _cvimg_from_url(image_url):
    """

    :param image:
    :return:
    """
    try:

        req = request.Request(url=image_url, headers={"User-Agent": "Python 3.6"})
        with request.urlopen(req) as res:
            img = np.asarray(bytearray(res.read()), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    except Exception as e:
        logger.error("url {} data invalid!".format(image_url))
        print(e)
