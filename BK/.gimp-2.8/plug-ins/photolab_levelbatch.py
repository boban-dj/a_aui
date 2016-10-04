#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Level Batch
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 3.0
# - ported to new level format used in GIMP-2.6
# Version 2.1
# - ported to GIMP-2.6
# - menu entry moved to Batch corrections
# Version 2.0.1
# - applied patch from Torbjörn Wassberg
# - fix a memory leak 
# - make it work with greyscale images
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
import os, glob, string

# Constants
#
dirlevel = "~/.gimp-2.6/levels" #default searching pathname for curves
dirlevel = os.path.expanduser( dirlevel )
if not os.path.exists( u''+dirlevel ):
  dirlevel = os.path.expanduser( "~" ) #otherwise start from user directory

# i18n
#
import gettext
locale_directory = gimp.locale_directory 
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_levelbatch_help = _("A batch process on images in a directory to apply a levels file saved from the Level tool of GIMP.")
Photolab_levelbatch_description = Photolab_levelbatch_help

# Main Program
#
def readcurvefile(
  curvefilename
  ):
  curvefile = open( u''+curvefilename,'r' )
  lines = curvefile.readlines( )
  curve = []
  curvered = []
  curvegreen = []
  curveblue = []
  if lines[0] == "# GIMP levels tool settings\n":
    for line in lines:
      if line == "(channel value)\n": 
        nameLevel = "value"
      elif line == "(channel red)\n": 
        nameLevel = "red"
      elif line == "(channel green)\n": 
        nameLevel = "green"
      elif line == "(channel blue)\n": 
        nameLevel = "blue"
      elif line == "(channel alpha)\n": 
        nameLevel = "alpha"
      if line != "\n" :
        words = string.split( line )
        index = 0
        if words[0] == "(gamma":
          curveFloat = float( words[1][:-1] )
        elif words[0] == "(low-input":
          index = 1
          curveFloat = float( words[1][:-1] ) * 255.0 #scale to [0,255]
        elif words[0] == "(high-input":
          index = 2
          curveFloat = float( words[1][:-1] ) * 255.0 #scale to [0,255]
        elif words[0] == "(low-output":
          index = 3
          curveFloat = float( words[1][:-1] ) * 255.0 #scale to [0,255]
        elif words[0] == "(high-output":
          index = 4
          curveFloat = float( words[1][:-1] ) * 255.0 #scale to [0,255]
        else:
          index = 5
        if index != 5:
          if nameLevel == "value":
            curve.append( curveFloat )
          elif nameLevel == "red":        
            curvered.append( curveFloat )      
          elif nameLevel == "green":
            curvegreen.append( curveFloat )   
          elif nameLevel == "blue":
            curveblue.append( curveFloat )             
          elif nameLevel == "alpha":
            pass
    return curve, curvered, curvegreen, curveblue # Alpha is ignored
  else:
    pdb.gimp_message( _("This is not a GIMP Level File") );
  curvefile.close()

def process_files( 
  filepathnames,
  levelfilename ): 
  #DEBUG pdb.gimp_message( 'The selected directory has '+str( len( filenames ))+' files to handle' );
  # read the curve for the value
  curve, curvered, curvegreen, curveblue = readcurvefile( levelfilename ) # Alpha is ignored
  #
  for filepathname in filepathnames:
    img= pdb.gimp_file_load( filepathname , filepathname )
    imglayer= img.layers[0]
    # Process
    if len(curve) == 5:
      pdb.gimp_levels( imglayer, HISTOGRAM_VALUE, curve[1], curve[2], curve[0], curve[3], curve[4] )
    if not imglayer.is_grey:
      if len(curvered) == 5:
        pdb.gimp_levels( imglayer, HISTOGRAM_RED, curvered[1], curvered[2], curvered[0], curvered[3], curvered[4] )
      if len(curvegreen) == 5:
        pdb.gimp_levels( imglayer, HISTOGRAM_GREEN, curvegreen[1], curvegreen[2], curvegreen[0], curvegreen[3], curvegreen[4] )
      if len(curveblue) == 5:
        pdb.gimp_levels( imglayer, HISTOGRAM_BLUE, curveblue[1], curveblue[2], curveblue[0], curveblue[3], curveblue[4] )
    #
    newfilepathname = os.path.dirname(filepathname) + os.sep + 'LEVEL_' + os.path.basename(filepathname)  
    pdb.gimp_file_save( img, imglayer, newfilepathname , newfilepathname )
    pdb.gimp_image_delete( img )    

def python_fu_levelbatch_xtns( 
  dirname, 
  ext,
  levelfilename ):
  
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      messagebox = pdb.gimp_message_get_handler( ) 
      pdb.gimp_message_set_handler( 2 ) # send messages in error console
      #Start of process
      process_files( filepathnames, levelfilename );
      # End of process         
      pdb.gimp_message( _("End of the process") )        
      pdb.gimp_message_set_handler( messagebox )
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ) )      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )
      

register(
  "LevelBatch",
  Photolab_levelbatch_description,
  Photolab_levelbatch_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Level"),
  "",
  [
    (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("Extension"), "jpg" ),
    (PF_FILE, "levelfilename", _("Gimp Levels file") , dirlevel ),
  ],
  [],
  python_fu_levelbatch_xtns,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch corrections"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
