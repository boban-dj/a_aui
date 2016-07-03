#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Plug-in:      Place Layer into Selection
# Version:      1.0
# Date:         17.07.2013
# Copyright:    Dmitry Dubyaga <dmitry.dubyaga@gmail.com>
# Website:      some-gimp-plugins.com
# Tested with:  GIMP 2.8


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from gimpfu import *

def python_fu_place_layer_into_selection(image, drawable, scaling_type, keep_ratio = False, addition = 0, interpolation = 2, aling_to_selection_center = True, postprocessing = 1):
    gimp.context_push()
    image.undo_group_start()

    pdb.gimp_message_get_handler(ERROR_CONSOLE)

    if pdb.gimp_item_is_group(drawable):
        pdb.gimp_message("Layer Groups is not supported yet. Coming in the next version.")
        image.undo_group_end()
        gimp.context_pop()
        return

    if not pdb.gimp_item_is_layer(drawable):
        pdb.gimp_message("The layer or layer group is not selected.")
        image.undo_group_end()
        gimp.context_pop()
        return

    if pdb.gimp_selection_is_empty(image):
        pdb.gimp_message("The selected area is missing.")
        image.undo_group_end()
        gimp.context_pop()
        return

    pdb.gimp_context_set_interpolation(interpolation)

    selection_bounds = pdb.gimp_selection_bounds(image)
    selection_width = selection_bounds[3] - selection_bounds[1]
    selection_height = selection_bounds[4] - selection_bounds[2]
    ratio_selection = selection_width / float(selection_height)

    ratio_drawable = drawable.width / float(drawable.height)

    if scaling_type == "fit_inside":
        if ratio_selection > ratio_drawable:
            layer_height = selection_height + selection_height * addition / 100
            layer_width = layer_height * ratio_drawable
        else:
            layer_width = selection_width + selection_width * addition / 100
            layer_height = layer_width / ratio_drawable
    if scaling_type == "fit_outside":
        if ratio_selection > ratio_drawable:
            layer_width = selection_width + selection_width * addition / 100
            layer_height = layer_width / ratio_drawable
        else:
            layer_height = selection_height + selection_height * addition / 100
            layer_width = layer_height * ratio_drawable
    if scaling_type == "scale_to_width":
        layer_width = selection_width + selection_width * addition / 100
        if keep_ratio:
            layer_height = layer_width / ratio_drawable
        else:
            layer_height = drawable.height
    if scaling_type == "scale_to_height":
        layer_height = selection_height + selection_height * addition / 100
        if keep_ratio:
            layer_width = layer_height * ratio_drawable
        else:
            layer_width = drawable.width
    if scaling_type == "scale_to_width_and_height":
        if keep_ratio:
            if ratio_selection > ratio_drawable:
                layer_width = selection_width + selection_width * addition / 100
                layer_height = layer_width / ratio_drawable
            else:
                layer_height = selection_height + selection_height * addition / 100
                layer_width = layer_height * ratio_drawable
        else:
            layer_width = selection_width + selection_width * addition / 100
            layer_height = selection_height + selection_height * addition / 100
    if scaling_type == "without_scaling":
        layer_width = drawable.width
        layer_height = drawable.height

    pdb.gimp_layer_scale(drawable, layer_width, layer_height, TRUE)
    layer_offset_x, layer_offset_y = pdb.gimp_drawable_offsets(drawable)

    if aling_to_selection_center:
        selection_center_x = selection_bounds[1] + selection_width / 2
        selection_center_y = selection_bounds[2] + selection_height / 2
        layer_offset_x = selection_center_x - drawable.width / 2
        layer_offset_y = selection_center_y - drawable.height / 2
        drawable.set_offsets(layer_offset_x, layer_offset_y)
    else:
        pass

    if postprocessing == 1:
        created_mask = pdb.gimp_layer_create_mask(drawable, ADD_SELECTION_MASK)
        pdb.gimp_layer_add_mask(drawable, created_mask)
    elif postprocessing == 2:
        pdb.gimp_layer_add_alpha(drawable)
        created_mask = pdb.gimp_layer_create_mask(drawable, ADD_SELECTION_MASK)
        pdb.gimp_layer_add_mask(drawable, created_mask)
        pdb.gimp_layer_remove_mask(drawable, MASK_APPLY)
        pdb.gimp_layer_resize(drawable, selection_width, selection_height, layer_offset_x - selection_bounds[1], layer_offset_y - selection_bounds[2])
    else:
        pass

    #pdb.gimp_selection_none(image)

    gimp.displays_flush()
    image.undo_group_end()
    gimp.context_pop()
    return

register (
    "python-fu-place-layer-into-selection",
    "Place Layer into Selection\nVersion 1.0",
    "Place Layer into Selection\nVersion 1.0",
    "Dmirty Dubyaga",
    "Dmitry Dubyaga <dmitry.dubyaga@gmail.com>",
    "17.07.2013",
    "Place Layer into Selection...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),
        (PF_RADIO, "scaling_type", "How to place:", "fit_outside",
            (
                ("Fit Inside", "fit_inside"),
                ("Fit Outside", "fit_outside"),
                ("Scale to Width", "scale_to_width"),
                ("Scale to Height", "scale_to_height"),
                ("Scale to Width and Height", "scale_to_width_and_height"),
                ("Without Scaling", "without_scaling")
            )
        ),
        (PF_TOGGLE, "keep_ratio", "Keep aspect ratio:", False),
        (PF_SPINNER, "addition", "Addition (%):", 0, (-99, 100, 1)),
        (PF_OPTION, "interpolation", "Interpolation:", 2, ("None", "Linear", "Cubic", "Sinc (Lanczos3)")),
        (PF_TOGGLE, "aling_to_selection_center", "Align layer\nto selection center:", True),
        (PF_OPTION, "postprocessing", "Postprocessing:", 1, ("None", "Create Layer Mask", "Crop to Selection")),
    ],
    [],
    python_fu_place_layer_into_selection, menu="<Image>/Layer/"
    )

main()