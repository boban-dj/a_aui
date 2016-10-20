#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Photolab :: photoduplicate
# Copyright Raymond Ostertag 2007-2009
# License GNU/GPL

# Version 2.1
# - ported to GIMP-2.6
# - added valid images "*"
# Version 2.0
# - ported to GIMP-2.4
# - use gettext
# Version 1.2
# - Line 81, Changed gimp_edit_fill by gimp_drawable_fill
# Version 1.1
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *
import math

# i18n
#
import gettext
locale_directory = gimp.locale_directory 
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_photoduplicate_help = _("Duplicate a portrait on paper of different size for printing")
Photolab_photoduplicate_description = Photolab_photoduplicate_help

# Constants
#
A6_300_width = 1240
A6_300_height = 1754
A4_300_width = 2480
A4_300_height = 3508
B5_300_width = 2079
B5_300_height = 2953
Legal_300_width = 2550
Legal_300_height = 4200
Letter_300_width = 2550
Letter_300_height = 3300
Custom_height = A4_300_height
Custom_width = A4_300_width

def photomaton_copy_layer_to_image( activLayer, Image, newLayername, PosX, PosY ) :
   newLayer = gimp.Layer( Image, newLayername, activLayer.width, activLayer.height, RGBA_IMAGE, 100, NORMAL_MODE )
   Image.add_layer( newLayer, 0)
   newLayer.fill( TRANSPARENT_FILL )
   #
   pdb.gimp_edit_copy( activLayer )
   floatingLayer= pdb.gimp_edit_paste( newLayer, 1 )
   pdb.gimp_floating_sel_anchor( floatingLayer )
   newLayer.flush( )
   newLayer.set_offsets(PosX, PosY)

def photomaton_copy_scale_layer_to_image( activLayer, Image, newLayername, PosX, PosY, SizeX, SizeY ) :
   newLayer = gimp.Layer( Image, newLayername, activLayer.width, activLayer.height, RGBA_IMAGE, 100, NORMAL_MODE )
   Image.add_layer( newLayer, 0)
   newLayer.fill( TRANSPARENT_FILL )
   #
   pdb.gimp_edit_copy( activLayer )
   floatingLayer= pdb.gimp_edit_paste( newLayer, 1 )
   pdb.gimp_floating_sel_anchor( floatingLayer )
   newLayer.flush( )
   newLayer.scale (SizeX, SizeY, 0)
   newLayer.set_offsets(PosX, PosY)

def python_fu_photomaton( inImage, inDrawable, Paper_Size, Paper_width, Paper_height, Conserve_Size, Duplication, Border ):
   if Paper_Size == 0 :
     image1_width = A6_300_width
     image1_height = A6_300_height
   elif Paper_Size == 1 :
     image1_width = A4_300_width
     image1_height = A4_300_height
   elif Paper_Size == 2 :
     image1_width = B5_300_width
     image1_height = B5_300_height
   elif Paper_Size == 3 :
     image1_width = Legal_300_width
     image1_height = Legal_300_height
   elif Paper_Size == 4 :
     image1_width = Letter_300_width
     image1_height = Letter_300_height
   elif Paper_Size == 5 :
     image1_width = Paper_width
     image1_height = Paper_height
   image1 = gimp.Image( image1_width, image1_height, RGB ) #Create a new A4 300 DPI image
   layer_bg = gimp.Layer(image1, _("Background"), image1_width, image1_height, RGB_IMAGE, 100, NORMAL_MODE)
   pdb.gimp_drawable_fill( layer_bg, WHITE_FILL)
   image1.add_layer(layer_bg, 0)
   #
   if Border < 0 :
      pdb.gimp_message (_("Negative border is not possible, border set to 0"))
      Border = 0
   #
   if Conserve_Size :
      width = inDrawable.width
      height = inDrawable.height
      if (width > image1_width) or (height > image1_height) :
        pdb.gimp_message (_("Portrait size bigger the Paper size"))
        PosX = 0
        PosY = 0
        photomaton_copy_layer_to_image( inDrawable, image1, inDrawable.name, PosX, PosY )
      else :
        Iteration_X = image1_width / (width + Border)
        MetaBorder_X = ( image1_width - Iteration_X * width - (Iteration_X-1) * Border) /2
        Iteration_Y = image1_height / (height + Border)
        MetaBorder_Y = ( image1_height - Iteration_Y * height - (Iteration_Y-1) * Border) /2
        for y in range( Iteration_Y ) :
          PosY = y * (height + Border) + MetaBorder_Y
          for x in range( Iteration_X ) :
            PosX = x * (width + Border) + MetaBorder_X
            photomaton_copy_layer_to_image( inDrawable, image1, inDrawable.name, PosX, PosY )
   else :
      if Duplication <= 0 :
        pdb.gimp_message (_("Negative or Nul duplication is not possible, duplication set to 1"))
        Duplication = 1
      Duplication_XY = int ( math.ceil( math.sqrt( Duplication )))
      if Duplication_XY < 1 :
        Duplication_XY = 1
      max_width = ( image1_width - ( Duplication_XY +1 ) * Border ) / Duplication_XY
      max_height = ( image1_height - ( Duplication_XY +1 ) * Border ) / Duplication_XY
      scale_X = max_width / inDrawable.width
      scale_Y = max_height / inDrawable.height
      scale = min ( scale_X, scale_Y )
      Size_X = scale * inDrawable.width
      Size_Y = scale * inDrawable.height
      Border_X = ( image1_width - Duplication_XY * Size_X ) / ( Duplication_XY +1)
      Border_Y = ( image1_height - Duplication_XY * Size_Y ) / ( Duplication_XY +1)
      if (Size_X < 1) or (Size_Y < 1) :
        pdb.gimp_message (_("Final size of portrait is less than 1 pixel !! Decrease duplication"))
      else :
        Counter = 0
        for y in range( Duplication_XY) :
          PosY = y * (Size_Y + Border_Y) + Border_Y
          for x in range( Duplication_XY ) :
            PosX = x * (Size_X + Border_X) + Border_X
            photomaton_copy_scale_layer_to_image( inDrawable, image1, inDrawable.name, PosX, PosY, Size_X, Size_Y )
            Counter = Counter +1
            if Counter == Duplication : break
          if Counter == Duplication : break
   gimp.Display( image1 )
   gimp.displays_flush( )

register(
  "Photoduplicate",
  Photolab_photoduplicate_description,
  Photolab_photoduplicate_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Photo duplicate"),
  "*",
  [
    (PF_IMAGE, "inImage", "Input image", None),
    (PF_DRAWABLE, "inLayer", "Input drawable", None),     
    (PF_RADIO, "Paper_Size", _("Paper sizes (300 DPI)"), 0,
       (("A6", 0), ("A4", 1), ("B5", 2), ("Legal", 3), ("Letter", 4), (_("Custom"),5))),
    (PF_INT, "Paper_width", _("Width of the Paper for CUSTOM Paper"),Custom_width),
    (PF_INT, "Paper_height", _("Height of the Paper for CUSTOM Paper"),Custom_height),
    (PF_TOGGLE, "Conserve_Size", _("Conserve Size"), TRUE),
    (PF_INT, "Duplication", _("Number of duplications"), 4),
    (PF_INT, "Border", _("Offset between each duplication"), 10),
  ],
  [],
  python_fu_photomaton,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
