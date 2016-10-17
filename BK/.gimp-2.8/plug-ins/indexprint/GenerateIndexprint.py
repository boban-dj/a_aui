#!/usr/bin/python2
# -*- coding: UTF-8 -*-

'''
Copyright

Elmar Sullock Enzlin at moroquendo@gmail.com
(C) 2009~2012 Utrecht, The Netherlands

This plugin was tested with Gimp V2.6/2.8
On PC configurations:   -windows XP 32bits
                        -Linux Ubuntu 12.04 LTS 32bits


software_license
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
'''

'''
VERSION HISTORY: see indexprint.py

to do list:
==> to do: total pages doesn't work on sorted directories with headings
==> to do: make filename and extension case insensitive, if yes filetype
        can be made much shorter
==> to do: sorting on selected exif
==> to do: sort on filename not on dirname.
==> meer exif informatie, datandtime hernoemen naar iets duidelijkers
==> dir met rare tekens wordt niet herkend als dit de eerste is,
    wel als het dieper in de boom zit.
==> to do: everything in mm confirm ISO standardisation??
==> to do: rename all variables to gui like for better understanding,
            perhaps using dict
==> to do: test on ufraw installed; UFRAW should be correct installed in
            the Gimp bin directory
'''

import os, gettext
import gimp
from gimpfu import *
import string
from math import ceil, floor
from operator import itemgetter, attrgetter


#==============================================================================
#================= localization with "indexprint.mo" ========================
#==============================================================================
APP = "indexprint"  
PO_DIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   APP), 'locale')
gettext.install(APP, PO_DIR, unicode=True)
# gettext.install("indexprint", gimp.locale_directory, unicode=True) 


#==============================================================================
#=========== function only used for testpurposes and error logging ============
#==============================================================================
def Log(text):
    '''
    Function used for testpurpose and error logging because 'print'
    doesn't work on windows systems.
    Aargh...: use cmd, go to the root, path should point to the Gimp bin then
    type at the prompt: "gimp-2.8 > error.txt 2>&1" without quotes of course.
    All the output of Gimp will be written in error.txt (here in the root path).
    
    Input: text to log
    Output: error file
    '''
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'errorlog/Error.log')
    f=file(filename, "a+")
    f.write(text+"\n")
    f.close()


#==============================================================================
#=============== Make an overview of the images and directorys ================
#==============================================================================
def LogFileName(text, save_to_location, filename, FirstRun):
    '''
    =============== Make an overview of the images and directorys =============
     input: text:              text to save
            save_to_location:  directory to save
            filename:      filename of the textfile is the same in the
                                registersection
            FirstRun:          bool, delete old file on first entry
     output: txt file with imagename and dirname where the image is located
    ===========================================================================
    '''
    Filename = (save_to_location + '/' + filename + '.txt')
    if (FirstRun == True):                  #delete old txt file if exist
        if (os.path.isfile(Filename) == True):
            os.remove(Filename)

    f=file(Filename, "a+")
    f.write(text + "\n")
    f.close()
    return


#==============================================================================
#===================== get exif information for caption =======================
#==============================================================================

# meer exif informatie, dateandtime hernoemen naar iets duidelijkers
def get_exif_info(image):
    '''
    ======================== get exif information =============================
    input: image:
    output: exif:   string of choosen exif information, if not available
                    'no exif data' will be returned; reserved space for the
                    string is two rows.
    ============================================================================
    '''
#    def get_selected_exif_info(image, exif_info)
#       '''
#       exif_info is a string with selected exif information
#       '''
#       if exif is_in_string exif_info add to exif_data string
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(image)
    try:
        metadata.read()
# ---select on exif data        
        try:
            tagDT = metadata['Exif.Image.DateTime'].value
            DT = str(tagDT)
        except:
            DT = '?'
            
        try:
            tagExposureTime = metadata['Exif.Photo.ExposureTime']
            nspeed = tagExposureTime.value.numerator
            dspeed = tagExposureTime.value.denominator
            if nspeed > dspeed: #exposuretime > 1 sec
                speed = str(dspeed / float(nspeed))
            else:
                nspeed = nspeed /nspeed
                dspeed = dspeed / nspeed
                speed = str(nspeed) + '/' + str(dspeed)
        except:
            speed = '?'

        try:
            tagFNumber = metadata['Exif.Photo.FNumber']
            ndia = tagFNumber.value.numerator
            ddia = tagFNumber.value.denominator
            FN = str(ndia / float(ddia))
        except:
            FN = '?'

        try:
            tagFLnumber = metadata['Exif.Photo.FocalLength']
            nFL = tagFLnumber.value.numerator
            dFL = tagFLnumber.value.denominator
            FL = str(nFL / float(dFL))
        except:
            FL = '?'
            
        try:
            tagISOSpeedratings = metadata['Exif.Photo.ISOSpeedRatings']
            iso = str(tagISOSpeedratings.value)
        except:
            iso = '?'

        #exif_data = str(tagDT)
        exif_data = ('DT:' + DT +'\n' + 'ISO' + iso + ';F' + FN + ';' + speed + 's' + ';FL' + FL)

    except:
        exif_data = 'no exif data'
    
    return exif_data

           
##        try:
##            tagMake = metadata['Exif.Image.Make']
##        except:
##            tagMake = 'No Manufacturer'
##
##        try:
##            tagModel  = metadata['Exif.Image.Model']
##        except:
##            tagModel = 'No Model'
##
##        try:
##            tagFlash = metadata['Exif.Photo.Flash']
##        except:
##            tagFlash = '?'
##
##        exif_data = ('ISO' + iso + ';F' + FN + ';' + speed + 'sec')
##        print exif_data
##    except:
##        exif_data = 'no exif data'
##        print 'no exif data'

#==============================================================================
#================= get images from eventually all dirs ========================
#==============================================================================
def get_images(FileType, original_location, include_subdirs,
               DirFileList, SortedImages, select_on_part_of_filename):
    '''
    ================== get images from eventually all dirs =====================
    input: FileType:          array contains one or more extensions
           original_location: directory to start
           include_subdirs:       bool to include subdirectory's too
           DirFileList:       bool to give a txt list of images with their dir
           SortedImages:      bool, sort images alphanumeric (a <> A !!)
           select_on_part_of_filename:       text string to make file selections
    output: images:           array with images
    ============================================================================
    '''
    # ==> to do: make filename and extension case insensitive, if yes filetype
    # can be made much shorter
    images = []
    if (include_subdirs == True):                       #include all subdirectory's
        for dirpath, dirnames, filenames in os.walk(original_location.decode(), topdown=True):
            #for dirpath, dirnames, filenames in os.walk(original_location.decode('idna'), topdown=True):
            # Log(dirpath)
            for filename in filenames:
                if select_on_part_of_filename.lower() in filename.lower():
                    basename, ext = os.path.splitext(filename)
                    if ((len(ext)>2) and (ext.lower() in FileType)): #15/11: case insensitive now
                        imagefile = os.path.join(dirpath, filename)
                        original_image = {'extension':ext.lower(),
                                          'base_name':basename.lower(),
                                          'image_file':imagefile.lower(),
                                          'dirpath':dirpath}
                        if os.path.isfile(imagefile):
                            images.append(original_image)
                            #Log(str(original_image))
                else:
                    continue
    else:                                           #only the choosen directory
        for filename in os.listdir(original_location.decode()):
            #for filename in os.listdir(original_location.decode('idna')):
            #Log(original_location)
            if select_on_part_of_filename.lower() in filename.lower():
                basename, ext = os.path.splitext(filename)
                if ((len(ext)>2) and (ext.lower() in FileType)):
                    imagefile = os.path.join(original_location, filename)
                    original_image = {'extension':ext.lower(),
                                        'base_name':basename.lower(),
                                        'image_file':imagefile.lower(),
                                        'dirpath':''}
                    if os.path.isfile(imagefile):
                        images.append(original_image)
                        #Log(str(original_image))
            else:
                continue

    # ==> to do: sorting on selected exif
    # ==> to do: sort on filename not on dirname.
    #Log(str(images))
    if (SortedImages == False):
        return images
    else:
        return sorted(images, key=itemgetter('image_file'))


#sorted(images, key=itemgetter('image_file',<item2>,.....)) sorteren op
#    meerdere items

# indien sorteren aan dan geen dir indeling/scheiding
# niet gesorteerd dan dir scheiding/indeling per dir
# dir met rare tekens wordt niet herkend als dit de eerste is, wel als het dieper
#   in de boom zit


# decode('idna') is working on windows
# on linux decode('mbcs') is unknown on windows it is a known :-( searching
# for an other solution
## for dirpath, dirnames, filenames in os.walk(original_location.decode('mbcs'),
#                                                           topdown=True):
## for filename in os.listdir(original_location.decode('mbcs')):

## for filename in os.listdir(original_location.decode('unicode_escape')):
## for filename in os.listdir(original_location.decode('mbcs')): #win only

#==============================================================================
#=================== sort images on several indexes ===========================
#==============================================================================
def sort_images(images, sortcriteria):
    '''
    ================ sort images on several given indexes =====================
    input: images:          array with images
           sortcriteria:    dictonary
    output: images:         array with sorted images
    ===========================================================================
    '''
    pass


#==============================================================================
#================= create a text list with file and dirnames ==================
#==============================================================================
#    input: images:            array contains the images etc.
#           save_to_location:  directory to save
#           filename:       name of the txt file
#    output: txt file with imagename and dirname were the image is located
#==============================================================================
def Make_DirFile_List(images, save_to_location, filename):
    files = images[0:len(images)]
    FirstRun = True
    for file in files:
        if FirstRun == True:
            directory_path = file['dirpath']
            text = file['dirpath']
            # Log(text)
            LogFileName(text, save_to_location, filename, FirstRun)
            FirstRun = False
            
        if directory_path == file['dirpath']:
            pass
        else:
            text = '' #linespace
            LogFileName(text, save_to_location, filename, FirstRun)
            text = file['dirpath']
            LogFileName(text, save_to_location, filename, FirstRun)
            directory_path = text #save dirpath
            
        text = file['base_name'] + file['extension']
        LogFileName(text, save_to_location, filename, FirstRun)


#==============================================================================
#=================== save index print as a png file ===========================
#==============================================================================
def save_png(image, drawable, new_filelocation, use_comment):
    compression = 9
    interlace, bkgd = False, False
    gama, offs, phys = False, False, False
    time, svtrans = True, False
    pdb.file_png_save2(image, drawable, new_filelocation, new_filelocation,
                       interlace, compression, bkgd, gama, offs, phys, time,
                       use_comment, svtrans) 

#==============================================================================
#=================== save index print as a jpg file ===========================
#==============================================================================
def save_jpeg(image, name, comment=""):
    jpeg_save_defaults = (0.85, 0.0, 1, 0, "", 1, 0, 0, 0)
    args = list(jpeg_save_defaults)
    args[4] = comment
    pdb.file_jpeg_save(image, image.active_layer, name, name, *args)


#==============================================================================
#========== calculate the size of a subminipage within a minipage =============
#==============================================================================
#input  AR              float, aspect ratio
#       MiniPage_x      int, size in pixels
#       MiniPage_y      int, size in pixels
#output SMPx            int, new size in px
#       SMPy            int, new size in px
#       offset_x        int, x offset subminipage
#       offset_y        int, y offset subminipage
#==============================================================================

# ==> to do: everything in mm ??
def CalcSubminipage(AR, MiniPage_x, MiniPage_y):
    if (AR >= 1):               #landscape
        SMPx = MiniPage_x
        SMPy = int(MiniPage_x/float(AR))
    else:                       #portrait
        SMPx = int(MiniPage_y*AR)
        SMPy = MiniPage_y

    offset_x = int((MiniPage_x - SMPx)/2)
    offset_y = int((MiniPage_y - SMPy)/2)

    return SMPx, SMPy, offset_x, offset_y


#==============================================================================
#========= resize and eventually rotate and crop photo to allowed size ========
#==============================================================================
# deze procedure ingeval indexprint: other then none
#------------------------------------
# input: filename:          photo to resize
#        MP_width:          int, size of minipage width in px
#        MP_height:         int, size of minipage height in px
#        image_rotate       bool, image rotate yes or no
#        aspect_ratio       int, photo has a fixed size or not
#        dpi:               for rendering eps/ps
# output: img:              resized photo
#         new[0]            int, x-size of the photo in px
#         new[1]            int, y-size of the photo in px
#==============================================================================

# ==> seperate loading ps/eps with dpi resolution due to a problem that
#       ps/eps always be rendered with default 100dpi. Use gimp_epsload,
#       see reference
#
# ==> to do: everything in mm ??
def generate_foto(filename, MP_width, MP_height, image_rotate, aspect_ratio, dpi):

    # Try to read the image. eps/ps will be rendered with dpi
    valid_image = True
    try:
        if ('.ps' in filename )or ('.eps' in filename):
            if dpi <= 200:
                dpi = 200   #a render less then 200 is very bad.
            
##            if '.eps' in filename:
##                Log('eps load')
##            elif '.ps' in filename:
##                Log('ps load')
##            else:
##                Log('geen postscript')

            pdb.file_ps_load_setargs(MP_width,MP_height,dpi,True,"1",7,1,1)
            #img = pdb.gimp_file_load(filename,filename)
            img = pdb.file_ps_load(filename,filename)
        else:
            #Log('andere file extensie')
            img = pdb.gimp_file_load(filename,filename)
    except RuntimeError:
        Log('Not a valid image: ' + filename)
        valid_image = False
        img=[]
        return img, 0, 0, valid_image

    minimum_scale = False
    maximum_scale = False
    MakeSMP = False
    if (image_rotate == True):            #rotate 90' if the longest side is vertical
        # not square
        if (img.height>img.width):
            pdb.gimp_image_rotate(img,0)    #rotate 90' to the right
            
        if (aspect_ratio == 6):             #none
            minimum_scale = True
        else:                               #ratio and fixed
            MakeSMP = True                  #nodig ??????
            maximum_scale = True
    else:
        # square
        if (aspect_ratio == 6):             #none
            minimum_scale = True
        else:                               #ratio and fixed
            MakeSMP = True
            maximum_scale = True

    if (MakeSMP == True):
        img_ratio = img.width/float(img.height)
        # img_ratio >=1 landscape else portrait
        AR, fixed_size, ImageSize_x, ImageSize_y = CalcAspect(aspect_ratio)
        if (img_ratio < 1):     # portrait
            AR = 1/AR
        #create subminipage with the desired dimensions;
        #is independend from image properties
        SMP_x, SMP_y, offset_x, offset_y = CalcSubminipage(AR, MP_width, MP_height)
        #now we have created a subminipage within a minipage with the correct
        #aspect ratio and dimensions SMP_x and SMP_y including the subminipage offset
    else:
        SMP_x = MP_width
        SMP_y = MP_height
        offset_x = 0
        offset_y = 0

    crop_y = False
    crop_x = False
    #define new scalefactors now from image
    scale_y = SMP_y/float(img.height)
    scale_x = SMP_x/float(img.width)
    if (minimum_scale == True):
        #lineair scale the image; just fit
        if (scale_x < scale_y):         #landscape; scale min in x
            new_x = int(img.width * scale_x)
            new_y = int(img.height * scale_x)
        else:                           #portrait; scale min in y
            new_y = int(img.height * scale_y)
            new_x = int(img.width * scale_y)
    else:                               # (maximum_scale == True):
        #now we have the image scaled in either the correct width or height
        #of the subminipage. The other side is larger and should therefor
        #be cropped in x or y
        if (scale_x < scale_y):         #scale max in y and crop in x
            new_x = int(img.width * scale_y)
            new_y = SMP_y
            crop_x = True
        else:
            new_y = int(img.height * scale_x)
            new_x = SMP_x
            crop_y = True

    #scale image (or is gimp_image_resize better ??????)
    pdb.gimp_image_scale(img, new_x, new_y)
        
    if (crop_x == True):
        offy = 0
        offx = int((new_x - SMP_x)/float(2))
        new_x = SMP_x
        pdb.gimp_image_crop(img, new_x, new_y, offx , offy)

    if (crop_y == True):
        offx = 0
        offy = int((new_y - SMP_y)/float(2))
        new_y = SMP_y
        pdb.gimp_image_crop(img, new_x, new_y, offx, offy) 
        
    return img, new_x, new_y, valid_image



#==============================================================================
#================= modify fontsize so it fits thumbwidth ======================
#==============================================================================

# ==> to do: everything in mm ??
def CalcFontSize(text,Font,Size,CalcTextHeight,max_width):
    #this procedure calculates the text size to fit within the
    #width param, the text is reduced until the width is small enough
    txtw,txtH,txte,txtd = pdb.gimp_text_get_extents_fontname(text,Size,PIXELS,Font)
    if (txtw<=max_width):
        return Size,txtw
    while ((txtw>max_width) and (Size>0)):
        Size = Size -1
        txtw,txtH,txte,txtd = pdb.gimp_text_get_extents_fontname(text,Size,
                                                                 PIXELS,Font)
    return Size,txtw


#==============================================================================
#===================== calculate papersize in pixels ==========================
#==============================================================================
#input: Contactsize     papersize text (given in mm)
#       dpi             desired resolution
#       orient          text of paperorientation
#output:width           width in pixels of the papersize
#       height          height in pixels of the papersize
#==============================================================================

# ==> to do: everything in mm confirm ISO standardisation
# a point pt=0.375 mm not 0.376mm(!) sinc 1973, see wiki on typographic

def CalcPaperSize(ContactSize, dpi, orient, paper_height, paper_width):
    if (ContactSize == "Jumbo"):          #Jumbo
        width,height = (102,152)
    elif (ContactSize == "6x8"):          #6x8
        width,height = (152,203)
    elif (ContactSize == "8x10"):         #8x10
        width,height = (203,254)
    elif (ContactSize == "A5"):           #A5
        width,height = (148,210)    
    elif (ContactSize == "A4"):           #A4
        width,height = (210,297)
    elif (ContactSize == "A3"):           #A3
        width,height = (297,420)
    elif (ContactSize == "A2"):           #A2
        width,height = (420,594)
    elif (ContactSize == "A1"):           #A1
        width,height = (594,841)
    elif (ContactSize == "A0"):           #A0
        width,height = (841,1189)        
    elif (ContactSize == "Letter"):       #Letter
        width,height = (216,279)
    elif (ContactSize == "Legal"):        #Legal
        width,height = (216,356)
    elif (ContactSize == "Tabloid"):      #Tabloid
        width,height = (279,432)
    elif (ContactSize == "banner1"):      #banner A4 width
        width,height = (210,1000)
    elif (ContactSize == "banner2"):      #banner A3 width
        width,height = (297,1000)
    elif (ContactSize == "custom"):       #free sizes
        width,height = (paper_width, paper_height)
    else:
        width,height = (210,297)          #use default if in error
        Log("error in pagesize, pagesize doesnot exist: " + ContactSize)

    # calculate width and height in px, both are floored
    if (orient == "land"):
        Height = int(width * dpi / 25.4)
        Width = int(height * dpi / 25.4)

    else:
        Width = int(width * dpi / 25.4)
        Height = int(height * dpi / 25.4)

    return Width, Height                    #size in pixels (integer)


#==============================================================================
#================== calculate aspectratio, size, etc  =========================
#==============================================================================
#input: AspectRatio         int number (from input, choice)
#output:AR                  float, aspect ratio
#       ImageSize_x         int, maximum width in mm for fixed_sizes only
#       ImageSize_y         int, maximum height in mm for fixed_sizes only
#       fixed_size          bool, 
#==============================================================================
## most common aspect ratio's (bxh = width x height)
##  4:3 -> TV
##  16:9 -> movie
##  3:2 -> SLR digital camera
##  5:4
##  6:7
##  1:1
##  none -> maximum size depends on paper, #rows and #columns
##
## otherwise predefined papersizes (bxh)
## 7x10 cm  ->
## 9x12 cm  ->
## 10x15 cm  ->
## 13x18 cm  ->
## 18x24 cm  ->
## else??
#==============================================================================
def CalcAspect(AspectRatio):
    fixed_size = False
    #---  The tallest size should be noted first (=width)!!
    #--- this section contains the non-fixed formats
    if (AspectRatio == 0):                      #1:1 (bxh)
        ImageSize_x,ImageSize_y = (1,1)         #float, desired ratio
    elif (AspectRatio == 1):                    #3:2
        ImageSize_x,ImageSize_y = (3,2)
    elif (AspectRatio == 2):                    #4:3
        ImageSize_x,ImageSize_y = (4,3)
    elif (AspectRatio == 3):                    #5:4
        ImageSize_x,ImageSize_y = (5,4)
    elif (AspectRatio == 4):                    #6:7
        ImageSize_x,ImageSize_y = (6,7)
    elif (AspectRatio == 5):                    #16:9
        ImageSize_x,ImageSize_y = (16,9)
    elif (AspectRatio == 6):                    #none, default to 4:3
        ImageSize_x,ImageSize_y = (4,3)
# --- this section contains the fixed formats in mm (bxh)
    elif (AspectRatio == 7):                    #7x10 cm predefined section
        fixed_size = True
        ImageSize_x,ImageSize_y = (100,70)
    elif (AspectRatio == 8):                    #9x13 cm
        fixed_size = True
        ImageSize_x,ImageSize_y = (127,89)        
    elif (AspectRatio == 9):                    #10x15 cm
        fixed_size = True
        ImageSize_x,ImageSize_y = (152,102)
    elif (AspectRatio == 10):                   #13x18 cm
        fixed_size = True
        ImageSize_x,ImageSize_y = (178,127)        
    elif (AspectRatio == 11):                   #18x24 cm
        fixed_size = True
        ImageSize_x,ImageSize_y = (240,180)
    else:
        fixed_size = False
        ImageSize_x,ImageSize_y = (4,3)         #none is the default
        Log("Error in routine CalcAspect, size doesn't exist.")

    AR =  ImageSize_x/float(ImageSize_y)        #float AR

    return AR, fixed_size, ImageSize_x, ImageSize_y

#==============================================================================
#================== calculate maximum photosize in pixels =====================
#==============================================================================
#input: CanvasWidth         canvaswidth in px
#       numcols             int number of columns
#       AspectRatio         int number (from input, choice)
#       PhotoMargin         margin in pixels
#       dpi                 int, resolution in px/inch
#output:MaxPhotoWidth       maximum width in pixels
#       MaxPhotoHeight      maximum height in pixels
#==============================================================================
def CalcMaxPhotoSize(CanvasWidth, numcols, AspectRatio, ImageMargin, dpi):
    
    AR, fixed_size, ImageSize_x, ImageSize_y = CalcAspect(AspectRatio)

    if (fixed_size == False):
        ImageSize_x = int((CanvasWidth-numcols*2*ImageMargin)/float(numcols))
        ImageSize_y = int(ImageSize_x / float(AR))     #resize y, x is oke

        MaxImageWidth = ImageSize_x     #sizes are now conform the aspect ratio
        MaxImageHeight = ImageSize_y
    else:                                       #fixed_size is true
        MaxImageWidth = int(ImageSize_x * dpi / float(25.4))
        MaxImageHeight = int(ImageSize_y * dpi / float(25.4))

    return MaxImageWidth, MaxImageHeight        #sizes are in px (integers)


#==============================================================================
#======================== calculate usable cols, rows =========================
#==============================================================================
#input: CanvasWidth         canvaswidth in px
#       CanvasHeight        canvasheight in px
#       numcols             int number of columns
#       numrows             int number of rows
#       AspectRatio         int number
#       PhotoMargin         margin in pixels
#output:UsableRows          int, maximum number of rows
#       UsableCols          int, maximum number of cols
#==============================================================================
def CalcMaxColsRows(CanvasWidth, CanvasHeight, numcols, numrows, AspectRatio,
                    PhotoMargin, MP_width, MP_height, Inc_FileName,
                    exif_dateandtime, FontSize):

    if ((Inc_FileName == True) and (exif_dateandtime == True)):
        ExtraSize = 3 * FontSize
    elif ((Inc_FileName == True) and (exif_dateandtime == False)):
        ExtraSize = FontSize
    elif ((Inc_FileName == False) and (exif_dateandtime == True)):
        ExtraSize = 2 * FontSize
    else:
        ExtraSize = 0
    
    UsableRows = floor(CanvasHeight/(MP_height + ExtraSize + 2*PhotoMargin))
    
##    if (Inc_FileName == True):
##        UsableRows = floor(CanvasHeight/(MP_height + FontSize + 2*PhotoMargin))
##    else:
##        UsableRows = floor(CanvasHeight/(MP_height + 2*PhotoMargin))
    
    #Number of chosen rows can never be bigger then usable rows
    if (numrows <= UsableRows):
        UsableRows = numrows

    UsableCols = numcols
    if (AspectRatio > 6):
        UsableCols = floor(CanvasWidth/(MP_width + 2*PhotoMargin))
        #Number of chosen cols can never be bigger then usable cols
        #only for fixed sizes
        if (numcols <= UsableCols):
            UsableCols = numrows
    
    return UsableRows,UsableCols


#==============================================================================
#============================ calculate margins ===============================
#==============================================================================
#input: PBorderL            int, top margin in mm
#       PBorderR            int, top margin in mm
#       PBorderB            int, top margin in mm
#       PBorderT            int, top margin in mm
#       mmFontSize          int, captionfont size in mm
#       mmThumbMargin       int, thumbmargin in mm
#       dpi                 int, resolution
#output:LPB                 left page border in px
#       RPB                 right page border in px
#       BPB                 bottom page border in px
#       TPB                 top page border in px
#       FS                  captionfont size in px
#       TM                  thumb margin in px
#==============================================================================

# extend with fontsize header and pagenumber
# canvas size = thumb's + header +pagenumber
# canvas size for thumb's to be calculated

def CalcMargins(PBorderL, PBorderR, PBorderB, PBorderT, mmFontSize,
                mmThumbMargin, dpi):
    LPB = int(PBorderL * dpi / float(25.4))   
    RPB = int(PBorderR * dpi / float(25.4))
    BPB = int(PBorderB * dpi / float(25.4))
    FS  = int(mmFontSize * dpi / float(25.4))
    
    aligned = False   #photoprint plugin for easy cutting; not implemented yet
    if (aligned == True):
        TPB = int(PBorderT * dpi / float(25.4))     #exclude sheet .. of ..
    else:                                           #include sheet .. of ..
        TPB = int(PBorderT * dpi / float(25.4)) + FS
        
    TM  = int(mmThumbMargin * dpi / float(25.4))
    
    return LPB,RPB,BPB,TPB,FS,TM                    # in px


#==============================================================================
#==================== calculate size of the minipage ==========================
#================ Images are placed within the minipages ======================
#==============================================================================
#input: Canvas_width            int, in px
#       Canvas_height           int, in px
#       num_col                 int, #columns
#       num_rows                int, #rows
#       TM                      int, image margin in px
#       aspect_ratio            int, ratio (from input)
#output:MP_width                int, width of minipage in px
#       MP_height               int, height of minipage in px
#==============================================================================
def CalcMinipage(CanvasWidth, numcols,ImageMargin, AspectRatio, image_rotate, dpi):

    MP_width, MP_height = CalcMaxPhotoSize(CanvasWidth, numcols, AspectRatio,
                                           ImageMargin, dpi)
    if (image_rotate == False):               #not aligned so minipage is square
        MP_height = MP_width

    return MP_width, MP_height


#==============================================================================
#================= main routine generate contact sheet ========================
#==============================================================================
##
##  ==> to do: rename all variables to gui like for better understanding
##
def contactsheet(file_type, select_on_part_of_filename,
        open_from_location, include_subdirs,
        save_to_location, filename, contact_type,
        paper_size, paper_height, paper_width,
        orient, dpi,
        page_with_background, page_rb_bg_solidcolor,
        page_background_color,
        page_background_image, page_background_image_opacity, 
        page_with_header, page_header, page_header_font, page_header_color,
        with_pagenumber, pagenumber, pagenumber_font, pagenumber_color, total_pages,
        topmargin, bottommargin, leftmargin, rightmargin,
        num_col, num_rows,
        image_whiteborder, aspect_ratio, image_rotate,
        mmFONT_SIZE, caption_font, caption_font_color,
        inc_filename, inc_extension,
        exif_dateandtime,
        Dump_Filename_list, Print_Contactsheet,
        Sorted_Images):    
    '''
    *****input:
    file_type:                  string of file extensions to read
    select_on_part_of_filename: select on part of filename
    open_from_location:         read directory
    include_subdirs:            include all subdirectories
    save_to_location:           save into the given directory
    filename, contact_type:     name of indexprint file and extension
    paper_size:                 size of the indexprint (page or sheet)
    paper_height, paper_width:  size of the paper
    dpi, orient:                page resolution and orientation
    page_with_background:       boolean background y/n
    page_rb_bg_solidcolor:      boolean solid or image (y/n)
    page_background_color:      page background color
    page_with_header            boolean header y/n
    page_header:                title text on the page
    with_pagenumber             boolean pagenumber y/n
    pagenumber, total_pages:    pagenumber and include total pages
    topmargin, bottommargin,leftmargin, rightmargin: page margins
    num_col, num_rows:          number of columns and rows
    image_whiteborder:          whiteborder
    aspect_ratio, image_rotate: aspect ratio or size and image rotating
    mmFONT_SIZE:                caption fontsize
    inc_filename, inc_extension: include filename and extension (caption)
    exif_dateandtime:           include exif information
    Dump_Filename_list:         include filenamelist
    Print_Contactsheet:         direct printing
    Sorted_Images:              images sorted

    *****ouput:
    set of index prints
    '''

    ## collect 'all' images in the choosen directory and subdirs
    ## eventualy sorted
    images = get_images(file_type, open_from_location, include_subdirs,
                        Dump_Filename_list, Sorted_Images, select_on_part_of_filename)
    num_images = len(images)                        #calculate number of images
    
    ## if necessary make a txt file with image name and image directory
    if (Dump_Filename_list == True):
        Make_DirFile_List(images, save_to_location, filename)

    ## Margin/font sizes are in px and floored with maximum error of one px
    ##        fontsizes are now individual
    LPB,RPB,BPB,TPB,FS,TM = CalcMargins(leftmargin, rightmargin, bottommargin,
                                        topmargin, mmFONT_SIZE, image_whiteborder,
                                        dpi)
    ## er is een canvas voor thumbs + header + pagenumber; header en pagenumber fontsizes
    ## en er is de thumb canvas size hier onderscheid in maken.
    
    ## calculate canvas size in px (the printable sheet dimensions)
    width,height = CalcPaperSize(paper_size, dpi, orient, paper_height,
                                 paper_width) #dimensions in px
    Canvas_width = width - LPB - RPB
    Canvas_height = height - BPB - TPB
    
    # define size of the minipage. Images are centered placed within a minipages
    # if image_rotate = False MPx=MPy else they differ; sizes are in px
    MPx, MPy = CalcMinipage(Canvas_width, num_col,TM, aspect_ratio, image_rotate, dpi)
    
    # calculate the maximum allowable columns and rows
    UseableRows,UseableCols = CalcMaxColsRows(Canvas_width, Canvas_height, num_col,
                                              num_rows, aspect_ratio, TM, MPx, MPy,
                                              inc_filename, exif_dateandtime, FS)

    ThumbsPerSheet = int(UseableCols*UseableRows)
    img_no = 1
    for sheetcount in range(int(ceil(num_images/float(ThumbsPerSheet)))):
        sheetimg = gimp.Image(width,height,RGB)
        bklayer = gimp.Layer(sheetimg,"Background",width,height,RGB_IMAGE,
                             100,NORMAL_MODE)
        sheetimg.disable_undo()
        sheetimg.add_layer(bklayer,0)
        sheetimg.resolution = (float(dpi), float(dpi))      #why float ?????

        #-- check if background
        if page_with_background:
            if page_rb_bg_solidcolor:
                # fill background with a solid color
                gimp.set_background(str(page_background_color))
                bklayer.fill(BACKGROUND_FILL)
                bklayer.flush()
            else:
                bklayer.fill(WHITE_FILL)
                bklayer.flush()
                # Load an image as a new layer
                BGLayer = pdb.gimp_file_load_layer(sheetimg, page_background_image)
                # BGLayer = pdb.gimp_file_load_layer(sheetimg, page_background_image.decode('unicode_escape'))
                pdb.gimp_image_add_layer(sheetimg, BGLayer, -1)
                # scale BGLayer to sheetimg size
                pdb.gimp_layer_scale(BGLayer, width, height, 0)
                pdb.gimp_layer_set_opacity(BGLayer, page_background_image_opacity)
                pdb.gimp_image_flatten(sheetimg)
        else:
            # if no background make background white
            bklayer.fill(WHITE_FILL)
            bklayer.flush()
        
        sheetdsp = gimp.Display(sheetimg)

        gimp.displays_flush()
        mid = width/2

        # ==> to do: total pages doesn't work on sorted on directories with headings
        if total_pages == True:
            total_pages_text = _("Sheet %03d of %03d")
            #--- test pagenumber with different fonts
            #--print(pagenumber_color)
            pdb.gimp_palette_set_foreground(pagenumber_color)
            #pdb.gimp_rgb_set(0.5, 0.5, 0.5)
            txtw,CalcTextHeight,txte,txtd = pdb.gimp_text_get_extents_fontname(
		total_pages_text % (sheetcount+1, int(ceil(num_images/float(ThumbsPerSheet)))),
		FS,PIXELS, pagenumber_font)
##            txtw,CalcTextHeight,txte,txtd = pdb.gimp_text_get_extents_fontname(
##		total_pages_text % (sheetcount+1, int(ceil(num_images/float(ThumbsPerSheet)))),
##		FS,PIXELS,"Arial")
            
            x_text = mid - txtw/2
            y_text = TPB-CalcTextHeight
            #--- page number with total pages if checked
            #text_layer = gimp_text_fontname (image,drawable,x,y,text,border,
            #                                   antialias,size,size_type,fontname)
            txtfloat = pdb.gimp_text_fontname(sheetimg, sheetimg.active_layer,
                            x_text, height-TPB,
                            total_pages_text % (sheetcount+1, int(ceil(num_images/float(ThumbsPerSheet)))),
                            -1, False, FS, PIXELS, pagenumber_font)
##            txtfloat = pdb.gimp_text_fontname(sheetimg, sheetimg.active_layer,
##                            x_text, height-TPB,
##                            total_pages_text % (sheetcount+1, int(ceil(num_images/float(ThumbsPerSheet)))),
##                            -1, False, FS, PIXELS, "Arial")
            pdb.gimp_floating_sel_anchor(txtfloat)
        else:
            total_pages_text = _("Sheet %03d") #deze werkt nog niet
            txtw,CalcTextHeight,txte,txtd = pdb.gimp_text_get_extents_fontname(
                total_pages_text % (sheetcount+pagenumber), FS,PIXELS,pagenumber_font)
            
            x_text = mid - txtw/2
            y_text = TPB-CalcTextHeight
            
            txtfloat = pdb.gimp_text_fontname(sheetimg, sheetimg.active_layer,
                            x_text, height-TPB, total_pages_text % (sheetcount+pagenumber),
                            -1, False, FS, PIXELS, pagenumber_font)
            pdb.gimp_floating_sel_anchor(txtfloat)


        txtw,CalcTextHeight,txte,txtd = pdb.gimp_text_get_extents_fontname(page_header,
		FS,PIXELS,page_header_font)

        x_text = mid - txtw/2
        y_text = TPB-CalcTextHeight

        # place header text centered if checked
        print(page_header_color)
        pdb.gimp_palette_set_foreground(page_header_color)
        
        if page_with_header == False:
            y_text = 0  # dummy statement
        else:   # center header
            txtfloat = pdb.gimp_text_fontname(sheetimg, sheetimg.active_layer,
                            x_text, y_text, page_header, -1, False,
                            FS, PIXELS, page_header_font)
            pdb.gimp_floating_sel_anchor(txtfloat)

        
        CalcTextHeight =0
        txtw,txth,txte,txtd = (0,0,0,0)
        if (inc_filename == True):
            txtw,CalcTextHeight,txte,txtd = pdb.gimp_text_get_extents_fontname(
                images[0]['base_name'], FS, PIXELS, caption_font)

        if (exif_dateandtime == True):
            txtw,ExifTextHeight,txte,txtd = pdb.gimp_text_get_extents_fontname(
                'none', FS, PIXELS, caption_font)
            CalcTextHeight = CalcTextHeight + 2 * ExifTextHeight
            
        files = images[sheetcount*ThumbsPerSheet:(sheetcount+1)*ThumbsPerSheet]
        
        #now for each of the image files generate a thumbnail
        rcount = 0      # row counter
        ccount = 0      # column counter
        pdb.gimp_palette_set_foreground(caption_font_color)
        for file in files:
            thumbimg,x_size,y_size,valid_image = generate_foto(file['image_file'],
                                                MPx, MPy, image_rotate, aspect_ratio, dpi)
            if valid_image == False:
                continue                                #next image

            #read exif date and time if possible
            if exif_dateandtime == True:
                dateandtime = get_exif_info(file['image_file'])
            
            cpy = pdb.gimp_edit_copy(thumbimg.active_layer)
            # center image within its minipage
            if (x_size >= y_size):
                # landscape image or square, center vertical
                y_offset = int((MPy - y_size)/2)
                x_offset = 0
            else:
                # portrait image, center horizontal
                x_offset = int((MPx - x_size)/2)
                y_offset = 0

            gimp.delete(thumbimg)
            #now paste the new thumb into contact sheet
            newselect = pdb.gimp_edit_paste(sheetimg.active_layer, True)

            #positition in top left corner 
            newselect.translate(-newselect.offsets[0],-newselect.offsets[1])
            #now place in correct position, modified with x- and y-offset
            xpos = LPB + ccount * (MPx + (2 * TM)) + TM  + x_offset
            ypos = TPB + rcount * (MPy + (2 * TM)  + CalcTextHeight) + TM + y_offset
            xpos = int(xpos)    #05/12/2011 changed to int: on ubuntu type error integer expected got float.
            ypos = int(ypos) 
            newselect.translate(xpos,ypos)
            pdb.gimp_floating_sel_anchor(newselect)


            #place filename if asked for to extend with exif info
            if (inc_filename == True):
                if (inc_extension == True):
                    ThumbName = file['base_name'] + file['extension']
                else:
                    ThumbName = file['base_name']
                    
                Size,txtwidth = CalcFontSize(ThumbName,caption_font,FS,CalcTextHeight,MPx)                
                #calculate text position, round the center of the image
                txt_xpos = xpos + (MPx - txtwidth)/2 - x_offset
                txt_ypos = ypos + MPy + TM - y_offset
                txtfloat = pdb.gimp_text_fontname(sheetimg, sheetimg.active_layer,
				  txt_xpos, txt_ypos, ThumbName,-1,
                                  False, Size, PIXELS, caption_font) #place at x,y position
                pdb.gimp_floating_sel_anchor(txtfloat) #merge with background

            if exif_dateandtime == True:
                ThumbName = str(dateandtime)
                #Log('thumbname: ' + ThumbName)
                Size,txtwidth = CalcFontSize(ThumbName,caption_font,FS,CalcTextHeight,MPx)                
                #calculate text position, round the center of the image
                txt_xpos = xpos + (MPx - txtwidth)/2 - x_offset
                if (inc_filename == True):
                    txt_ypos = ypos + MPy + TM - y_offset + FS       #skip one line
                else:
                    txt_ypos = ypos + MPy + TM - y_offset
                    
                txtfloat = pdb.gimp_text_fontname(sheetimg, sheetimg.active_layer,
				  txt_xpos, txt_ypos, ThumbName,-1,
                                  False, Size, PIXELS, caption_font) #place at x,y position
                pdb.gimp_floating_sel_anchor(txtfloat) #merge with background


            ccount = ccount + 1
            if (ccount>= UseableCols):
                ccount = 0
                rcount = rcount + 1
            gimp.displays_flush()

        #save contactsheet
        contact_filename = filename + "_%03d" % (sheetcount+1) + contact_type
        contact_full_filename = os.path.join(save_to_location, contact_filename)

        if (contact_type == ".jpg"):
            save_jpeg(sheetimg,contact_full_filename,"")
        else:
            save_png(sheetimg,pdb.gimp_image_get_active_drawable(sheetimg),
                     contact_full_filename,False)

        if (Print_Contactsheet == True):
            pdb.file_print_gtk(sheetimg)

        gimp.delete(sheetimg)
        pdb.gimp_display_delete(sheetdsp)
