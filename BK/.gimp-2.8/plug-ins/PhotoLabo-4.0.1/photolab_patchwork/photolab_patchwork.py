#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Photolab_patchwork python-fu pour Gimp 2.6
# Copyright Raymond Ostertag 2009
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the photolab_patchwork.py file in your $HOME/.gimp-2.n/plug-ins.
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
Photolab_patchwork_help = _("Create a patchwork of images taken in the same directory. Two templates for 3 or 4 images are available. The paper size are to be choosen in a list of presets. Add an optional border around each images. Fill the background as plain color, pattern or image." )                                
Photolab_patchwork_description = Photolab_patchwork_help

# constant
#
paperSizes = { '13x17cm':(13/2.54,17/2.54), '20x27cm':(20/2.54,27/2.54), '30x40cm':(30/2.54,40/2.54) }
templateSizes = { '3u':(3,0.60,0.03), '4s':(4,0.495) }

# process
#                                         
def python_fu_photolab_patchwork_process( 
  filepathnames,
  template,
  imageSize,
  resolution,
  paper,
  borderSize,
  borderColor,
  bgtype,
  bgtypeColorIs,
  bgtypePatternIs,
  bgtypeImageIs ):
  if paperSizes.has_key( paper ):
   if templateSizes.has_key( template ):
     gimp.context_push()
     bgColor = gimp.get_background()
     #calculate Gimp file size
     if template == "3u":
       paperH = int( paperSizes[ paper ][1] * resolution )
       paperW = int( paperSizes[ paper ][0] * resolution )
     elif template == "4s":
       paperH = int( paperSizes[ paper ][0] * resolution )
       paperW = int( paperSizes[ paper ][1] * resolution )
     else:
       pdb.gimp_message( _("wrong template %s, aborting") %(template) )
     #DEBUG print paperH, paperW
     #create image with a background
     pwImage = gimp.Image( paperW, paperH, RGB )
     bgLayer = gimp.Layer( pwImage, "Background", paperW, paperH, RGB_IMAGE, 100, NORMAL_MODE )
     pwImage.add_layer( bgLayer, 0 )
     gimp.set_background( bgtypeColorIs )   
     pdb.gimp_edit_fill( bgLayer, BACKGROUND_FILL)
     if bgtype == "bgtypePattern":
       patternActiv = pdb.gimp_context_get_pattern( )
       pdb.gimp_context_set_pattern( bgtypePatternIs )
       pdb.gimp_edit_fill( bgLayer, PATTERN_FILL)
       pdb.gimp_context_set_pattern( patternActiv )
     if bgtype == "bgtypeImage":
       bglayerImage = pdb.gimp_file_load_layer( pwImage, bgtypeImageIs )
       pwImage.add_layer( bglayerImage , 0 )
       ratioHW = ( float(bglayerImage.height) / paperH ) / ( float(bglayerImage.width) / paperW )
       if ratioHW >= 1:
         layerW = int( paperW )
         layerH = int( layerW * ( float(bglayerImage.height) / float(bglayerImage.width) ))
       else:      
         layerH = int( paperH )
         layerW = int( layerH * ( float(bglayerImage.width) / float(bglayerImage.height) ))    
       pdb.gimp_layer_scale_full( bglayerImage, layerW, layerH, 0, INTERPOLATION_CUBIC )
       bgLayer = pdb.gimp_image_merge_down( pwImage, bglayerImage, CLIP_TO_BOTTOM_LAYER )
     #DEBUG print layerH, layerW
     #open images as layers
     maxFile = int( templateSizes[ template ][0] )
     nrFile = 1  
     for filepathname in filepathnames:
       if nrFile <= maxFile:
         layerName = str( os.path.basename(filepathname))
         layerName = pdb.gimp_file_load_layer( pwImage, filepathname )
         pwImage.add_layer( layerName , 0 )
         #put layer at bottom-1 in the stack
         pdb.gimp_image_lower_layer_to_bottom( pwImage, layerName )
         pdb.gimp_image_raise_layer( pwImage, layerName )
         #calculate Layer size  
         ratioHW = ( float(layerName.height) / paperH ) / ( float(layerName.width) / paperW )
         reduceRatio = float(imageSize) / 100
         if reduceRatio > templateSizes[ template ][1]:
           reduceRatio = templateSizes[ template ][1]
         if ratioHW <= 1:
           layerW = int( paperW * reduceRatio )
           layerH = int( layerW * ( float(layerName.height) / float(layerName.width) ))
         else:      
           layerH = int( paperH * reduceRatio )
           layerW = int( layerH * ( float(layerName.width) / float(layerName.height) ))    
         pdb.gimp_layer_scale_full( layerName, layerW, layerH, 0, INTERPOLATION_CUBIC)
         if template == "3u":
           #calculate layer location for template 3u
           XPos = int( paperW * templateSizes[template][2] )
           YPos = XPos
           if nrFile == 1:
             X1 = XPos
             Y1 = YPos
           if nrFile == 2:
             X1 = int( paperW /2.0 ) - int( layerW /2.0 )
             Y1 = int( paperH /2.0 ) - int( layerH /2.0 )
           if nrFile == 3:
             X1 = int( paperW - XPos - layerW )
             Y1 = int( paperH - YPos - layerH )   
           X2 = X1 + layerW
           Y2 = Y1 + layerH           
         elif template == "4s":
           #calculate layer location for template 4u
           XPos = int( (2.0/3.0) * (( paperW / 2.0 ) - layerW ))
           YPos = int( (2.0/3.0) * (( paperH / 2.0 ) - layerH ))  
           if nrFile == 1:
             X1 = XPos
             Y1 = YPos
           if nrFile == 2:
             X1 = int( paperW /2.0 ) + int( XPos /2.0 )
             Y1 = YPos
           if nrFile == 3:
             X1 = XPos
             Y1 = int( paperH /2.0 ) + int( YPos /2.0 )
           if nrFile == 4:
             X1 = int( paperW /2.0 ) + int( XPos /2.0 )
             Y1 = int( paperH /2.0 ) + int( YPos /2.0 )          
           X2 = X1 + layerW
           Y2 = Y1 + layerH
         else:
           pdb.gimp_message( _("wrong template %s, aborting") %(template) )
         #
         layerName.translate( X1, Y1 )
         nrFile = nrFile +1
         #DEBUG print nrFile, layerName.height, layerName.width, X1, Y1
         #start border
         if borderSize > 0:
           gimp.set_background( borderColor ) 
           borderLayer = pdb.gimp_layer_new( pwImage, layerW+2*borderSize, layerH+2*borderSize, RGBA_IMAGE, "border", 100, NORMAL_MODE )
           pwImage.add_layer( borderLayer, 0 )
           #put layer at bottom-1 in the stack
           pdb.gimp_image_lower_layer_to_bottom( pwImage, borderLayer )
           pdb.gimp_image_raise_layer( pwImage, borderLayer )
           #
           borderLayer.translate( X1-borderSize, Y1-borderSize )
           pdb.gimp_edit_fill( borderLayer, BACKGROUND_FILL )
         #end border
       else:
         pass
     #
     flattenLayer = pdb.gimp_image_flatten( pwImage )
     pwImageBaseName = os.path.splitext( os.path.basename( filepathnames[0] ) )[0]
     pwImageExtName = os.path.splitext( os.path.basename( filepathnames[0] ) )[1]
     pwImageName = os.path.dirname( filepathnames[0] ) + os.sep + pwImageBaseName + "_PATCHWORK." + pwImageExtName
     pdb.gimp_file_save( pwImage, flattenLayer, pwImageName, pwImageName, run_mode=0 )
     gimp.delete( pwImage )
     gimp.set_background( bgColor )
     gimp.context_pop()
   else:
     pdb.gimp_message( _("wrong template %s, aborting") %(template) )   
  else:
   pdb.gimp_message( _("wrong paper size %s, aborting") %(paper) )
  pass

# main
#
def python_fu_photolab_patchwork( 
  dirname, 
  ext,
  template,
  imageSize,
  resolution,
  paper,
  borderSize,
  borderColor,
  bgtype,
  bgtypeColorIs,
  bgtypePatternIs,
  bgtypeImageIs ):
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      #Start of process
      #DEBUG pdb.gimp_message( _("The selected directory has %s files to handle") %(str( len( filepathnames ))));
      python_fu_photolab_patchwork_process( filepathnames, template, imageSize, resolution, paper, borderSize, borderColor, bgtype, bgtypeColorIs, bgtypePatternIs, bgtypeImageIs ),
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname) )      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-photolab-patchwork",
  Photolab_patchwork_description,
  Photolab_patchwork_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Patchwork"),
  "",
  [
    (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("File extension"), "jpg" ),
    (PF_RADIO, "template", _("Template"), "4s", ((_("Vertical: 3 images up-left to bottom-right"),"3u"), (_("Horizontal: 4 images side by side"),"4s"))), #str
    (PF_SLIDER, "imageSize", _("Image size (%)"), 48, (35,60,1)), #float
    (PF_SLIDER, "resolution", _("Resolution (ppi)"), 300, (200,600,10)), #float    
    (PF_RADIO, "paper", _("Paper size"), "20x27cm", (("13x17 cm","13x17cm"), ("20x27 cm","20x27cm"), ("30x40 cm","30x40cm"))), #str
    (PF_INT, "borderSize", _("Border size (px)"), 5 ),
    (PF_COLOR, "borderColor", _("Border color"), (0,0,0)),
    (PF_RADIO, "bgType", _("Type of background"), "bgtypeColor", ((_("Plain color"),"bgtypeColor"), (_("Pattern"),"bgtypePattern"), (_("Image"),"bgtypeImage"))), #str
    (PF_COLOR, "bgtypeColorIs", ".."+_("Background color"), (255,255,255)),
    (PF_PATTERN, "bgtypePatternIs", ".."+_("Background pattern"), ""), #str
    (PF_FILENAME, "bgtypeImageIs", ".."+_("Background image"), ""), #str
  ],
  [],
  python_fu_photolab_patchwork,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
