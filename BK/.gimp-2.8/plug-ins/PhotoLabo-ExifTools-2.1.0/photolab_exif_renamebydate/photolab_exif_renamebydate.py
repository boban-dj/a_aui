#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Exiftools-renamebydate python-fu pour Gimp 2
# Copyright Raymond Ostertag 2008-2009
# Licence GPL

# Version 1.2
# - change way (Windows compatible) to handle space for file names
# Version 1.1
# - now accept space for file names in command line
# Version 1.0
# - initial release

# Installation : put the py file in your $HOME/.gimp-2.n/plug-ins.
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
Photolab_exiftools_renamebydate_help = _("A batch process on photos with EXIF data in a directory. Rename photos by adding EXIF date as prefix.")                                
Photolab_exiftools_renamebydate_description = Photolab_exiftools_renamebydate_help

# main
#                                         
def process_files( 
  filepathnames ): 
  #DEBUG pdb.gimp_message( _("The selected directory has %s files to handle") %(str( len( filepathnames ))));
  for filepathname in filepathnames:
    os.system( "jhead -n%Y%m%d-%H%M%S-%f "+"\""+filepathname+"\"")

def python_fu_exiftools_renamebydate( 
  dirname, 
  ext ):
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      #Start of process
      process_files( filepathnames );
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-exiftools-renamebydate",
  Photolab_exiftools_renamebydate_description,
  Photolab_exiftools_renamebydate_help,
  "Raymond Ostertag",
  "GPL License",
  "2008-2009",
  _("Rename by date"),
  "",
  [
     (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
     (PF_STRING, "ext", _("File extension"), "jpg" ),
  ],
  [],
  python_fu_exiftools_renamebydate,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("EXIF tools"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
