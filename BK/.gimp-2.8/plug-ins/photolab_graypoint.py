#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Photolab_graypoint python-fu pour Gimp 2.6
# Copyright Raymond Ostertag 2009
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the photolab_graypoint.py file in your $HOME/.gimp-2.n/plug-ins.
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
Photolab_graypoint_help = _("Set a gray point in the image by adjusting the color channels. Pick the adjusting color in the image. This color will be turned into the reference gray color.")                                
Photolab_graypoint_description = Photolab_graypoint_help
#
Photolab_graypoint_batch_help = _("A batch process on images in a directory.")+" "+Photolab_graypoint_help         
Photolab_graypoint_batch_description = Photolab_graypoint_batch_help

# dialog parameters
#
Standalone_parameters = [
  (PF_IMAGE, "inImage", "Input image", None),
  (PF_DRAWABLE, "inLayer", "Input drawable", None),
]
BatchMode_parameters = [
  (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
  (PF_STRING, "ext", _("File extension"), "jpg" ),
  (PF_DIRNAME, "toDirectory", _("Destination directory"), os.getcwd() ),  
]
Photolab_graypoint_parameters = [
  (PF_COLOR, "adjustColor", _("Adjusting color"), (128,128,128) ), #gimpcolor.RGB
  (PF_COLOR, "grayColor", _("Reference gray"), (128,128,128) ), #gimpcolor.RGB
  (PF_RADIO, "preserveWB", _("Preserve White and Black"), "curve", ((_("No (Channel mixer)"),"mixer"), (_("Yes (Curves)"),"curve"))), #str
]  

# main
#             
def python_fu_photolab_graypoint_exportname( 
  inImage,  
  toDirectory, 
  adjustColor,
  ):
  imageName = pdb.gimp_image_get_name( inImage )
  imageBasename = os.path.splitext( imageName )[0]
  imageExtname = os.path.splitext( imageName )[1]
  if imageExtname == "" or imageExtname == ".xcf" :
    imageExtname = ".jpg"
  idGraypoint = 'R' + str(adjustColor[0]) + 'V' + str(adjustColor[1]) + 'B' + str(adjustColor[2])
  newfilepathname = toDirectory + os.sep + imageBasename + '_GRAYPOINT_' + idGraypoint + imageExtname 
  return newfilepathname
                            
def python_fu_photolab_graypoint( 
  inImage,
  inDrawable,
  adjustColor,
  grayColor,
  preserveWB,
  ): 
  gimp.context_push()
  pdb.gimp_image_undo_group_start( inImage )
  #preserve luminosity
  adjustColorLum = ( adjustColor[0] + adjustColor[1] + adjustColor[2] ) /  3.0
  grayColorLum = ( grayColor[0] + grayColor[1] + grayColor[2] ) /  3.0
  factorLum = adjustColorLum / grayColorLum
  #DEBUG print adjustColorLum, grayColorLum, factorLum
  #calculate destination gray
  destinationColor = ( int( grayColor[0] * factorLum), int( grayColor[1] * factorLum), int( grayColor[2] * factorLum))
  #DEBUG print destinationColor
  #calculate gain
  rr_gain = float(destinationColor[0]) / float(adjustColor[0])
  gg_gain = float(destinationColor[0]) / float(adjustColor[1])
  bb_gain = float(destinationColor[0]) / float(adjustColor[2]) 
  #DEBUG print rr_gain, gg_gain, bb_gain
  # linear (channel mixer)
  if preserveWB == "mixer":
    monochrome = 0 #FALSE
    rg_gain = 0.0
    rb_gain = 0.0
    gr_gain = 0.0
    gb_gain = 0.0
    br_gain = 0.0
    bg_gain = 0.0  
    pdb.plug_in_colors_channel_mixer( inImage, inDrawable, monochrome, rr_gain, rg_gain, rb_gain, gr_gain, gg_gain, gb_gain, br_gain, bg_gain, bb_gain )
  #
  # non linear (curves)
  else:
    medianX = adjustColor[0] #red of adjustcolor
    redCurve = []
    redCurve.append( 0 )
    redCurve.append( 0 )
    redCurve.append( medianX )
    redCurve.append( int( medianX * rr_gain ))
    redCurve.append( 255 )
    redCurve.append( 255 )
    pdb.gimp_curves_spline( inDrawable, HISTOGRAM_RED, len(redCurve), redCurve )
    medianX = adjustColor[1] #green of adjustcolor
    greenCurve = []
    greenCurve.append( 0 )
    greenCurve.append( 0 )
    greenCurve.append( medianX )
    greenCurve.append( int( medianX * gg_gain ))
    greenCurve.append( 255 )
    greenCurve.append( 255 )
    pdb.gimp_curves_spline( inDrawable, HISTOGRAM_GREEN, len(greenCurve), greenCurve )
    medianX = adjustColor[2] #blue of adjustcolor
    blueCurve = []
    blueCurve.append( 0 )
    blueCurve.append( 0 )
    blueCurve.append( medianX )
    blueCurve.append( int( medianX * bb_gain ))
    blueCurve.append( 255 )
    blueCurve.append( 255 )
    #DEBUG print redCurve, greenCurve, blueCurve
    pdb.gimp_curves_spline( inDrawable, HISTOGRAM_BLUE, len(blueCurve), blueCurve )
  #
  pdb.gimp_image_undo_group_end( inImage )
  gimp.context_pop()  

register(
  "python-fu-photolab-graypoint",
  Photolab_graypoint_description,
  Photolab_graypoint_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Graypoint"),
  "*",
  Standalone_parameters + Photolab_graypoint_parameters,
  [],
  python_fu_photolab_graypoint,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=("gimp20-photolab", locale_directory)   
  )

# batch of main
#

def python_fu_photolab_graypoint_batch( 
  dirname, 
  ext,
  toDirectory,
  adjustColor,
  grayColor,
  preserveWB,
  ):
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
        python_fu_photolab_graypoint( img, imglayer, adjustColor, grayColor, preserveWB );
        #
        newfilepathname = python_fu_photolab_graypoint_exportname( img, toDirectory, adjustColor )
        pdb.gimp_file_save( img, imglayer, newfilepathname , newfilepathname )
        gimp.delete( img )
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-photolab-graypoint-batch",
  Photolab_graypoint_batch_description,
  Photolab_graypoint_batch_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Graypoint"),
  "",
  BatchMode_parameters + Photolab_graypoint_parameters,
  [],
  python_fu_photolab_graypoint_batch,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
