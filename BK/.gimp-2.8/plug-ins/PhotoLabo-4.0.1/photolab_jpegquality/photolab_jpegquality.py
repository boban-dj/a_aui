#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Jpeg Quality
# Copyright Raymond Ostertag 2009
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the photolab_template.py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *
import os, glob, shutil

# Constants
#
minQuality = 50 
maxQuality = 98 
smoothing = 0.0 
optimize = 1
comment = ""
subsmp = 0
baseline = 0
restart= 0
dct = 0

# i18n
#
import gettext
locale_directory = gimp.locale_directory
gettext.install( "gimp20-photolab" , locale_directory, unicode=True )

#
Photolab_jpegq_help = _("A batch process on images in a directory.")+_("Set quality of JPEG. Useful to decrease the weight of JPEG before sending them to the Web.")
Photolab_jpegq_description = Photolab_jpegq_help 

# export name
#         
def python_fu_photolab_jpegq_exportname( 
  inImage,  
  toDirectory, 
  quality
  ):
  imageName = pdb.gimp_image_get_name( inImage )
  imageBasename = os.path.splitext( imageName )[0]
  imageExtname = os.path.splitext( imageName )[1]
  if imageExtname == "" or imageExtname == ".xcf" :
    imageExtname = ".jpg"
  newfilepathname = toDirectory + os.sep + imageBasename + '_JPEGQ' + str(int(quality)) + imageExtname 
  return newfilepathname  

# Main Program
#
def python_fu_photolab_jpegq( 
  dirname, 
  ext,
  copy,
  toDirectory,
  quality,
  progressive ):
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      #Start of process
      #DEBUG pdb.gimp_message( _("The selected directory has %s files to handle") %(str( len( filepathnames ))));
      for filepathname in filepathnames:
        img= pdb.gimp_file_load( filepathname , filepathname )
        imglayer= img.layers[0]
        #
        if copy :
          jpegqfilepathname = python_fu_photolab_jpegq_exportname( img, toDirectory, quality )
        else:
          jpegqfilepathname = filepathname
        pdb.file_jpeg_save( img, imglayer, jpegqfilepathname, jpegqfilepathname, float(quality)/100.0, float(smoothing), optimize, int(progressive), comment, subsmp, baseline, restart, dct)
        gimp.delete( img )
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-photolab-jpegq",
  Photolab_jpegq_description,
  Photolab_jpegq_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Jpeg quality"),
  "",
  [
    (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("File extension"), "jpg" ),
    (PF_TOGGLE, "copy", _("Create a copy"), True), #bool
    (PF_DIRNAME, "toDirectory", ".."+_("Destination directory"), os.getcwd() ),  
    (PF_SPINNER, "quality", _("Quality"), 85, (minQuality,maxQuality,1)), #int
    (PF_TOGGLE, "progressive", _("Progressive image loading (Web)"), True), #bool
  ],
  [],
  python_fu_photolab_jpegq,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
