from getopt import error
import os
import cv2
import typing as t

class ImageDoesNotExist(ValueError):
    """ Raised when cant open image """
    pass

class ImageReadError(Exception):
    """ Raised when  """
    pass

class ImageSaveError(Exception):
    """ Raised when  """
    pass

class ImageManager():
    """
        Manager for images
    """
    errors = (ImageDoesNotExist, ImageReadError, ImageSaveError)

    def __init__(self, dir_to_save: str) -> None:
        self.__set_dir_to_save(dir_to_save)

    def __set_dir_to_save(self, dir_to_save: str):
        self.dir_to_save = dir_to_save

        if not os.path.isdir(dir_to_save):
            os.mkdir(dir_to_save)

    def is_img_exist(self, img_path: str) -> None:
        if not os.path.exists(img_path):
            raise ImageDoesNotExist(f"Image {img_path} does not exist")

    def read_img(self, img_path: str) -> any:
        self.is_img_exist(img_path)

        try:
            read_img = cv2.imread(img_path)
        except cv2.error:
            raise ImageReadError(f"Failed to read {img_path}, please, make sure if this file has image format")
        else:
            return read_img

    def save_img(self, read_img: any, img_name: str, img_res: str = "png") -> str:
        image_name = f"{img_name}.{img_res}"
        image_path = os.path.join(self.dir_to_save, image_name)
        try:
            saved = cv2.imwrite(image_path, read_img)
        except cv2.error:
            raise ImageSaveError(f"Failed to save {img_name}, please, make sure if this file has image format")
        else:
            if saved:
                return image_name
            else:
                raise ImageSaveError("Error ImageSaveError")
    
    def resave_img(self, img_path: str, img_name: str) -> str:
        read_img = self.read_img(img_path)
        try:
            new_img_name = self.save_img(read_img=read_img, img_name=img_name)
        except ImageSaveError:
            raise ImageSaveError(f"Failed to save {img_path}, please, make sure if this file has image format")
        else:
            return new_img_name
