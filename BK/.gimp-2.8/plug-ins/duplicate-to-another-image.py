#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plug-in:      Duplicate to another Image...
# Version:      1.1
# Date:         19.04.2013
# Copyright:    Dmitry Dubyaga <dmitry.dubyaga@gmail.com>      
# Tested with:  GIMP 2.8
# ----------------------------------

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gimpfu import *

def show_message(m_id):
    messages = []
    messages.append("Can only be called on a layer, not on a mask.")
    messages.append("The layer or layer group is not selected.")
    pdb.gimp_message(messages[m_id])
    return

def align_item_to_center(image, item):
    offset_x = (image.width - item.width) / 2
    offset_y = (image.height - item.height) / 2
    return item.set_offsets(offset_x, offset_y)

def python_fu_duplicate_to_another_image(image, drawable, item_name, destination, dest_image, item_position = 0, keep_level = 1, remove_original = False):
    gimp.context_push()
    image.undo_group_start()

    pdb.gimp_message_get_handler(ERROR_CONSOLE)
    
    if pdb.gimp_item_is_layer_mask(drawable):
        show_message(0)
        image.undo_group_end()
        gimp.context_pop()
        return
    if not pdb.gimp_item_is_layer(drawable):
        show_message(1)
        image.undo_group_end()
        gimp.context_pop()
        return

    if destination == "another_image":
        item_parent = pdb.gimp_item_get_parent(drawable)
        if keep_level == 2:
            item_level_from_top = pdb.gimp_image_get_item_position(image, drawable)
            number_of_layers_original = pdb.gimp_image_get_layers(image)[0]
            number_of_layers_destination = pdb.gimp_image_get_layers(dest_image)[0]
            item_level_from_bottom = number_of_layers_original - item_level_from_top
            item_level = number_of_layers_destination - item_level_from_bottom + 1
        elif keep_level == 1:
            item_level_from_top = pdb.gimp_image_get_item_position(image, drawable)
            item_level = item_level_from_top
        else:
            item_level = 0
        item_copy = pdb.gimp_layer_new_from_drawable(drawable, dest_image)
        pdb.gimp_image_insert_layer(dest_image, item_copy, item_parent, item_level)
    else:
        image_create = pdb.gimp_image_new(image.width, image.height, 0)
        display = pdb.gimp_display_new(image_create)
        item_copy = pdb.gimp_layer_new_from_drawable(drawable, image_create)
        pdb.gimp_image_insert_layer(image_create, item_copy, None, 0)

    if item_name == "":
        item_copy.name = drawable.name
    else:
        item_copy.name = item_name
    if item_position == 1:
        align_item_to_center(dest_image, item_copy)
    if item_position == 2:
        item_copy.set_offsets(0, 0)
    if remove_original:
        pdb.gimp_image_remove_layer(image, drawable)
    pdb.gimp_drawable_update(item_copy, 0, 0, item_copy.width, item_copy.height)

    image.undo_group_end()
    gimp.displays_flush()
    gimp.context_pop()
    return

register (
    "python-fu-duplicate-to",
    "Duplicate to another Image...\nVersion 1.1",
    "Duplicate to another Image...\nVersion 1.1",
    "Dmirty Dubyaga",
    "Dmitry Dubyaga <dmitry.dubyaga@gmail.com>",
    "19.04.2013",
    "Duplicate to another Image...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),
        (PF_STRING, "item_name", "Duplicate name:", ""),
        (PF_RADIO, "destination", "Destination:", "another_image", 
            (
                ("New image", "new_image"),
                ("Another open image", "another_image")
            )
        ),
        (PF_IMAGE, "dest_image", "Image:", None),
        (PF_OPTION, "item_position", "Position:", 0, ("In the same position", "Image center", "Coordinate origin")),
        (PF_OPTION, "keep_level", "Keep level:", 1, ("None", "From the top", "From the bottom")),
        (PF_TOGGLE, "remove_original", "Remove original:", False)
    ],
    [],
    python_fu_duplicate_to_another_image, menu = "<Image>/Layer/"
    )
register (
    "python-fu-duplicate-to-another-image",
    "Duplicate to another Image...\nVersion 1.1",
    "Duplicate to another Image...\nVersion 1.1",
    "Dmirty Dubyaga",
    "Dmitry Dubyaga <dmitry.dubyaga@gmail.com>",
    "19.04.2013",
    "Duplicate to another Image...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),
        (PF_STRING, "item_name", "Duplicate name:", ""),
        (PF_RADIO, "destination", "Destination:", "another_image",
            (
                ("New image", "new_image"),
                ("Another open image", "another_image")
            )
        ),
        (PF_IMAGE, "dest_image", "Image:", None),
        (PF_OPTION, "item_position", "Position:", 0, ("In the same position", "Image center", "Coordinate origin")),
        (PF_OPTION, "keep_level", "Keep level:", 1, ("None", "From the top", "From the bottom")),
        (PF_TOGGLE, "remove_original", "Remove original:", False)
    ],
    [],
    python_fu_duplicate_to_another_image, menu = "<Layers>/"
    )

main()
