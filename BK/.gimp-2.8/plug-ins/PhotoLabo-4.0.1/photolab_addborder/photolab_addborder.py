#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Photolab_addborder python-fu pour Gimp 2.6
# Copyright Raymond Ostertag 2009
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the photolab_addborder.py file in your $HOME/.gimp-2.n/plug-ins.
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
Photolab_addborder_help = _("Create a border around the active layer. Add optionaly a title below the picture. The result can be exported.")                                
Photolab_addborder_description = Photolab_addborder_help
#
Photolab_addborder_batch_help = _("A batch process on images in a directory.")+" "+Photolab_addborder_help
Photolab_addborder_batch_description = Photolab_addborder_batch_help

# user parameters
#
titleGap = 0.05
tagDefault = ("BORDER")

# dialog parameters
#
Standalone_parameters = [
  (PF_IMAGE, "inImage", "Input image", None),
  (PF_DRAWABLE, "inLayer", "Input drawable", None),
]
Standalone_tail_parameters = [
  (PF_TOGGLE, "export", _("Export"), False), 
  (PF_DIRNAME, "expDirectory", ".."+_("Export directory"), os.getcwd() ),
]
BatchMode_parameters = [
  (PF_DIRNAME, "directory", _("Directory"), os.getcwd() ),
  (PF_STRING, "ext", _("File extension"), "jpg" ),
  (PF_DIRNAME, "toDirectory", _("Destination directory"), os.getcwd() ),
]
Photolab_addborder_parameters = [
  (PF_INT, "borderSize", _("Border size"), 100),
  (PF_COLOR, "borderColor", _("Border color"), (255,255,255)),
  (PF_TOGGLE, "addThinBorder", _("Add thin black border"), True), 
  (PF_COLOR, "titleColor", _("Thin border and Title color"), (0,0,0)),
  (PF_TOGGLE, "addTitle", _("Add title"), True), 
  (PF_INT, "titleSize", ".."+_("Title size"), 100),
  (PF_STRING, "title",".."+ _("Title"), "Photo"),
  (PF_FONT, "font", ".."+_("Font"), "Sans"), 
]  

# utilities
#
def tagfilename( 
  filename, #string
  tag, #string
  head, #boolean
  ):
  extfilename = os.path.splitext( filename )[1]
  basefilename = os.path.splitext( filename )[0]
  if( extfilename == "" ):
    extfilename = ".xcf" # add nativ extension is no one is found
  if( head ): 
    return tag+'_'+basefilename+extfilename
  else:
    return basefilename+'_'+tag+extfilename

# main
#                                         
def python_fu_photolab_addborder( 
  inImage,
  inDrawable,
  borderSize,
  borderColor,
  addThinBorder,
  titleColor,
  addTitle,
  titleSize,
  title,
  font,
  export,
  expDirectory ): 
  gimp.context_push()
  pdb.gimp_image_undo_group_start( inImage )
  gimp.progress_init( _("Add border") ) 
  pdb.gimp_selection_none( inImage )
  # resize canvas
  newWidth = inDrawable.width + ( borderSize * 2 )
  offWidth = borderSize
  if( addTitle ):
    newHeight = inDrawable.height + ( borderSize * 2 ) + titleSize
    offHeight = borderSize
  else:
    newHeight = inDrawable.height + ( borderSize * 2 )
    offHeight = borderSize
  # add background layer
  borderLayer = inDrawable.copy( True )
  inImage.add_layer( borderLayer, -1 )
  inImage.lower_layer( borderLayer )
  # resize and set pos of background layer
  offsetX, offsetY = borderLayer.offsets # memorize origin layer position
  borderLayer.resize( newWidth, newHeight, 0, 0 )
  borderLayer.set_offsets( offsetX - borderSize, offsetY - borderSize ) 
  newOffsetX, newOffsetY = borderLayer.offsets # memorize resized layer position
  #
  gimp.set_background( borderColor )   
  pdb.gimp_edit_fill( borderLayer, BACKGROUND_FILL ) #fill background with borderColor
  # add thin black border
  gimp.progress_update( 0.25 ) 
  if( addThinBorder ):
    gimp.set_foreground( titleColor )
    pdb.gimp_rect_select( inImage, offsetX, offsetY, inDrawable.width -1, inDrawable.height-1, CHANNEL_OP_REPLACE, False, 0 )
    pdb.gimp_context_set_brush( "Circle (03)" )
    pdb.gimp_edit_stroke( borderLayer )
    pdb.gimp_selection_none( inImage )
  # add title
  gimp.progress_update( 0.50 ) 
  if( addTitle ):
    gimp.set_foreground( titleColor )
    fontSize = float( titleSize )
    textWidth, textHeight, textAscent, textDescent = pdb.gimp_text_get_extents_fontname( title, fontSize, PIXELS, font )
    ratioWidth = float( textWidth ) / ( newWidth * ( 1 - titleGap ))
    ratioHeight = float( textHeight ) / ( titleSize * ( 1 - titleGap ))
    if( ratioWidth > ratioHeight ):
      # adjusting width
      newFontSize = fontSize / ratioWidth
    else:
      # adjusting height
      newFontSize = fontSize / ratioHeight
    newTextWidth, newTextHeight, newTextAscent, newTextDescent = pdb.gimp_text_get_extents_fontname( title, newFontSize, PIXELS, font )
    titleX = (( newWidth - newTextWidth ) / 2 ) + newOffsetX
    titleY = ( newHeight - titleSize + (( titleSize - newTextHeight ) / 2 )) + newOffsetY
    #DEBUG print newFontSize, titleX, titleY
    pdb.gimp_text_fontname( inImage, borderLayer, titleX, titleY, title, -1, True, newFontSize, PIXELS, font )
    pdb.gimp_floating_sel_anchor( pdb.gimp_image_get_floating_sel( inImage )) 
  # export
  gimp.progress_update( 0.75 ) 
  if( export ):
    # copy layers   
    pdb.gimp_edit_copy( borderLayer )
    newImage = pdb.gimp_edit_paste_as_new() #create a new image
    copyLayer = pdb.gimp_layer_new_from_drawable( inDrawable, newImage )
    newImage.add_layer( copyLayer, -1 )
    copyLayer.set_offsets( borderSize, borderSize ) 
    # save image
    newImage.flatten()
    imageName = pdb.gimp_image_get_name( inImage )
    taggedImageName = tagfilename( imageName, tagDefault, False )
    newfilepathname = expDirectory + os.sep + taggedImageName
    pdb.gimp_file_save( newImage, newImage.layers[0], newfilepathname , newfilepathname )   
    # clean everything
    pdb.gimp_image_delete( newImage )  
    inImage.remove_layer( borderLayer )
  else:
    # resize image is needed to see the border
    pdb.gimp_image_resize_to_layers( inImage )
  #
  pdb.gimp_image_undo_group_end( inImage )
  gimp.context_pop()

register(
  "python-fu-photolab-addborder",
  Photolab_addborder_description,
  Photolab_addborder_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Add border"),
  "*",
  Standalone_parameters + Photolab_addborder_parameters + Standalone_tail_parameters,
  [],
  python_fu_photolab_addborder,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=("gimp20-photolab", locale_directory)   
  )

# batch of main
#

def python_fu_photolab_addborder_batch( 
  dirname, 
  ext,
  toDirectory,
  borderSize,
  borderColor,
  addThinBorder,
  titleColor,
  addTitle,
  titleSize,
  title,
  font ): 
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
        img.flatten() #it's not supposed to work on multi layered files
        imglayer= img.layers[0]
        export = True
        python_fu_photolab_addborder( img, imglayer, borderSize, borderColor, addThinBorder, titleColor, addTitle, titleSize, title, font, export, toDirectory );
        pdb.gimp_image_delete( img )
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-photolab-addborder-batch",
  Photolab_addborder_batch_description,
  Photolab_addborder_batch_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Add border"),
  "",
  BatchMode_parameters + Photolab_addborder_parameters,
  [],
  python_fu_photolab_addborder_batch,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
