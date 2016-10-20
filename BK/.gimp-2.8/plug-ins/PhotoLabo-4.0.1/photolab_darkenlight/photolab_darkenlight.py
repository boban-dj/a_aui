#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: darkenlight
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.1
# - ported to GIMP-2.6
# - added valid images "*"
# Version 2.0.2
# - valueImage.layers[2](value) was [0](hue) and wrong
# Version 2.0.1
# - restricted to RGB images
# Version 2.0
# - ported to GIMP-2.4
# - use gettext
# Version 1.1
# - Added threshold for high luminosity pixels
# Version 1.0
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *

# i18n
#
import gettext
locale_directory = gimp.locale_directory
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_darkenlight_help = _("Add a layer in softlight mode. A layer mask is added and filled with the value channel.")
Photolab_darkenlight_description = Photolab_darkenlight_help

# Main Program
#
def python_fu_darkenlight( 
  inImage,
  inDrawable,
  brightness ): 
  #
  width= inDrawable.width
  height= inDrawable.height
  brightness= brightness +127 #Values from 0 to 255
  pdb.gimp_image_undo_group_start( inImage )
  # Add a layer mask with the value channel (inverted)
  valueImage = pdb.plug_in_decompose( inImage, inDrawable, "HSV", True )[0]
  valueLayer = pdb.gimp_layer_new_from_drawable( valueImage.layers[2], inImage )
  inImage.add_layer( valueLayer, -1 )
  pdb.gimp_displays_flush()    
  pdb.gimp_image_delete( valueImage )
  #
  pdb.gimp_invert( valueLayer )
  pdb.gimp_layer_add_mask( valueLayer, valueLayer.create_mask( ADD_COPY_MASK ))
 # Fill the layer and switch to softlight mode
  gimp.set_background( brightness, brightness, brightness )
  pdb.gimp_drawable_fill( valueLayer, BACKGROUND_FILL )
  pdb.gimp_layer_set_mode( valueLayer, SOFTLIGHT_MODE )
  pdb.gimp_layer_set_name( valueLayer, _("Enlight dark tones") )
  #
  pdb.gimp_displays_flush()
  pdb.gimp_image_undo_group_end ( inImage )

# Register
#
register(
  "Darkenlight",
  Photolab_darkenlight_description,
  Photolab_darkenlight_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Enlight the dark tones"),
  "*",
  [
    (PF_IMAGE, "inImage", "Input image", None),
    (PF_DRAWABLE, "inLayer", "Input drawable", None),
    (PF_SPINNER, "brightness", _("Brightness"), 255, (0,255,10) )
  ],
  [],
  python_fu_darkenlight,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
