# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# imageUtility.py
#-------------------------------------------------------------------------------
# Software License
# The Python Imaging Library (PIL) is
#
#    Copyright © 1997-2011 by Secret Labs AB
#    Copyright © 1995-2011 by Fredrik Lundh
#-------------------------------------------------------------------------------

import os
from PIL import Image


class Parameters(object):
    # where to save thumnails and images
    thumbNailPath = r'C:\Users\codingCobra\Desktop\backgrounds'
    imagePath     = r'C:\Users\codingCobra\Desktop\backgrounds'
    # default parameters
    maxImageWidth = 900
    thumbHalfRez  = 200
    thumbWidth    = 110
    thumbHeight   = 90

class ImageResizer(object):
    """
        Utilities to Resize and Crop an image based on parameters.
        Supply a path to the image that needs processing.
    """
    WIDTH      = 'width'
    HEIGHT     = 'height'
    RESIZE     = 'resize'
    THUMB_NAIL = 'thumbNail'

    def __init__(self, imagePath, parameters):
        self.originalImage = self.__openImage(imagePath)
        self.image         = self.originalImage
        self.mode          = self.image.mode
        self.format        = self.image.format
        self.width         = self.image.size[0]
        self.height        = self.image.size[1]
        self.name          = self.__fileName(self.image)
        self.savePrefix    = 'resized_'
        self.thumbPrefix   = 'thumbnail_'
        self.parameters    = parameters

    def __getattr__(self, key):
        print 'ImageResizer has no attribute %s' % key

    def __delattr__(self, key):
        print 'You are not allowed to delete attributes.'

    #---------------------------------------------------------------------------
    # Methods
    #---------------------------------------------------------------------------

    def resizeImage(self, scaleBy=None, size=None):
        """
        Uniformally Resize an image by height or width.
        :param scaleBy: width or height
        :param size: pixels count
        :return:
        """
        sizeDefault = int(self.parameters.maxImageWidth)
        scaleBy     = self.WIDTH  if scaleBy is None else scaleBy
        size        = sizeDefault if size    is None else size
        self.__downRezImage(scaleBy, size)
        self.__saveImage(self.RESIZE)

    def createThumbNail(self):
        """
        Resize image to smaller size then crop based on parameters
        thumbWidth and thumbHeight
        :return:
        """
        halfRezWidth = int(self.parameters.thumbHalfRez)
        newWidth     = int(self.parameters.thumbWidth)
        newHeight    = int(self.parameters.thumbHeight)

        if self.width > halfRezWidth:
            self.__downRezImage(self.WIDTH, halfRezWidth)

        left  = (self.width  - newWidth) /2
        upper = (self.height - newHeight)/2
        right = (self.width  + newWidth) /2
        lower = (self.height + newHeight)/2

        box   = (left, upper, right, lower)

        self.image = self.image.crop(box)
        self.__saveImage(self.THUMB_NAIL)

    #---------------------------------------------------------------------------
    # Helpers
    #---------------------------------------------------------------------------

    def __saveImage(self, saveType):
        """
        Save processed image as thumbNail or resize.
        :param saveType: resize or thumbNail
        :return: boolean
        """
        if saveType == self.RESIZE:
            newName   = str(self.savePrefix) + str(self.name)
            savePath  = self.parameters.imagePath
        elif saveType == self.THUMB_NAIL:
            newName   = str(self.thumbPrefix) + str(self.name)
            savePath  = self.parameters.thumbNailPath

        imagePath = os.path.join(savePath, newName)
        try:
            self.image.save(imagePath, "JPEG")
            return True
        except IOError, e:
            raise IOError('Unable to save new image: %s' % str(e))

    def __downRezImage(self, region, size):
        """
        Resize image into memory before cropping.
        :param region: width or height
        :param size: pixels count
        :return:
        """
        if region == self.WIDTH:
            ratio     = float(size)/float(self.width)
            newWidth  = int(size)
            newHeight = int(self.height*ratio)
        if region == self.HEIGHT:
            ratio     = float(size)/float(self.height)
            newHeight = int(size)
            newWidth  = int(self.width*ratio)

        self.image  = self.image.resize((newWidth, newHeight), Image.ANTIALIAS)
        self.width  = newWidth
        self.height = newHeight

    #---------------------------------------------------------------------------
    # Statics
    #---------------------------------------------------------------------------

    @staticmethod
    def __openImage(image):
        """
        Open image using the PIL.
        :param image: path to image
        :return: PIL image obj
        """
        if os.path.isfile(image):
            try:
                return Image.open(image)
            except IOError:
                raise
        else:
            mssage = 'This is not a file'
            raise IOError(mssage)

    @staticmethod
    def __fileName(image):
        """
        Get the name of the image without the path.
        :param image: path to image
        :return: imageName.ext
        """
        return os.path.split(image.filename)[-1]


# example usages
path = r'C:\Users\codingCobra\Desktop\backgrounds\7YMpZvD.jpg'

image = ImageResizer(path, Parameters())
image.savePrefix  = 'resized-1_'
image.thumbPrefix = 'thumb-1_'
image.resizeImage(scaleBy='width', size=700)
image.createThumbNail()

image = ImageResizer(path, Parameters())
image.savePrefix  = 'resized-2_'
image.thumbPrefix = 'thumb-2_'
image.resizeImage(scaleBy='height', size=600)
image.createThumbNail()

image = ImageResizer(path, Parameters())
image.savePrefix  = 'resized-3_'
image.thumbPrefix = 'thumb-3_'
image.resizeImage()
image.createThumbNail()
