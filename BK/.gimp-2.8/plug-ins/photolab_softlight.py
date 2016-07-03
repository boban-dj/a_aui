#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Softlight
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.1
# - ported to GIMP-2.6
# - added valid images "*"
# Version 2.0
# - ported to GIMP-2.4
# - use gettext 
# Version 1.0
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *

# i18n
#
import gettext
locale_directory = gimp.locale_directory #return a wrong path until Gimp-2.4.2 under Windows see bug 502506
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_softlight_description = _("Add a layer in Softlight mode. If a selection exists a layer mask is added")
Photolab_sofrlight_help = _("Python-fu Photolab Soft light.")+" "+Photolab_softlight_description

# Main Program
#
def python_fu_softlight( 
  inImage,
  inDrawable,
  brightness ): 
  #
  width= inDrawable.width
  height= inDrawable.height
  brightness= brightness +127 #Values from 0 to 255
  #
  softlightlayer= gimp.Layer(inImage, _("softlight"), width, height, RGBA_IMAGE, 100, SOFTLIGHT_MODE)
  inImage.add_layer(softlightlayer, -1)
  gimp.set_background( brightness, brightness, brightness )
  pdb.gimp_drawable_fill( softlightlayer, BACKGROUND_FILL )
  if pdb.gimp_selection_is_empty(inImage) == 0:
    #softlightlayer.create_mask(ADD_SELECTION_MASK)
    pdb.gimp_layer_add_mask( softlightlayer, softlightlayer.create_mask( ADD_SELECTION_MASK ))
  pdb.gimp_displays_flush()

register(
  "Softlight",
  Photolab_softlight_description,
  Photolab_sofrlight_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Softlight Layer"),
  "*",
  [
    (PF_IMAGE, "inImage", "Input image", None),
    (PF_DRAWABLE, "inLayer", "Input drawable", None),
    (PF_SPINNER, "brightness", _("Brightness"), 0, (-127,128,10) )
  ],
  [],
  python_fu_softlight,
  menu="<Image>/Filters"+"/"+_("Photolab"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
