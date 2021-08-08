#!/usr/bin/env python

import io
import re
from copy import copy
from os import path
from typing import Any, Dict, List, Tuple, Union
from urllib.request import urlopen

import face_recognition
import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
from PIL import Image, ImageDraw, ImageOps

matplotlib.use('Qt5Agg')

PILImage = Image.Image
FaceLandmarks = List[Dict[str, List[Tuple[Any, ...]]]]


class FaceIsNotDetected(Exception):
    """[summary]

    Args:
        Exception ([type]): [description]
    """
    pass


class FaceSym:
    """[summary]
    """
    SimImages = Tuple[PILImage, PILImage, PILImage,
                      PILImage, PILImage, PILImage]

    def __init__(self, img_location: str) -> None:
        """[summary]

        Args:
            img_location (str): [description]

        Raises:
            ValueError: [description]
        """
        self.image_location = img_location
        if self.__is_valid_url(img_location):
            self.__load_from_url(img_location)
        elif path.isfile(img_location):
            self.__load_from_local(img_location)
        else:
            raise ValueError(
                "'%s' is not a valid location of an image." % img_location)

        self.f_img_PIL = Image.fromarray(self.f_img)
        self.image_size: Tuple[int, int] = self.f_img_PIL.size
        self.face_locations = face_recognition.face_locations(self.f_img)
        self.face_landmarks = face_recognition.face_landmarks(self.f_img)
        self.mid_face_locations = self.__get_mid_face_locations(
            self.face_landmarks)
        self.face_count = len(self.face_locations)

    def get_cropped_face_images(self, show: bool = False) -> List[PILImage]:
        """[summary]

        Args:
            show (bool, optional): [description]. Defaults to False.

        Returns:
            List[PILImage]: [description]
        """
        images = []
        for face_location in self.face_locations:
            top, right, bottom, left = face_location
            cropped_face_img = self.f_img[top:bottom, left:right]
            pil_img = Image.fromarray(cropped_face_img)
            if show:
                plt.imshow(pil_img)
                plt.show()

            images.append(pil_img)

        return images

    def get_face_box_drawed_image(self, show: bool = False) -> PILImage:
        """[summary]

        Args:
            show (bool, optional): [description]. Defaults to False.

        Returns:
            PILImage: [description]
        """
        pil = copy(self.f_img_PIL)
        draw = ImageDraw.Draw(pil)
        for idx, (top, right, bottom, left) in enumerate(self.face_locations):
            name = str("%02d" % idx)
            mid_face = self.mid_face_locations[idx]

            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            _, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10),
                            (right, bottom)),
                           fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5),
                      name, fill=(255, 255, 255))

            draw.line(((mid_face[0], -10), mid_face,
                       (mid_face[0], self.image_size[0])),
                      fill=(255, 255, 0), width=10)
        del draw
        if show:
            plt.imshow(pil)
            plt.show()
        return pil

    def get_full_image(self, show: bool = False, is_pil: bool = False
                       ) -> Union[np.ndarray, PILImage]:
        """[summary]

        Args:
            show (bool, optional): [description]. Defaults to False.
            is_pil (bool, optional): [description]. Defaults to False.

        Returns:
            Union[np.ndarray, PILImage]: [description]
        """
        if show:
            plt.imshow(self.f_img)
            plt.show()

        if is_pil:
            return self.f_img_PIL
        else:
            return self.f_img

    def get_symmetrized_images(
            self, idx: int = 0, show: bool = False) -> SimImages:
        """[summary]

        Args:
            idx (int, optional): [description]. Defaults to 0.
            show (bool, optional): [description]. Defaults to False.

        Returns:
            SimImages: [description]
        """
        def get_concat_h(im1: PILImage, im2: PILImage) -> PILImage:
            dst = Image.new('RGB', (im1.width + im2.width, im1.height))
            dst.paste(im1, (0, 0))
            dst.paste(im2, (im1.width, 0))
            return dst

        face_count = len(self.mid_face_locations)
        if face_count < 1:
            raise FaceIsNotDetected
        elif face_count <= idx:
            raise IndexError('0 <= idx <= %d' % (face_count-1))
        else:
            mid_face = self.mid_face_locations[idx]

        cropped_left_img = self.f_img[
            0:self.image_size[1], 0:int(mid_face[0])]
        cropped_right_img = self.f_img[
            0:self.image_size[1], int(mid_face[0]):self.image_size[0]]

        pil_img_left = Image.fromarray(cropped_left_img)
        pil_img_left_mirrored = ImageOps.mirror(pil_img_left)
        pil_img_left_inner = get_concat_h(
            pil_img_left, pil_img_left_mirrored)
        pil_img_left_outer = get_concat_h(
            pil_img_left_mirrored, pil_img_left)

        pil_img_right = Image.fromarray(cropped_right_img)
        pil_img_right_mirrored = ImageOps.mirror(pil_img_right)
        pil_img_right_inner = get_concat_h(
            pil_img_right_mirrored, pil_img_right)
        pil_img_right_outer = get_concat_h(
            pil_img_right, pil_img_right_mirrored)

        if show:
            title = 'Symmetrized images (face: %d)' % idx
            sub_figttls = (
                'left_cropped', 'left_cropped_inner', 'left_cropped_outer',
                'right_cropped', 'right_cropped_inner', 'right_cropped_outer')
            axarr: np.ndarray
            f, axarr = plt.subplots(2, 3, num=title)
            f.suptitle(title)
            axarr[0, 0].set_title(sub_figttls[0])
            axarr[0, 1].set_title(sub_figttls[1])
            axarr[0, 2].set_title(sub_figttls[2])
            axarr[1, 0].set_title(sub_figttls[3])
            axarr[1, 1].set_title(sub_figttls[4])
            axarr[1, 2].set_title(sub_figttls[5])
            axarr[0, 0].imshow(pil_img_left)
            axarr[0, 1].imshow(pil_img_left_inner)
            axarr[0, 2].imshow(pil_img_left_outer)
            axarr[1, 0].imshow(pil_img_right)
            axarr[1, 1].imshow(pil_img_right_inner)
            axarr[1, 2].imshow(pil_img_right_outer)
            plt.show()

        return (pil_img_left, pil_img_left_inner, pil_img_left_outer,
                pil_img_right, pil_img_right_inner, pil_img_right_outer)

    def __load_from_url(self, url: str) -> None:
        """[summary]

        Args:
            url (str): [description]

        Raises:
            ValueError: [description]
        """
        if not self.__is_valid_url(url):
            raise ValueError("'%s' is not valid url" % url)
        else:
            img_data = io.BytesIO(urlopen(url).read())
            self.f_img = face_recognition.load_image_file(img_data)

    def __load_from_local(self, path_: str) -> None:
        if path.isfile(path_):
            self.f_img = face_recognition.load_image_file(path_)

    @staticmethod
    def __is_valid_url(url: str) -> bool:
        """[summary]

        Args:
            url (str): [description]

        Returns:
            bool: [description]

        Note:
            Copyright (c) Django Software Foundation and individual
            contributors. All rights reserved.
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
            r'[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    @staticmethod
    def __get_mid_face_locations(
            face_landmarks: FaceLandmarks) -> List[Tuple[int, int]]:
        """[summary]

        Args:
            face_landmarks (FaceLandmarks): [description]

        Returns:
            List[Tuple[int, int]]: [description]
        """
        def mean(lst: List[int]) -> int:
            return int(sum(lst)/len(lst))

        mid_faces = []
        for face_landmark in face_landmarks:
            if not('left_eye' in face_landmark
                   and 'right_eye' in face_landmark):
                raise ValueError('eye locations was missing.')
            l_e_xs = [i[0] for i in face_landmark["left_eye"]]
            l_e_ys = [i[1] for i in face_landmark["left_eye"]]
            r_e_xs = [i[0] for i in face_landmark["right_eye"]]
            r_e_ys = [i[1] for i in face_landmark["right_eye"]]
            mid_face = ((mean(l_e_xs)+mean(r_e_xs))//2,
                        (mean(l_e_ys)+mean(r_e_ys))//2,)
            mid_faces.append(mid_face)
        return mid_faces


def main() -> None:
    """[summary]
    """
    data = list(map(
        lambda x: "https://pbs.twimg.com/media/%s?format=jpg" % x,
        [
            "E7okHDEVUAE1O6i",  "E7jaibgUcAUWvg-",
            "E7jahEbUcAMNLdU",  "E7Jqli9VEAEStvs",
            "E7Jqk-aUcAcfg3o",  "E7EhGi2XoAsMrO5",
            "E5dhLccUYAUD5Yx",  "E5TOAqUVUAMckXT",
            "E4vK6e0VgAAksnK",  "E4Va7u4VkAAKde3",
            "E4A0ksEUYAIpynP",  "E3xXzcyUYAIX1dC",
            "E2zkvONVcAQEE_S",  "E1cBsxDUcAIe_LZ",
            "E1W4HTRVUAgYkmo",  "E1HbVAeVIAId5yP",
            "E09INVFUcAYpcWo",  "E0oh0hmUUAAfJV9"
        ]))
    success, fail = 0, 0
    for idx, link in enumerate(data):
        print("[%02d]" % idx, link, end='')
        f = FaceSym(link)
        if f.face_count != 0:
            print("=>Detected")
            f.get_symmetrized_images(show=True)
            success += 1
        else:
            print("=>Not Detected")
            fail += 1

    else:
        print("DATA: %d" % len(data), "OK: %d" % success, "NG: %d" % fail)


if __name__ == '__main__':
    main()
