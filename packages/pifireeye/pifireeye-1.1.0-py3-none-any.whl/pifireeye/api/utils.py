import cv2
from PIL import Image as PImage
import numpy as np
from picompress.compressor import Compressor
import matplotlib.pyplot as plt
from ..models.image import *
from datetime import datetime


def _caculate_background_percentage(img, mode='bgr',
                                    lower_bound=(70, 0, 0),
                                    upper_bound=(255, 255, 255)):
    if mode.lower() == 'bgr':
        hsv_nut = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif mode.lower() == 'rgb':
        hsv_nut = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    else:
        raise ValueError('Unknown color space!')
    mask = cv2.inRange(hsv_nut, lower_bound, upper_bound)
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    gray_img = cv2.cvtColor(masked_img, cv2.COLOR_RGB2GRAY)
    percent = np.count_nonzero(gray_img) * 1.0 / np.prod(gray_img.shape)
    return percent


def _show_hsv_image(img,
                    lower_bound=(70, 0, 0),
                    upper_bound=(255, 255, 255)):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)
    fig = plt.figure()
    hsv_plot = fig.add_subplot(1, 3, 1, projection='3d')

    hsv_plot.scatter(h.flatten(), s.flatten(), v.flatten(),
                     # facecolors=pixel_colors,
                     marker=".")
    hsv_plot.set_xlabel("Hue")
    hsv_plot.set_ylabel("Saturation")
    hsv_plot.set_zlabel("Value")

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    raw_plot = fig.add_subplot(1, 3, 2)
    raw_plot.imshow(rgb_img)

    mask_plot = fig.add_subplot(1, 3, 3)
    mask = cv2.inRange(hsv_img, lower_bound, upper_bound)
    masked_img = cv2.bitwise_and(rgb_img, rgb_img, mask=mask)
    mask_plot.imshow(masked_img)

    gray_img = cv2.cvtColor(masked_img, cv2.COLOR_RGB2GRAY)
    percent = np.count_nonzero(gray_img) * 1.0 / np.prod(gray_img.shape)
    print(percent)
    plt.show()


def validate_image(img, mode='bgr',
                   lower_bound=(70, 0, 0),
                   upper_bound=(255, 255, 255),
                   min_percent=0,
                   max_percent=0.8):
    bg = _caculate_background_percentage(img,
                                         mode,
                                         lower_bound,
                                         upper_bound)
    if min_percent < bg < max_percent:
        return True
    else:
        return False


def upload_training_images(image_api, platform_id, images, task_category_ids,
                           truth_ids, slots, platform_key, size=(120, 80, 3)):
    assert len(images) == len(task_category_ids), 'Num of images should' \
                                                  ' be equal with categ' \
                                                  'ory ids'
    assert len(images) == len(truth_ids), 'Num of images should ' \
                                          'be equal with truth ids'
    swagger_imgs = []
    for pixels, task_category_id, truth_id, slot in zip(images,
                                                        task_category_ids,
                                                        truth_ids,
                                                        slots):
        img = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)
        img = PImage.fromarray(img)
        # 调整分辨率
        img = img.resize(size[:2], PImage.ANTIALIAS)
        compressed = [x for x in Compressor.compress(img.tobytes())]
        swagger_img = Image(pixels=compressed, size=size, mode='RGB',
                            time=datetime.now().timestamp(),
                            task_category_id=task_category_id,
                            truth_id=truth_id,
                            platform_id=platform_id,
                            slot=slot,
                            confidence=100)
        swagger_imgs.append(swagger_img)
    image_api.upload_images(swagger_imgs, True, False, platform_key=platform_key)


def upload_testing_images(image_api, platform_id, images, task_category_ids, slots, platform_key,
                          save=False, size=(120, 80, 3)):
    assert len(images) == len(task_category_ids), 'Num of images should' \
                                                  ' be equal with categ' \
                                                  'ory ids'
    swagger_imgs = []
    for pixels, task_category_id, slot in zip(images,
                                              task_category_ids,
                                              slots):
        img = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)
        img = PImage.fromarray(img)
        # 调整分辨率
        img = img.resize(size[:2], PImage.ANTIALIAS)
        compressed = [x for x in Compressor.compress(img.tobytes())]
        swagger_img = Image(pixels=compressed, size=size, mode='RGB',
                            time=datetime.now().timestamp(),
                            task_category_id=task_category_id,
                            platform_id=platform_id,
                            slot=slot)
        swagger_imgs.append(swagger_img)
    return image_api.upload_images(swagger_imgs, save=save, detect=True, platform_key=platform_key)
