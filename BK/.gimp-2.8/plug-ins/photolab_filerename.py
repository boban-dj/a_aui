#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Files Rename
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.1
# - ported to GIMP-2.6
# - menu entry moved to Batch works
# Version 2.0
# - ported to GIMP-2.4
# - use system encodage detection
# - use unicode
# - use gettext 
# Version 1.0
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *
import os, locale, glob, math, string

# i18n
#
import gettext
locale_directory = gimp.locale_directory 
gettext.install( "gimp20-photolab" , locale_directory, unicode=True )

# System locale
try:
  encodage = locale.getpreferredencoding('CODESET')
except:
  encodage = locale.getpreferredencoding('') 
#encodage = myCODESET (force encodage here)

#
Photolab_filerename_help = _("A batch process on images in a directory. Rename the files in alphabetical order by adding a prefix followed by the number of order.")
Photolab_filerename_description = Photolab_filerename_help
  
# Main Program
#

def python_fu_filerename_xtns( 
  dirname, 
  ext,
  prefix ): #inImage, inDrawable, 
  
  if os.path.exists( u''+dirname ):
    #
    fileindir = os.listdir( u''+dirname )
    fileindir.sort()
    filenames = []
    if fileindir : 
      for filename in fileindir:
        nbext = string.count( filename, '.')
        fileext = string.split( filename, '.' )[nbext]
        if fileext == ext :
          filenames.append( filename )   
    #
    if filenames:
      recoverydir= os.getcwd() # Prepare to work !
      os.chdir( u''+dirname )
      messagebox = pdb.gimp_message_get_handler( ) 
      pdb.gimp_message_set_handler( 2 ) # send messages in error console
      #
      # Overwrite Prefix txt files when exists
      try:
        prefixfile = open( 'prefix.txt', 'r' )
        encodedprefix = string.split( prefixfile.readline( ))[0]
        prefix = encodedprefix.decode( encodage ) 
        prefixfile.close( ) 
        pdb.gimp_message( _("prefix.txt found use encodage: %s") %(encodage) )                
      except:  
        pdb.gimp_message( _("prefix.txt not found use prefix value: %s") %(prefix) ) 
      index = 1
      fileduplicate = []         
      for filename in filenames:
        if os.path.isfile( filename ):
           # Files processing
           nbdigits = int( math.ceil( math.log10( len( filenames ) +1)))
           textindex = string.replace( string.rjust( str ( index ), nbdigits ), ' ', '0' )
           newfilename = prefix + '_' + textindex + '.' + ext
           if os.path.isfile( u''+newfilename ):
             os.rename( u''+filename, u''+newfilename+'#2' )  
             fileduplicate.append( newfilename+'#2' )      
           else:
             os.rename( u''+filename, u''+newfilename )
        else:
          pdb.gimp_message( _("%s:error") %( filemane ))       
        # Loop parameters
        index = index +1
      if ( fileduplicate ):
        for filename in fileduplicate:
          newfilename = filename[ :-2 ]
          os.rename( u''+filename, u''+newfilename )         
      # End of process         
      pdb.gimp_message( _("End of the process") )        
      os.chdir( u''+recoverydir )
      pdb.gimp_message_set_handler( messagebox )
    else:
      pdb.gimp_message( _("%s don't have files to handle") %( dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "FileRenameXtns",
  Photolab_filerename_description,
  Photolab_filerename_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Rename files"),
  "",
  [
    (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("Extension"), 'jpg' ),
    (PF_STRING, "prefix", _("Prefix"), "prefix" ),
  ],
  [],
  python_fu_filerename_xtns,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=( "gimp20-photolab", locale_directory )      
  )

main()
