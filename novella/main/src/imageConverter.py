import sys, os, time
from PIL import Image
from main.src.config import  my_config
from main.src.filemanager import my_filemanager
from main.src.logger import logger

# Image object
class ImageConverter:
    def __init__(self):
        self.new_width = my_config.get("image", "new_width")
        self.new_height = my_config.get("image", "new_height")
        self.fixed_length = 88

    def convert_image(self, imagename):
        ImageConverter.debug("Converting image {}".format(imagename))
        imgname = os.path.join( my_filemanager.image_dir, imagename)
        self.isImage = False
        outputFile = " "
        retbin = ""
        try:
            self.im = Image.open(imgname)
            self.owidth, self.oheight = self.im.size
            self.info = self.im.info
            temp = imagename.split('.')[0] + '.bin'
            retbin = temp
            outputFile = os.path.join(my_filemanager.bin_dir, temp)
        except Exception as e:
            ImageConverter.debug(e)
            return None

        newWidth = int(self.owidth * self.fixed_length / self.oheight)
        newSize = newWidth, self.fixed_length

        self.im = self.im.convert('RGB')    # convert to rgb
        self.im = self.im.resize(newSize, Image.ANTIALIAS)     # resize to thumbnail
        self.im = self.im.rotate(90, expand=True)

        data = list(self.im.getdata())

        if os.path.isfile(outputFile):      # delete file if already exists
            os.remove(outputFile)

        with open(outputFile, 'wb') as myf:
            myf.write( newWidth.to_bytes(1, byteorder='big') )  # Write no of columns to file
            for pixel in data:          # iterate through all the pixels
                for col in pixel:       # iterate through all the colors 
                    tem = int(col)
                    myf.write( tem.to_bytes(1, byteorder='big') )

        ImageConverter.debug("IMAGE: Bin file generated ..")
        return retbin


    @staticmethod
    def debug(*args):
        logger.debug("ImageConverter", *args)


    @staticmethod
    def error(*args):
        logger.error("ImageConverter", *args)


# class object
my_imageConverter = ImageConverter()

