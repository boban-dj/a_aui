#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Exiftools-synchronize-2camera python-fu pour Gimp 2
# Copyright Raymond Ostertag 2008-2009
# Licence GPL

# Version 1.2
# - change way (Windows compatible) to handle space for file names
# - add missing code lines for case of directory3 = directory2
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
Photolab_exiftools_synchronize_2camera_help = _("Manually synchronize EXIF date from photos taken by two cameras. The source photos are in separate directory, one for each camera. The result is renammed by EXIF date and can be merged into a new directory.")                                
Photolab_exiftools_synchronize_2camera_description = Photolab_exiftools_synchronize_2camera_help

# main
#                                         
def process_files( 
  filepathnames1,
  sign,
  days, hours, minutes, seconds,
  filepathnames2,
  dirname1, dirname2, dirname3 ): 
  #DEBUG pdb.gimp_message( _("The selected directory has %s files to handle") %(str( len( filepathnames1 ))));
  hours = hours + 24*days;
  for filepathname in filepathnames1:
    os.system( "jhead -ta"+sign+str(int(hours))+":"+str(int(minutes))+":"+str(int(seconds))+" "+"\""+filepathname+"\"")
  # if directory3 = directory1
  # copy files from directory2 to directory3
  newfilepathnames = []
  if ( dirname3 == dirname1 ):
    for filepathname in filepathnames1:
      newfilepathnames.append( filepathname )
    for filepathname in filepathnames2:
      os.system( "cp "+"\""+filepathname+"\""+" "+"\""+dirname3+"\"")
      newfilepathnames.append( os.path.join( dirname3, os.path.basename( filepathname )))      
  # if directory3 = directory2
  # copy files from directory to directory3
  elif ( dirname3 == dirname2 ):
    for filepathname in filepathnames1:
      os.system( "cp "+"\""+filepathname+"\""+" "+"\""+dirname3+"\"")
      newfilepathnames.append( os.path.join( dirname3, os.path.basename( filepathname )))      
    for filepathname in filepathnames2:
      newfilepathnames.append( filepathname )
  # copy files from directory and directory2 to directory3
  else:
    for filepathname in filepathnames1:
      os.system( "cp "+"\""+filepathname+"\""+" "+"\""+dirname3+"\"")
      newfilepathnames.append( os.path.join( dirname3, os.path.basename( filepathname )))      
    for filepathname in filepathnames2:
      os.system( "cp "+"\""+filepathname+"\""+" "+"\""+dirname3+"\"")   
      newfilepathnames.append( os.path.join( dirname3, os.path.basename( filepathname )))      
  # rename by date in directory3
  for filepathname in newfilepathnames:
    os.system( "jhead -n%Y%m%d-%H%M%S-%f "+"\""+filepathname+"\"")
  
def python_fu_exiftools_synchronize_2camera( 
  dirname1, 
  ext1,
  sign,
  days, hours, minutes, seconds,
  dirname2, ext2,
  dirname3 ):
  if (dirname1 == dirname2) :
    pdb.gimp_message( _("Sorry but first and second directory can't be the same"))
  else:  
    if os.path.exists( u''+dirname1 ):
      #
      globpattern = u''+dirname1 + os.sep + '*.' + ext1
      filepathnames1 = glob.glob( globpattern ) # return complete path name of files
    else:
      pdb.gimp_message( _("%s don't exist") %(dirname1) )
    if os.path.exists( u''+dirname2 ):
      #
      globpattern = u''+dirname2 + os.sep + '*.' + ext2
      filepathnames2 = glob.glob( globpattern ) # return complete path name of files
    else:
      pdb.gimp_message( _("%s don't exist") %(dirname2) )
    if filepathnames1 and filepathnames2 :
      #Start of process
      process_files( filepathnames1, sign, days, hours, minutes, seconds, filepathnames2, dirname1, dirname2, dirname3 );
      #End of process         
    else:
      pdb.gimp_message( _("%s or %s don't have files to handle") %(dirname1,dirname2))  

register(
  "python-fu-exiftools-synchronize-2camera",
  Photolab_exiftools_synchronize_2camera_description,
  Photolab_exiftools_synchronize_2camera_help,
  "Raymond Ostertag",
  "GPL License",
  "2008-2009",
  _("Synchronize 2 cameras"),
  "",
  [
     (PF_DIRNAME, "directory1", _("First camera source directory"), os.getcwd() ),
     (PF_STRING, "ext1", _("File extension"), "jpg" ),
     (PF_RADIO, "sign", _("Sign"), "+", (("+","+"), ("-","-"))), #str
     (PF_INT8, "days", _("Days"), 0 ),
     (PF_SPINNER, "hours", _("Hours"), 0, (0,24,1)), #int
     (PF_SPINNER, "minutes", _("Minutes"), 0, (0,60,1)), #int
     (PF_SPINNER, "seconds", _("Seconds"), 0, (0,60,1)), #int
     (PF_DIRNAME, "directory2", _("Second camera source directory"), os.getcwd() ),
     (PF_STRING, "ext2", _("File extension"), "jpg" ),
     (PF_DIRNAME, "directory3", _("Merging destination directory"), os.getcwd() ),
  ],
  [],
  python_fu_exiftools_synchronize_2camera,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("EXIF tools"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
