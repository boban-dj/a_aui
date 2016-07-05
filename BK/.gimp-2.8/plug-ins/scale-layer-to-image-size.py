#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plug-in:      Scale Layer to Image Size
# Version:      1.3
# Date:         01.06.2012
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
    messages.append("The layer or layer group is not selected.")
    pdb.gimp_message(messages[m_id])
    return

def find_layers_in_group(group, elements):
    num_children, child_ids = pdb.gimp_item_get_children(group)
    for id in child_ids:
        child = gimp.Item.from_id(id)
        if pdb.gimp_item_is_group(child):
            find_layers_in_group(child, elements)
        else:
            elements.append(child)
    return elements

def align_layer_to_center(image, layer):
    offset_x = (image.width - layer.width) / 2
    offset_y = (image.height - layer.height) / 2
    return layer.set_offsets(offset_x, offset_y)

def python_fu_scale_layer_to_image_size(image, drawable, scaling_type, scale_separately = True, keep_aspect = False, addition = 0, interpolation = 2, align_method = 1, crop = True):
    gimp.context_push()
    image.undo_group_start()

    pdb.gimp_message_get_handler(ERROR_CONSOLE)

    if not pdb.gimp_item_is_layer(drawable):
        show_message(0)
        image.undo_group_end()
        gimp.context_pop()
        return

    pdb.gimp_context_set_interpolation(interpolation)
    aspect_image = image.width / float(image.height)

    if pdb.gimp_item_is_group(drawable) and scale_separately:
        layers_list = find_layers_in_group(drawable, elements = [])
        for element in layers_list:
            aspect_layer = element.width / float(element.height)
            if scaling_type == "fit_inside":
                if aspect_image > aspect_layer:
                    layer_height = image.height + image.height * addition / 100
                    layer_width = layer_height * aspect_layer
                else:
                    layer_width = image.width + image.width * addition / 100
                    layer_height = layer_width / aspect_layer            
            if scaling_type == "fit_outside":
                if aspect_image > aspect_layer:
                    layer_width = image.width + image.width * addition / 100
                    layer_height = layer_width / aspect_layer
                else:
                    layer_height = image.height + image.height * addition / 100
                    layer_width = layer_height * aspect_layer
            if scaling_type == "scale_to_width":
                layer_width = image.width + image.width * addition / 100
                if keep_aspect == True:
                    layer_height = layer_width / aspect_layer
                else:
                    layer_height = element.height
            if scaling_type == "scale_to_height":
                layer_height = image.height + image.height * addition / 100
                if keep_aspect == True:
                    layer_width = layer_height * aspect_layer
                else:
                    layer_width = element.width
            if scaling_type == "scale_to_width_and_height":
                if keep_aspect == True:
                    if aspect_image > aspect_layer:
                        layer_width = image.width + image.width * addition / 100
                        layer_height = layer_width / aspect_layer
                    else:
                        layer_height = image.height + image.height * addition / 100
                        layer_width = layer_height * aspect_layer
                else:
                    layer_width = image.width + image.width * addition / 100
                    layer_height = image.height + image.height * addition / 100
            if scaling_type == "scale_none":
                layer_width = element.width
                layer_height = element.height

            pdb.gimp_layer_scale(element, layer_width, layer_height, TRUE)

            if align_method == 1:
                align_layer_to_center(image, element)

        if align_method == 0:
            align_layer_to_center(image, drawable)

        if crop:
            if drawable.width > image.width or drawable.height > image.height:
                pdb.gimp_layer_resize_to_image_size(drawable)
                pdb.plug_in_autocrop_layer(image, drawable)
        
        gimp.displays_flush()
        image.undo_group_end()
        gimp.context_pop()
        return

    aspect_drawable = drawable.width / float(drawable.height)

    if scaling_type == "fit_inside":
        if aspect_image > aspect_drawable:
            layer_height = image.height + image.height * addition / 100
            layer_width = layer_height * aspect_drawable
        else:
            layer_width = image.width + image.width * addition / 100
            layer_height = layer_width / aspect_drawable                
    if scaling_type == "fit_outside":
        if aspect_image > aspect_drawable:
            layer_width = image.width + image.width * addition / 100
            layer_height = layer_width / aspect_drawable
        else:
            layer_height = image.height + image.height * addition / 100
            layer_width = layer_height * aspect_drawable
    if scaling_type == "scale_to_width":
        layer_width = image.width + image.width * addition / 100
        if keep_aspect == True:
            layer_height = layer_width / aspect_drawable
        else:
            layer_height = drawable.height
    if scaling_type == "scale_to_height":
        layer_height = image.height + image.height * addition / 100
        if keep_aspect == True:
            layer_width = layer_height * aspect_drawable
        else:
            layer_width = drawable.width
    if scaling_type == "scale_to_width_and_height":
        if keep_aspect == True:
            if aspect_image > aspect_drawable:
                layer_width = image.width + image.width * addition / 100
                layer_height = layer_width / aspect_drawable
            else:
                layer_height = image.height + image.height * addition / 100
                layer_width = layer_height * aspect_drawable
        else:
            layer_width = image.width + image.width * addition / 100
            layer_height = image.height + image.height * addition / 100
    if scaling_type == "scale_none":
        layer_width = drawable.width
        layer_height = drawable.height

    pdb.gimp_layer_scale(drawable, layer_width, layer_height, TRUE)

    if align_method == 0 or align_method == 1:
        align_layer_to_center(image, drawable)

    if crop:
        if drawable.width > image.width or drawable.height > image.height:
            pdb.gimp_layer_resize_to_image_size(drawable)
            pdb.plug_in_autocrop_layer(image, drawable)  

    gimp.displays_flush()
    image.undo_group_end()
    gimp.context_pop()    
    return

register (
    "python-fu-scale-layer-to-image-size",
    "Scale Layer to Image Size\nVersion 1.3\nScaling a group of layers is also supported.",
    "Scale Layer to Image Size\nVersion 1.3\nScaling a group of layers is also supported.",
    "Dmirty Dubyaga",
    "Dmitry Dubyaga <dmitry.dubyaga@gmail.com>",
    "01.06.2012",
    "Scale Layer to Image Size...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),
        (PF_RADIO, "scaling_type", "Scaling type:", "fit_inside", 
            (
                ("Fit inside", "fit_inside"),
                ("Fit outside", "fit_outside"),
                ("Scale to width", "scale_to_width"), 
                ("Scale to height", "scale_to_height"),
                ("Scale to width and height", "scale_to_width_and_height"),
                ("None", "scale_none")
            )
        ),
        (PF_TOGGLE, "scale_separately", "Scale separately each layer\nin the selected group:", True),
        (PF_TOGGLE, "keep_aspect", "Keep aspect ratio:", False),
        (PF_SPINNER, "addition", "Addition (%):", 0, (-99, 100, 1)),
        (PF_OPTION, "interpolation", "Interpolation:", 2, ("None", "Linear", "Cubic", "Sinc (Lanczos3)")),
        (PF_OPTION, "align_method", "Align to image center:", 1, ("Group as a whole", "Each layer separately", "None")),
        (PF_TOGGLE, "crop", "Crop to image size:", True)
    ],
    [],
    python_fu_scale_layer_to_image_size, menu="<Image>/Layer/"
    )

main()
