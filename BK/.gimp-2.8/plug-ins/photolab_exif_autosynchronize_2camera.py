#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Exiftools-autosynchronize-2camera python-fu pour Gimp 2
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
import os, glob, datetime

# i18n
#
import gettext
locale_directory = gimp.locale_directory
gettext.install( "gimp20-photolab" , locale_directory, unicode=True )

# jhead parameters
#
dateTag = "Date/Time"

#
Photolab_exiftools_autosynchronize_2camera_help = _("Auto synchronize EXIF date from photos taken by two cameras. To synchronize automatically the EXIF dates, you need two reference photos taken at the same time by the 2 cameras. The source photos and therefore the reference photos are in separate directory, one for each camera. The result is renammed by EXIF date and can be merged into a new directory.")                                
Photolab_exiftools_autosynchronize_2camera_description = Photolab_exiftools_autosynchronize_2camera_help

# main
#                                         
def process_files( 
  filepathnames1, filepathnames2,
  photoref1, photoref2,
  dirname1, dirname2, dirname3 ):
  #
  os.system( "jhead "+"\""+photoref1+"\""+">"+"\""+photoref1+".txt"+"\"" )
  ref1hasdate = False
  for textline in open( photoref1+".txt", 'r' ):
    #DEBUG print textline[0:9]
    if( textline[0:9]==dateTag ):
      ref1tag, ref1year, ref1month, ref1dayhour, ref1minute, ref1second = textline.split( ":" )
      ref1day= ref1dayhour[0:2]
      ref1hour = ref1dayhour[3:5]
      #DEBUG print( ref1year + ref1month + ref1day + ref1hour + ref1minute + ref1second )
      ref1date = datetime.datetime( int(ref1year), int(ref1month), int(ref1day), int(ref1hour), int(ref1minute), int(ref1second), tzinfo=None)
      ref1hasdate = True
      break
  os.system( "rm "+"\""+photoref1+".txt"+"\"" )
  if( not ref1hasdate ):
    pdb.gimp_message( _("Can't find date in Exif data of %s") %(photoref1))
  else:
    os.system( "jhead "+"\""+photoref2+"\""+">"+"\""+photoref2+".txt"+"\"" )
    ref2hasdate = False
    for textline in open( photoref2+".txt", 'r' ):
      #DEBUG print textline[0:9]
      if( textline[0:9]==dateTag ):
        ref2tag, ref2year, ref2month, ref2dayhour, ref2minute, ref2second = textline.split( ":" )
        ref2day= ref2dayhour[0:2]
        ref2hour = ref2dayhour[3:5]
        #DEBUG print( ref2year + ref2month + ref2day + ref2hour + ref2minute + ref2second )
        ref2date = datetime.datetime( int(ref2year), int(ref2month), int(ref2day), int(ref2hour), int(ref2minute), int(ref2second), tzinfo=None)
        ref2hasdate = True
        break
    os.system( "rm "+"\""+photoref2+".txt"+"\"" )
    if( not ref2hasdate ):
      pdb.gimp_message( _("Can't find date in Exif data of %s") %(photoref2))
    else:
      #
      deltatime = ref1date-ref2date
      if( ref1date >= ref2date ):
        sign = "+"
      else:
        sign = "-"
      #DEBUG print sign, deltatime
      #
      newfilepathnames = []
      # if directory3 = directory1
      if ( dirname3 == dirname1 ):
        for filepathname1 in filepathnames1:
          newfilepathnames.append( filepathname1 )
        for filepathname2 in filepathnames2:
          os.system( "cp "+"\""+filepathname2+"\""+" "+"\""+dirname3+"\"") #Copy files from dirname2 to dirname3   
          newfilepathname2 = os.path.join( dirname3, os.path.basename( filepathname2 ))
          os.system( "jhead -ta"+sign+"0:0:"+str(int(deltatime.seconds))+" "+"\""+newfilepathname2+"\"") #Change exif date of files copied from dirname2
          newfilepathnames.append( newfilepathname2 )      
      # if directory3 = directory2
      elif ( dirname3 == dirname2 ):
        for filepathname1 in filepathnames1:
          os.system( "cp "+"\""+filepathname1+"\""+" "+"\""+dirname3+"\"") #Copy files from dirname1 to dirname3
          newfilepathname1 = os.path.join( dirname3, os.path.basename( filepathname1 ))
          newfilepathnames.append( newfilepathname1 )      
        for filepathname2 in filepathnames2:
          os.system( "jhead -ta"+sign+"0:0:"+str(int(deltatime.seconds))+" "+"\""+filepathname2+"\"") #Change exif date of files original from dirname2
          newfilepathnames.append( filepathname2 )      
      else:
        for filepathname1 in filepathnames1:
          os.system( "cp "+"\""+filepathname1+"\""+" "+"\""+dirname3+"\"") #Copy files from dirname1 to dirname3
          newfilepathname1 = os.path.join( dirname3, os.path.basename( filepathname1 ))
          newfilepathnames.append( newfilepathname1 )      
        for filepathname2 in filepathnames2:
          os.system( "cp "+"\""+filepathname2+"\""+" "+"\""+dirname3+"\"") #Copy files from dirname2 to dirname3   
          newfilepathname2 = os.path.join( dirname3, os.path.basename( filepathname2 ))
          os.system( "jhead -ta"+sign+"0:0:"+str(int(deltatime.seconds))+" "+"\""+newfilepathname2+"\"") #Change exif date of files copied from dirname2
          newfilepathnames.append( newfilepathname2 )      
      # rename by date in directory3
      for filepathname in newfilepathnames:
        os.system( "jhead -n%Y%m%d-%H%M%S-%f "+"\""+filepathname+"\"") #Change name of all files copied

def python_fu_exiftools_autosynchronize_2camera( 
  photoref1, 
  toggle1, dirname1, ext1,
  photoref2,
  toggle2, dirname2, ext2,
  dirname3 ):
  if not toggle1 :
    dirname1 = os.path.dirname( photoref1 )
    ext1 = os.path.splitext( os.path.basename( photoref1 ))[1] 
  if not toggle2 :
    dirname2 = os.path.dirname( photoref2 )
    ext2 = os.path.splitext( os.path.basename( photoref2 ))[1]   
  if( photoref1 and photoref2 ):
    if(dirname1 == dirname2 ):
      pdb.gimp_message( _("Sorry but first and second directory can't be the same"))
    else:  
      if os.path.exists( u''+dirname1 ):
        #
        globpattern = u''+dirname1 + os.sep + '*' + str(ext1)
        filepathnames1 = glob.glob( globpattern ) # return complete path name of files
      else:
        pdb.gimp_message( _("%s don't exist") %(dirname1) )
      if os.path.exists( u''+dirname2 ):
        #
        globpattern = u''+dirname2 + os.sep + '*' + str(ext2)
        filepathnames2 = glob.glob( globpattern ) # return complete path name of files
      else:
        pdb.gimp_message( _("%s don't exist") %(dirname2) )  
      if filepathnames1 and filepathnames2 :
        #Start of process
        process_files( filepathnames1, filepathnames2, photoref1, photoref2, dirname1, dirname2, dirname3 );
        #End of process         
      else:
        pdb.gimp_message( _("%s or %s don't have files to handle") %(dirname1,dirname2))  
  else:
      pdb.gimp_message( _("You need two reference photos, please modify %s or %s") %(photoref1,photoref2))  


register(
  "python-fu-exiftools-autosynchronize-2camera",
  Photolab_exiftools_autosynchronize_2camera_description,
  Photolab_exiftools_autosynchronize_2camera_help,
  "Raymond Ostertag",
  "GPL License",
  "2008-2009",
  _("Synchronize automatically 2 cameras"),
  "",
  [
     (PF_FILENAME, "photoref1", _("First reference photo"), None ),
     (PF_TOGGLE, "toggle1", _("Use different first source directory or file extension"), False), #bool
     (PF_DIRNAME, "directory1", "..."+_("First camera source directory"), None ),
     (PF_STRING, "ext1","..."+ _("File extension"), "jpg" ),
     (PF_FILENAME, "photoref2", _("Second reference photo"), None ),
     (PF_TOGGLE, "toggle2", _("Use different second source directory or file extension"), False), #bool
     (PF_DIRNAME, "directory2","..."+ _("Second camera source directory"), os.getcwd() ),
     (PF_STRING, "ext2","..."+ _("File extension"), "jpg" ),
     (PF_DIRNAME, "directory3", _("Merging destination directory"), os.getcwd() ),
  ],
  [],
  python_fu_exiftools_autosynchronize_2camera,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("EXIF tools"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
