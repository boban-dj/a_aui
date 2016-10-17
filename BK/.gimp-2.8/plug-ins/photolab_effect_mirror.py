#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Photolab_effect_mirror python-fu pour Gimp 2.6
# Copyright Raymond Ostertag 2009
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the photolab_effect_mirror.py file in your $HOME/.gimp-2.n/plug-ins.
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
Photolab_effect_mirror_help = _("Create one or four mirror effects from a image. The result can be exported.")                                
Photolab_effect_mirror_description = Photolab_effect_mirror_help
#
Photolab_effect_mirror_batch_help = _("A batch process on images in a directory.")+" "+Photolab_effect_mirror_help                   
Photolab_effect_mirror_batch_description = Photolab_effect_mirror_batch_help

# dialog parameters
#
Standalone_parameters = [
  (PF_IMAGE, "inImage", "Input image", None),
  (PF_DRAWABLE, "inLayer", "Input drawable", None),
]
Standalone_export_parameters = [
  (PF_TOGGLE, "export", _("Export"), False), 
  (PF_DIRNAME, "expDirectory", ".."+_("Export directory"), os.getcwd() ),
]
BatchMode_parameters = [
  (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
  (PF_STRING, "ext", _("File extension"), "jpg" ),
  (PF_DIRNAME, "toDirectory", _("Destination directory"), os.getcwd() ),
]
Photolab_effect_mirror_parameters = [
  (PF_RADIO, "whatToDo", _("What to do?"), "one", ( (_("All four effects"),"all"), (_("Only the effect below"),"one") )), #str  
  (PF_RADIO, "orientation", ".."+_("Mirror orientation"), "h", ((_("Horizontal"),"h"), (_("Vertical"),"v"))), #str
  (PF_RADIO, "keepSide", ".."+_("Keep side"), "lt", ((_("Left/Top"),"lt"), (_("Right/Bottom"),"rb"))), #str
]  

# main
#               
def python_fu_photolab_effect_mirror_mirrorname( 
  orientation,
  keepSide ):
  if orientation == "h":
    if keepSide == "rb" :
      return "h_right"
    elif keepSide == "lt" :
      return "h_left"
    else:
      return "unknown"
  elif orientation == "v":
    if keepSide == "rb" :
      return "v_bottom"
    elif keepSide == "lt" :
      return "v_top"
    else:
      return "unknown"
  
def python_fu_photolab_effect_mirror_exportname( 
  inImage,  
  toDirectory, 
  orientation,
  keepSide ):
  imageName = pdb.gimp_image_get_name( inImage )
  imageBasename = os.path.splitext( imageName )[0]
  imageExtname = os.path.splitext( imageName )[1]
  if imageExtname == "" or imageExtname == ".xcf" :
    imageExtname = ".jpg"
  newfilepathname = toDirectory + os.sep + imageBasename + '_MIRROR_' + python_fu_photolab_effect_mirror_mirrorname( orientation, keepSide ) + imageExtname 
  return newfilepathname

def python_fu_photolab_effect_mirror_from_layer( 
  inImage,
  inDrawable,
  orientation,
  keepSide ):
  #work on copy
  copyLayer = inDrawable.copy( )
  inImage.add_layer( copyLayer, 0 )
  #add mirror layer
  mirrorLayer = copyLayer.copy( )
  inImage.add_layer( mirrorLayer, 0 )
  #transform mirror layer
  horizontalAxisPos = float(mirrorLayer.width) / 2
  verticalAxisPos = float(mirrorLayer.height) / 2
  if orientation == "h":
    mirrorLayer = pdb.gimp_drawable_transform_flip_simple( mirrorLayer, ORIENTATION_HORIZONTAL, False, horizontalAxisPos, False )
  elif orientation == "v":
    mirrorLayer = pdb.gimp_drawable_transform_flip_simple( mirrorLayer, ORIENTATION_VERTICAL, False, verticalAxisPos, False )  
  #add mask to mirror layer
  mirrorMask = mirrorLayer.create_mask( ADD_BLACK_MASK )
  pdb.gimp_layer_add_mask( mirrorLayer, mirrorMask )
  XMed = float( mirrorLayer.width ) / 2.0
  YMed = float( mirrorLayer.height ) / 2.0
  if orientation == "h":
    if keepSide == "rb":  
      X1 = 0.0
      X2 = XMed
      Y1 = 0.0
      Y2 = float( mirrorLayer.height )
    elif keepSide == "lt":
      X1 = XMed
      X2 = float( mirrorLayer.width )
      Y1 = 0.0
      Y2 = float( mirrorLayer.height )  
    else:
      pass 
  elif orientation == "v":
    if keepSide == "rb":  
      X1 = 0.0
      X2 = float( mirrorLayer.width )
      Y1 = 0.0
      Y2 = YMed
    elif keepSide == "lt":
      X1 = 0.0
      X2 = float( mirrorLayer.width )
      Y1 = YMed
      Y2 = float( mirrorLayer.height )  
    else:
      pass 
  else:
    pass  
  pdb.gimp_rect_select( inImage, X1, Y1, X2, Y2, CHANNEL_OP_REPLACE, False, 0 )
  pdb.gimp_edit_fill( mirrorMask, WHITE_FILL )
  pdb.gimp_selection_none( inImage )
  #merge down mirror layer
  mirrorLayer.apply_mask
  mergedLayer = pdb.gimp_image_merge_down( inImage, mirrorLayer, CLIP_TO_BOTTOM_LAYER )
  pdb.gimp_drawable_set_name( mergedLayer, python_fu_photolab_effect_mirror_mirrorname( orientation, keepSide ))
  return mergedLayer
                          
def python_fu_photolab_effect_mirror( 
  inImage,
  inDrawable,
  whatToDo,
  orientation,
  keepSide,
  export,
  expDirectory ): 
  gimp.context_push()
  pdb.gimp_image_undo_group_start( inImage )
  #apply effect
  if whatToDo == "one":
    newMirrorLayer = python_fu_photolab_effect_mirror_from_layer( inImage, inDrawable, orientation, keepSide )
    if export:
      newfilepathname = python_fu_photolab_effect_mirror_exportname( inImage, expDirectory, orientation, keepSide )
      pdb.gimp_file_save( inImage, newMirrorLayer, newfilepathname , newfilepathname )
      inImage.remove_layer( newMirrorLayer )
  elif whatToDo == "all":
    newMirrorLayer = python_fu_photolab_effect_mirror_from_layer( inImage, inDrawable, "h", "lt" )
    if export:
      newfilepathname = python_fu_photolab_effect_mirror_exportname( inImage, expDirectory, "h", "lt" )
      pdb.gimp_file_save( inImage, newMirrorLayer, newfilepathname , newfilepathname )
      inImage.remove_layer( newMirrorLayer )
    newMirrorLayer = python_fu_photolab_effect_mirror_from_layer( inImage, inDrawable, "h", "rb" )
    if export:
      newfilepathname = python_fu_photolab_effect_mirror_exportname( inImage, expDirectory, "h", "rb" )
      pdb.gimp_file_save( inImage, newMirrorLayer, newfilepathname , newfilepathname )
      inImage.remove_layer( newMirrorLayer )  
    newMirrorLayer = python_fu_photolab_effect_mirror_from_layer( inImage, inDrawable, "v", "lt" )
    if export:
      newfilepathname = python_fu_photolab_effect_mirror_exportname( inImage, expDirectory, "v", "lt" )
      pdb.gimp_file_save( inImage, newMirrorLayer, newfilepathname , newfilepathname )
      inImage.remove_layer( newMirrorLayer )  
    newMirrorLayer = python_fu_photolab_effect_mirror_from_layer( inImage, inDrawable, "v", "rb" )
    if export:
      newfilepathname = python_fu_photolab_effect_mirror_exportname( inImage, expDirectory, "v", "rb" )
      pdb.gimp_file_save( inImage, newMirrorLayer, newfilepathname , newfilepathname )
      inImage.remove_layer( newMirrorLayer )  
  #
  pdb.gimp_image_undo_group_end( inImage )
  gimp.context_pop()  

register(
  "python-fu-photolab-effect_mirror",
  Photolab_effect_mirror_description,
  Photolab_effect_mirror_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Effect:mirror"),
  "*",
  Standalone_parameters + Photolab_effect_mirror_parameters + Standalone_export_parameters,
  [],
  python_fu_photolab_effect_mirror,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=("gimp20-photolab", locale_directory)   
  )

# batch of main
#
def python_fu_photolab_effect_mirror_batch( 
  dirname, 
  ext,
  toDirectory,
  whatToDo,
  orientation,
  keepSide ):
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
        python_fu_photolab_effect_mirror( img, imglayer, whatToDo, orientation, keepSide, True, toDirectory );
        gimp.delete( img )
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-photolab-effect_mirror-batch",
  Photolab_effect_mirror_batch_description,
  Photolab_effect_mirror_batch_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Effect:mirror"),
  "",
  BatchMode_parameters + Photolab_effect_mirror_parameters,
  [],
  python_fu_photolab_effect_mirror_batch,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
