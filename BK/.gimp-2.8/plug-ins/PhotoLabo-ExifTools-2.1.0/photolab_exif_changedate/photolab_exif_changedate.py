#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Exiftools-changedate python-fu pour Gimp 2
# Copyright Raymond Ostertag 2009
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
Photolab_exiftools_changedate_help = _("A batch process on photos with EXIF data in a directory. Change EXIF date by adding or substracting a delay.")                                
Photolab_exiftools_changedate_description = Photolab_exiftools_changedate_help

# main
#                                         
def process_files( 
  filepathnames,
  sign,
  days, hours, minutes, seconds ): 
  #DEBUG pdb.gimp_message( _("The selected directory has %s files to handle") %(str( len( filepathnames ))));
  hours = hours + 24*days;
  for filepathname in filepathnames:
    os.system( "jhead -ta"+sign+str(int(hours))+":"+str(int(minutes))+":"+str(int(seconds))+" "+"\""+filepathname+"\"")

def python_fu_exiftools_changedate( 
  dirname, 
  ext,
  sign,
  days, hours, minutes, seconds ):
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      #Start of process
      process_files( filepathnames, sign, days, hours, minutes, seconds );
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-exiftools-changedate",
  Photolab_exiftools_changedate_description,
  Photolab_exiftools_changedate_help,
  "Raymond Ostertag",
  "GPL License",
  "2008-2009",
  _("Change date"),
  "",
  [
     (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
     (PF_STRING, "ext", _("File extension"), "jpg" ),
     (PF_RADIO, "sign", _("Sign"), "+", (("+","+"), ("-","-"))), #str
     (PF_INT8, "days", _("Days"), 0 ),
     (PF_SPINNER, "hours", _("Hours"), 0, (0,24,1)), #int
     (PF_SPINNER, "minutes", _("Minutes"), 0, (0,60,1)), #int
     (PF_SPINNER, "seconds", _("Seconds"), 0, (0,60,1)), #int
  ],
  [],
  python_fu_exiftools_changedate,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("EXIF tools"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
