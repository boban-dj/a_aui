#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Curve Batch
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 3.0
# - ported to new curve format used in GIMP-2.6
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
import os, glob, string, sys

# i18n
#
import gettext
locale_directory = gimp.locale_directory
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_curvebatch_help = _("A batch process on images in a directory to apply a curves file saved from the Curve tool of GIMP")
Photolab_curvebatch_description = Photolab_curvebatch_help

# Constants
#
dircurve = "~/.gimp-2.6/curves" #default searching pathname for curves
dircurve = os.path.expanduser( dircurve )
if not os.path.exists( u''+dircurve ):
  dircurve = os.path.expanduser( "~" ) #otherwise start from user directory

# Main Program
#

def readcurvefile(
  curvefilename
  ):
  curvefile = open( u''+curvefilename,'r' )
  lines = curvefile.readlines( )
  if lines[0] == "# GIMP curves tool settings\n":
    for line in lines:
      if line == "(channel value)\n": 
        nameCurve = "value"
      if line == "(channel red)\n": 
        nameCurve = "red"
      if line == "(channel green)\n": 
        nameCurve = "green"
      if line == "(channel blue)\n": 
        nameCurve = "blue"
      if line == "(channel alpha)\n": 
        nameCurve = "alpha"
      if line != "\n" :
        words = string.split( line )
        if words[0] == "(points":
          if nameCurve == "value":
            curve = words[2:]
          if nameCurve == "red":
            curvered = words[2:]
          if nameCurve == "green":
            curvegreen = words[2:]
          if nameCurve == "blue":
            curveblue = words[2:]
          if nameCurve == "alpha":
            curvealpha = words[2:]
    return curve, curvered, curvegreen, curveblue # Alpha is ignored
  else:
    pdb.gimp_message( _("This is not a GIMP Curves File") )
  curvefile.close()  


def extractpoints( curve ):
  icurve= [];
  for curvestr in curve:
    if curvestr[-1] == ")" :
      curvestr = curvestr[:-1]
    curvefloat = float( curvestr )
    curveint = (curvefloat * 255.0) #scale to [0,255]
    icurve.append( int( curveint ))
  ibmax = int( len(icurve) ) -1
  ib= 0
  ixcurve= []
  while ib <= ibmax:
    if icurve[ ib ] != -255:
    # Suppress all XY points beginning by -255
    # Not sure what I am doing here but you can not introduce directly the gimpcurve in gimp_curves_splines, doesn't work
    # Tested like that and seem's to work correctly
      ixcurve.append( icurve[ ib ] )
      ixcurve.append( icurve[ ib+1 ] )
    ib= ib +2
  return ixcurve

def process_files( 
  filepathnames,
  curvefilename ): 
  #DEBUG pdb.gimp_message( 'The selected directory has '+str( len( filenames ))+' files to handle' );
  # read the curve for the value
  curve, curvered, curvegreen, curveblue = readcurvefile( curvefilename ) # Alpha is ignored
  icurve= extractpoints( curve )
  icurvered= extractpoints( curvered )
  icurvegreen= extractpoints( curvegreen )
  icurveblue= extractpoints( curveblue )
  #
  for filepathname in filepathnames:
    img= pdb.gimp_file_load( filepathname , filepathname )
    imglayer= img.layers[0]
    # Process
    # Uncomment the line below to print the applied curve in format : 0,0,X1,Y1,X2,Y2,...,255,255
    # print "len:", len(icurve), "::courbe :", icurve
    if len(icurve) >= 4:
      pdb.gimp_curves_spline( imglayer, HISTOGRAM_VALUE, len(icurve), icurve )
    if len(icurvered) >= 4:
      pdb.gimp_curves_spline( imglayer, HISTOGRAM_RED, len(icurvered), icurvered )
    if len(icurvegreen) >= 4:
      pdb.gimp_curves_spline( imglayer, HISTOGRAM_GREEN, len(icurvegreen), icurvegreen )
    if len(icurveblue) >= 4:
      pdb.gimp_curves_spline( imglayer, HISTOGRAM_BLUE, len(icurveblue), icurveblue )
    #_("Batch")+"/"+
    newfilepathname = os.path.dirname(filepathname) + os.sep + 'CURVE_' + os.path.basename(filepathname)  
    pdb.gimp_file_save( img, imglayer, newfilepathname , newfilepathname )
    pdb.gimp_image_delete( img )

def python_fu_curvebatch_xtns( 
  dirname, 
  ext,
  curvefilename ):
  
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      messagebox = pdb.gimp_message_get_handler( ) 
      pdb.gimp_message_set_handler( 2 ) # send messages in error console
      #Start of process
      process_files( filepathnames, curvefilename );
      # End of process         
      pdb.gimp_message( _("End of the process") )        
      pdb.gimp_message_set_handler( messagebox )
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

# Register
#
register(
  "CurveBatch",
  Photolab_curvebatch_description,
  Photolab_curvebatch_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Curve"),
  "",
  [
    (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("Extension"), "jpg" ),
    (PF_FILENAME, "curvefilename", _("Curve file"), dircurve ),
  ],
  [],
  python_fu_curvebatch_xtns,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch corrections"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
