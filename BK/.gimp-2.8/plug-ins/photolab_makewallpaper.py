#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Photolab_make_wallpaper python-fu pour Gimp 2.6
# Copyright Raymond Ostertag 2009
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the Photolab_make_wallpaper.py file in your $HOME/.gimp-2.n/plug-ins.
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
Photolab_make_wallpaper_help = _("Create one or more wallpapers from the active layer. The size can be standard, selected from a list, or customized. The cutting mode set which part of the image should be keeped. If no cutting is asked then the residual areas are filled in black.")                                
Photolab_make_wallpaper_description = Photolab_make_wallpaper_help
#
Photolab_make_wallpaper_batch_help = _("A batch process on images in a directory.")+" "+Photolab_make_wallpaper_help
Photolab_make_wallpaper_batch_description = Photolab_make_wallpaper_batch_help

# parameters    
XGA_res = {
    'XGA':( 1024, 768 ), #XGA
    'WXGA': ( 1280, 800 ), #WXGA
    'SXGA': ( 1280, 1024 ), #SXGA
    'WSXGA': ( 1600, 1024 ), #WSXGA
    'UXGA': ( 1600, 1200 ), #UXGA
    'WUXGA': ( 1920, 1200 ), #WUXGA
    'QXGA': ( 2048, 1536 ), #QXGA
    'WQXGA' : ( 2560, 1600 ), #WQXGA
}

# main
#                                         
def python_fu_photolab_make_wallpaper( 
  inImage,
  inDrawable,
  toDirectory,
  cutMode,
  border,
  custom,
  customWidth,
  customHeight,
  XGA,
  WXGA,
  SXGA,
  WSXGA,
  UXGA,
  WUXGA,
  QXGA,
  WQXGA ): 
  gimp.context_push()
  originalWidth = inDrawable.width
  originalHeight = inDrawable.height
  if( custom ):
    XGA_res['custom'] = ( customWidth, customHeight )
  for keys in XGA_res:  
    if vars()[keys]:
      ratioWidth = float( originalWidth ) / float( XGA_res[keys][0] )
      ratioHeight = float( originalHeight ) / float( XGA_res[keys][1] )
      ratioWidthHeight = float( ratioWidth ) / float( ratioHeight )
      if( cutMode == "preserve" ): #no cropping
        if (ratioWidthHeight >= 1 ):
          newWidth = originalWidth
          offWidth = 0
          newHeight = int( originalWidth * ( float( XGA_res[keys][1] ) / float( XGA_res[keys][0] )))
          offHeight = int( abs( originalHeight - newHeight ) /2)
        else:
          newWidth = int( originalHeight * ( float( XGA_res[keys][0] ) / float( XGA_res[keys][1] )))
          offWidth = int( abs( originalWidth - newWidth ) / 2 )
          newHeight = originalHeight
          offHeight = 0       
        pdb.gimp_edit_copy( inDrawable )
        newImage = pdb.gimp_edit_paste_as_new() #create a new image
        pdb.gimp_image_resize( newImage, newWidth, newHeight, offWidth, offHeight ) #resize canvas
        backgroundLayer = gimp.Layer( newImage, "background", newWidth, newHeight, RGB_IMAGE, 0, NORMAL_MODE )
        newImage.add_layer( backgroundLayer, -1 )
        gimp.set_background( 0,0,0 ) 
        pdb.gimp_edit_fill( backgroundLayer, BACKGROUND_FILL ) #fill background in black
        newImage.flatten()                                  
      else:
        if( ratioWidthHeight >= 1 ):
          newWidth = int( originalHeight * ( float( XGA_res[keys][0] ) / float( XGA_res[keys][1] )))
          if( cutMode == "topLeft" ): #keep top or left
            offWidth = 0
          elif( cutMode == "bottomRight"): #keep bottom or right
            offWidth = int( abs( originalWidth - newWidth ))
          else:
            offWidth = int( abs( originalWidth - newWidth ) / 2 )
          newHeight = originalHeight
          offHeight = 0
        else:
          newWidth = originalWidth
          offWidth = 0
          newHeight = int( originalWidth * ( float( XGA_res[keys][1] ) / float( XGA_res[keys][0] )))
          if( cutMode == "topLeft" ): #keep top or left
            offHeight = 0
          elif( cutMode == "bottomRight"): #keep bottom or right
            offHeight = int( abs( originalHeight - newHeight ))          
          else:
            offHeight = int( abs( originalHeight - newHeight ) /2)
        pdb.gimp_edit_copy( inDrawable )
        newImage = pdb.gimp_edit_paste_as_new() #create a new image
        newImage.flatten()
        pdb.gimp_image_crop( newImage, newWidth, newHeight, offWidth, offHeight) #crop new image  
      if( border != 0 ): #add border
        borderWidth = ( XGA_res[keys][0] ) * ( border / 100 )
        borderHeight = ( XGA_res[keys][1] ) * ( border / 100 )
        pdb.gimp_image_scale_full( newImage, XGA_res[keys][0]-borderWidth, XGA_res[keys][1]-borderHeight, INTERPOLATION_CUBIC ) #scale new image     
        pdb.gimp_image_resize( newImage, XGA_res[keys][0], XGA_res[keys][1], borderWidth / 2 , borderHeight / 2 ) #resize canvas
        backgroundLayer = gimp.Layer( newImage, "background", XGA_res[keys][0], XGA_res[keys][1], RGB_IMAGE, 0, NORMAL_MODE )
        newImage.add_layer( backgroundLayer, -1)
        gimp.set_background( 0,0,0)
        pdb.gimp_edit_fill( backgroundLayer, BACKGROUND_FILL ) #fill background in black  
        newImage.flatten()                                             
      else:
        pdb.gimp_image_scale_full( newImage, XGA_res[keys][0], XGA_res[keys][1], INTERPOLATION_CUBIC ) #scale new image
      imageName = pdb.gimp_image_get_name( inImage )
      imageBasename = os.path.splitext( imageName )[0]
      imageExtname = os.path.splitext( imageName )[1]
      if( custom ):
        newfilepathname = toDirectory + os.sep + imageBasename + '_' + str( XGA_res[keys][0] ) +'x' + str( XGA_res[keys][1] )+ '.jpg'      
      else:
        newfilepathname = toDirectory + os.sep + imageBasename + '_' + keys+ '_' + str( XGA_res[keys][0] ) +'x' + str( XGA_res[keys][1] )+ '.jpg'
      pdb.gimp_file_save( newImage, newImage.layers[0], newfilepathname , newfilepathname )   
      pdb.gimp_image_delete( newImage )  
  gimp.context_pop()

register(
  "python-fu-photolab-make-wallpaper",
  Photolab_make_wallpaper_description,
  Photolab_make_wallpaper_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Make wallpaper"),
  "*",
  [
    (PF_IMAGE, "inImage", "Input image", None),
    (PF_DRAWABLE, "inLayer", "Input drawable", None),     
    (PF_DIRNAME, "toDirectory", _("Destination directory"), os.getcwd() ),
    (PF_RADIO, "cutMode", _("Cutting mode"), "center", ((_("Center"),"center"), (_("Keep Top / Left"),"topLeft"), (_("Keep Bottom / Right"),"bottomRight"), (_("Don't cut"),"preserve"))), #str
    (PF_SPINNER, "border", _("Border percentage size (0:no border)"), 0, (0,50,1)),
    (PF_TOGGLE, "custom", _("Custom"), True),    
    (PF_INT, "customWidth", ".."+_("Custom Width"), 1920), 
    (PF_INT, "customHeight", ".."+_("Custom Height"), 1200),
    (PF_TOGGLE, "XGA", ("XGA 1024x768"), False),
    (PF_TOGGLE, "WXGA", ("WXGA 1280x800"), False),
    (PF_TOGGLE, "SXGA", ("SXGA 1280x1024"), False),
    (PF_TOGGLE, "WSXGA", ("WSXGA 1600x1025"), False),
    (PF_TOGGLE, "UXGA", ("UXGA 1600x1200"), False),
    (PF_TOGGLE, "WUXGA", ("WUXGA 1920x1200"), False),
    (PF_TOGGLE, "QXGA", ("QXGA 2048x1536"), False),
    (PF_TOGGLE, "WQXGA", ("WQXGA 2560x1600"), False),
  ],
  [],
  python_fu_photolab_make_wallpaper,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=("gimp20-photolab", locale_directory)   
  )

# batch of main
#

def python_fu_photolab_make_wallpaper_batch( 
  dirname, 
  ext,
  toDirectory,
  cutMode,
  border,
  custom,
  customWidth,
  customHeight,
  XGA,
  WXGA,
  SXGA,
  WSXGA,
  UXGA,
  WUXGA,
  QXGA,
  WQXGA ): 
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      #Start of process
      #DEBUG pdb.gimp_message( _("The selected directory has %s files to handle") %(str( len( filepathnames ))));
      for filepathname in filepathnames:
        img = pdb.gimp_file_load( filepathname , filepathname )
        img.flatten()
        imglayer = img.layers[0]
        python_fu_photolab_make_wallpaper( img, imglayer, toDirectory, cutMode, border, custom, customWidth, customHeight, XGA, WXGA, SXGA, WSXGA, UXGA, WUXGA, QXGA, WQXGA );
        gimp.delete( img )
      # End of process         
    else:
      pdb.gimp_message( _("%s don't have files to handle") %(dirname ))      
  else:
    pdb.gimp_message( _("%s don't exist") %(dirname) )

register(
  "python-fu-photolab-make-wallpaper-batch",
  Photolab_make_wallpaper_batch_description,
  Photolab_make_wallpaper_batch_help,
  "Raymond Ostertag",
  "GPL License",
  "2009",
  _("Make wallpaper"),
  "",
  [
    (PF_DIRNAME, "directory", _("Source directory"), os.getcwd() ),
    (PF_STRING, "ext", _("File extension"), "jpg" ),
    (PF_DIRNAME, "toDirectory", _("Destination directory"), os.getcwd() ),    
    (PF_RADIO, "cutMode", _("Cutting mode"), "center", (("Center","center"), ("Keep Top-Left","topLeft"), ("Keep Bottom-Right","bottomRight"), ("Don't cut","preserve"))), #str
    (PF_SPINNER, "border", _("Border percentage size (0:no border)"), 0, (0,50,1)),
    (PF_TOGGLE, "custom", ("Custom"), False),    
    (PF_INT, "customWidth", ".."+_("Custom Width"), 1920), 
    (PF_INT, "customHeight", ".."+_("Custom Height"), 1200),
    (PF_TOGGLE, "XGA", ("XGA 1024x768"), True),
    (PF_TOGGLE, "WXGA", ("WXGA 1280x800"), True),
    (PF_TOGGLE, "SXGA", ("SXGA 1280x1024"), True),
    (PF_TOGGLE, "WSXGA", ("WSXGA 1600x1025"), True),
    (PF_TOGGLE, "UXGA", ("UXGA 1600x1200"), True),
    (PF_TOGGLE, "WUXGA", ("WUXGA 1920x1200"), True),
    (PF_TOGGLE, "QXGA", ("QXGA 2048x1536"), True),
    (PF_TOGGLE, "WQXGA", ("WQXGA 2560x1600"), True),
  ],
  [],
  python_fu_photolab_make_wallpaper_batch,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Batch works"),
  domain=("gimp20-photolab", locale_directory)   
  )

main()
