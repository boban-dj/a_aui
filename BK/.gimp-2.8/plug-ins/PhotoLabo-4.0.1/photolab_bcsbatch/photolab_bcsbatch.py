#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Brightness Contrast Saturation Batch
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.1
# - ported to GIMP-2.6
# - menu entry moved to Batch corrections
# Version 2.0
# - ported to GIMP-2.4
# - use unicode
# - use gettext 
# - moved to glob function and file pathname
# Version 1.0
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *
import os, glob

# i18n
#
import gettext
locale_directory = gimp.locale_directory
gettext.install( "gimp20-photolab" , locale_directory, unicode=True )

#
Photolab_bcsbatch_help = _("A batch process on images in a directory to apply brightness contrast and saturation of GIMP.")
Photolab_bcsbatch_description = Photolab_bcsbatch_help
  
# Main Program
#
def process_files( 
  filepathnames,
  brightness,
  contrast,
  saturation ): 
  for filepathname in filepathnames:
    img= pdb.gimp_file_load( filepathname , filepathname )
    imglayer= img.layers[0]
    # Process
    pdb.gimp_brightness_contrast( imglayer, brightness, contrast )
    hue_range= 0
    hue_offset= 0 # Neutral value
    lightness= 0 # Neutral value
    pdb.gimp_hue_saturation( imglayer, hue_range, hue_offset, lightness, saturation )
    #
    newfilepathname = os.path.dirname(filepathname) + os.sep + 'BCS_' + os.path.basename(filepathname)  
    pdb.gimp_file_save( img, imglayer, newfilepathname , newfilepathname )
    pdb.gimp_image_delete( img )

def python_fu_bcsbatch_xtns( 
  dirname, 
  ext,
  brightness,
  contrast,
  saturation ): #inImage, inDrawable, 
  
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      messagebox = pdb.gimp_message_get_handler( ) 
      pdb.gimp_message_set_handler( 2 ) # send messages in error console
      #Start of process
      process_files( filepathnames, brightness, contrast, saturation );
      # End of process         
      pdb.gimp_message( _("End of the process") )        
      pdb.gimp_message_set_handler( messagebox )
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ) )      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

# Register
#
register(
   "BCSBatch",
   Photolab_bcsbatch_description,
   Photolab_bcsbatch_help,
   "Raymond Ostertag",
   "GPL License",
   "2007-2009",
   _("Brightness contrast saturation"),
   "",
   [
      (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
      (PF_STRING, "ext", _("Extension"), 'jpg' ),
      (PF_SLIDER, "brightness", _("Brightness"), 0, (-127,127,1) ),
      (PF_SLIDER, "contrast", _("Contrast"), 0, (-127,127,1) ),
      (PF_SLIDER, "saturation", _("Saturation"), 0, (-100,100,1) ),
   ],
   [],
   python_fu_bcsbatch_xtns,
   menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch corrections"),
   domain=( "gimp20-photolab", locale_directory )         
   )

main()
