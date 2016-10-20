#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Files Resize
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.2
# - use gimp if file can't be handle by PyImaging
# Version 2.1
# - ported to GIMP-2.6
# - menu entry moved to Batch works
# Version 2.0
# - conserve layers for files in XCF format
# - can use GIMP if PyImaging is not there
# - ported to GIMP-2.4
# - use unicode
# - use gettext 
# Version 1.0
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the template-xtns.py file must be executable.
# The python-fu code is embedded by Gimp since 1.3 series.
# If python-fu is not activ then you probably need to recompile Gimp with
# "./configure --enable-python" option or find a binary/RPM gimp-python.

from gimpfu import *
import os, glob, shutil

# Optionnal module needed : PyImaging
# http://www.pythonware.com/products/pil/
#
try:
  import Image
  usegimp = False # If PyImaging is not there then use GIMP
except:
  usegimp = True
#usegimp = True # Force to use GIMP aniway here

# Constants
#
dirscaled = "scaled"

# i18n
#
import gettext
locale_directory = gimp.locale_directory 
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_fileresize_help = _("A batch process on images in a directory. Resize files by indicating the number of pixels of the larger side.")
Photolab_fileresize_description = Photolab_fileresize_help

# Main Program
#

def newsizecalculation( imagewidth, imageheight, thmaxsize ):
  if (imagewidth >= imageheight):
    ratiowidth = float( thmaxsize ) / imagewidth
    newimagewidth = thmaxsize
    newimageheight = ratiowidth * imageheight
  else:
    ratioheight = float( thmaxsize ) / imageheight
    newimageheight = thmaxsize
    newimagewidth = ratioheight * imagewidth
  newsizes = []
  newsizes.append( int(newimagewidth) )
  newsizes.append( int(newimageheight) )
  return list( newsizes )

def GIMPthumbnailer( filepathname, thfilepathname, thmaxsize ):
  try:
    GIMPimage= pdb.gimp_file_load( filepathname , filepathname )
  except:
    pdb.gimp_message( _("%s can't be treated by GIMP") %(filepathname) )
  else:  
    try:
      GIMPimage = pdb.gimp_xcf_load( 0, filepathname, filepathname ) # test if the image can be treated as xcf
      fileisxcf = True
    except:
      GIMPlayer= pdb.gimp_image_flatten( GIMPimage ) # flatten image in case there is more than one layer 
      fileisxcf = False
    imagewidth = GIMPimage.width
    imageheight = GIMPimage.height
    if ((imagewidth > thmaxsize) or (imageheight > thmaxsize)):
      newsizes = newsizecalculation( imagewidth, imageheight, thmaxsize )
      #DEBUG print( "newsizes=",newsizes[0], newsizes[1]) 
      GIMPimage.scale( newsizes[0], newsizes[1] )
      GIMPlayer= pdb.gimp_image_get_active_layer( GIMPimage )
    if fileisxcf:
      pdb.gimp_xcf_save( 0, GIMPimage, GIMPlayer, thfilepathname, thfilepathname )
    else:
      pdb.gimp_file_save( GIMPimage, GIMPlayer, thfilepathname, thfilepathname )

def thumbnailer( imageorig, thfilepathname, thmaxsize ):
  # Size calculation
  imagewidth = imageorig.size[0]
  imageheight = imageorig.size[1]
  if ((imagewidth > thmaxsize) or (imageheight > thmaxsize)):
    newsizes = newsizecalculation( imagewidth, imageheight, thmaxsize )
    #DEBUG print( "newsizes=",newsizes[0], newsizes[1]) 
    imageth = imageorig.resize( (newsizes[0], newsizes[1]), Image.ANTIALIAS )
    imageth.save( thfilepathname )
  else:  
    imageorig.save( thfilepathname )  

def python_fu_fileresize_xtns( 
  dirname, 
  ext,
  size ): #inImage, inDrawable, 
  
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      messagebox = pdb.gimp_message_get_handler( ) 
      pdb.gimp_message_set_handler( 2 ) # send messages in error console
      dirscaledpathname = os.path.join( u''+dirname, dirscaled )
      if os.path.exists( dirscaledpathname ):
        shutil.rmtree( dirscaledpathname )
      os.mkdir( dirscaledpathname )
      # Let start serious things  
      pdb.gimp_message( _("File processing is starting, please wait...") )
      for filepathname in filepathnames:
        try:
          file = open( u''+filepathname, 'rb' )
        except:
          if os.path.exists( filepathname ):
            pdb.gimp_message( "%s is a directory" %(filepathname) )
          else:
            pdb.gimp_message( "%s: Error" %(filepathname) )
          continue    
        # Files processing
        try:
          GIMPimage= pdb.gimp_xcf_load( 0, filepathname, filepathname)
          fileisxcf = True # Force to use GIMP if file is in XCF format
        except:
          fileisxcf = False
          try:
            imageorig = Image.open( u''+filepathname )
            fileimaging = True
          except:        
            fileimaging = False
        if usegimp or fileisxcf or not fileimaging: # with GIMP
          scfilepathname = os.path.join( dirscaledpathname, 'sc_' + os.path.basename(filepathname) )
          GIMPthumbnailer( filepathname, scfilepathname, size )
        else: # with PyImaging
          imageorig = Image.open( u''+filepathname )        
          scfilepathname = os.path.join( dirscaledpathname, 'sc_' + os.path.basename(filepathname) )
          thumbnailer( imageorig, scfilepathname, size )
      # End of process         
      pdb.gimp_message( _("End of the process") )        
      pdb.gimp_message_set_handler( messagebox )
    else:
      pdb.gimp_message( "%s is empty" %(dirname) )      
  else:
    pdb.gimp_message( "%s is not a directory" %(dirname) )

register(
  "FileResizeXtns",
  Photolab_fileresize_description,
  Photolab_fileresize_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Images Resize"),
  "",
  [
    (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("Extension"), "jpg" ),
    (PF_INT, "size", _("Size (px)"), "800" ),
  ],
  [],
  python_fu_fileresize_xtns,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
