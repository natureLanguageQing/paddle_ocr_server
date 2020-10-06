import base64
from urllib import request

import cv2
import numpy as np

from ocr_center import ocr
from ocr_center.utils import logger


def get_ocr_answer(urls=None):
    images = []
    result_ocr_dict = []

    if urls and isinstance(urls, str):
        img_nd_array = _cv_img_from_url(urls)
        images.append(img_nd_array)
    if urls and isinstance(urls, list):
        for i in urls:
            img_nd_array = _cv_img_from_url(i)
            images.append(img_nd_array)

    if images:
        ocr_result = ocr.ocr(img=images)
        for line in ocr_result:
            result_ocr_dict.append(
                {"left_top": line[0][0],
                 "left_button": line[0][1],
                 "right_top": line[0][2],
                 "right_button": line[0][3],
                 "word": line[1][0]})
    return result_ocr_dict


def _cv_img_from_base64(image):
    """

    :param image:图片的base64编码
    :return:
    """
    try:
        if image.startswith("data:image/"):
            image = image.split(",")[1]
        img = base64.b64decode(image)
        img = np.fromstring(img, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    except:
        logger.error("base64 decode failed!")


def _cv_img_from_url(image_url):
    """

    :param image_url: 图片对应的地址
    :return:
    """
    try:
        logger.info("base64 decode failed!{}".format(image_url))
        req = request.Request(url=image_url, headers={"User-Agent": "Python 3.6"})
        with request.urlopen(req) as res:
            img = np.asarray(bytearray(res.read()), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    except Exception as e:
        logger.error("url {} data invalid!".format(image_url))
        print(e)
