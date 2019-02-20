from main.src.logger import logger
from main.src.config import my_config
import sys, os


class File_Manager:

    def __init__(self):
        base = os.path.expanduser("~")
        self.parent_dir = my_config.get("filemanager", "parent_directory")
        self.parent_dir = os.path.join(base, self.parent_dir)
        self.image_dir  = os.path.join( self.parent_dir, my_config.get("filemanager", "image_directory") )
        self.bin_dir    = os.path.join( self.parent_dir, my_config.get("filemanager", "bin_directory") )

        File_Manager.debug("Initializing file manager")
        if not os.path.isdir(self.parent_dir):
            os.mkdir(self.parent_dir)
        if not os.path.isdir(self.image_dir):
            os.mkdir(self.image_dir)
        if not os.path.isdir(self.bin_dir):
            os.mkdir(self.bin_dir)


    def list_images(self):
        imgs = os.listdir(self.image_dir)
        for img in imgs:
            img = os.path.join(self.image_dir, bin)
        return imgs


    def list_bins(self):
        bins = os.listdir(self.bin_dir)
        for bin in bins:
            bin = os.path.join(self.bin_dir, bin)
        return bins


    @staticmethod
    def debug(*args):
        logger.debug("File_Manager", *args)

    @staticmethod
    def error(*args):
        logger.error("File_Manager", *args)


# File manager object
my_filemanager = File_Manager()

