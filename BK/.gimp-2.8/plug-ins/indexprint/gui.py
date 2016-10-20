#!/usr/bin/python2
# -*- coding: UTF-8 -*-

'''
Copyright

Elmar Sullock Enzlin at moroquendo@gmail.com
(C) 2009, ..., 2012 Utrecht, The Netherlands

This plugin was tested with Gimp V2.6/2.8
On PC configurations:   -windows XP 32bits
                        -Linux Ubuntu 12.04 LTS 32bits


software_license
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
'''

'''
Version History: see indexprint.py
'''

import math
try:
    import pygtk
    pygtk.require("2.0")
except ImportError,  e :
    pass
#    self.on_error(_("Libraries not found!"), _("The pygtk library not found.\nCheck your installation please!\n"+str(e)))

try:
    import gtk, gtk.glade           #after adding gtk.glade translations are working
except ImportError,  e :
    sys.exit(1)
#    self.on_error(_("Libraries not found!"), _("The Gtk or Glade library not found.\nCheck your installation please!\n"+str(e)))

import locale, gettext

import glib
import os, ConfigParser
from gimpfu import *

import re

from indexprint import GenerateIndexprint

##try:
##    import pyexiv2
##    pyexiv2_loaded = True
##except ImportError, e :
##    self.on_error(_("PyExiv2 not installed!"), _("Disabling exif functions.\n"+str(e)))
##    pyexiv2_loaded = False

# -- self.on_error werkt nog niet nog niet gedefinieerd
# -- attribute on_error bestaat niet

# *****************************************************************************
# ********************** initialize internationalisation **********************
# *****************************************************************************
APP = "indexprint"              #name of the translation file <---!!!!!!!
# DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                   'locale')     #locale dir of gimp
DIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   APP), 'locale')

locale.setlocale(locale.LC_ALL, '')            #reset all

gettext.bindtextdomain(APP,DIR)
gettext.textdomain(APP)

##lang = gettext.translation(APP, DIR) 
##
##_ = lang.gettext

gettext.install(APP, DIR)





#gettext.install(APP, DIR, unicode=True)
gtk.glade.bindtextdomain(APP,DIR)
gtk.glade.textdomain(APP)


# Make fully qualified path so pygtk finds glade file.
# Get the glade file from same directory as this file (must be together)
GUI_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'IndexPrint.glade')


# *****************************************************************************
# *************************** build the window ********************************
# *****************************************************************************
class ContactsheetApp():   # new-style class

    def __init__(self):
        if not os.path.exists(GUI_FILENAME):
            Log(_("Cannot find the glade file: ") + GUI_FILENAME)
            self.on_error(_("No dialog file found!"),
                          _("Sorry, the dialog file IndexPrint.glade was not found.\nCheck your installation please!"))
            return
    
        # Note: use self for all variables accessed across class methods,
        # but not passed into a method, eg in a callback.
        # gtk.glade.textdomain(GUI_FILENAME)
        builder = gtk.Builder()
        builder.set_translation_domain(APP)
        builder.add_from_file(GUI_FILENAME)

        # Connect some signals defined in the glade file.
        # See callbacks below, named same as in glade file.
        builder.connect_signals(self)
        self.dialog     = builder.get_object("dialog1")
        self.helpMessage = builder.get_object("messagedialog1")
        self.aboutDialog = builder.get_object("aboutdialog1")
        self.buttonOK   = builder.get_object("button_ok")

        # --------------- read&save tab -----------------------
        # images to read section
        self.jpg = builder.get_object("checkbutton_jpg")
        self.png = builder.get_object("checkbutton_png")
        self.tif = builder.get_object("checkbutton_tif")
        self.xcf = builder.get_object("checkbutton_xcf")
        self.pcx = builder.get_object("checkbutton_pcx")
        self.bmp = builder.get_object("checkbutton_bmp")
        self.gif = builder.get_object("checkbutton_gif")
        self.eps = builder.get_object("checkbutton_eps")
        self.raw = builder.get_object("checkbutton_raw")
        self.wdp = builder.get_object("checkbutton_wdp")
        self.svg = builder.get_object("checkbutton_svg")
        self.psd = builder.get_object("checkbutton_psd")
        self.select_part_of_filename =  builder.get_object("entry_select_part_of_filename")
        self.open_from_location     = builder.get_object("filechooserbutton_open_from_location")
        self.include_subdirs        = builder.get_object("checkbutton_include_subdirs")
        
        # images to save section
        self.save_to_location = builder.get_object("filechooserbutton_save_to_location")
        self.filename       = builder.get_object("entry_filename")
        self.extension_jpg  = builder.get_object("radiobutton_jpg")
        self.extension_png  = builder.get_object("radiobutton_png")
        
        # --------------- page options tab ---------------
        self.paper_size     = builder.get_object("combobox_sheet_size")
        self.paper_height   = builder.get_object("spinbutton_height")
        self.paper_width    = builder.get_object("spinbutton_width")
        self.paper_units    = builder.get_object("combobox_units_customsize")
        
        self.page_orientation_portrait = builder.get_object("radiobutton_portrait")
        self.page_orientation_landscape = builder.get_object("radiobutton_landscape")
        self.page_resolution        = builder.get_object("spinbutton_resolution")
        #--background
        self.page_with_background = builder.get_object("checkbutton_with_background")
        self.page_rb_bg_solidcolor = builder.get_object("radiobutton_background_solidcolor")
        self.page_rb_bg_image       = builder.get_object("radiobutton_background_image")
        self.page_background_color = builder.get_object("colorbutton_background_color")
        self.page_background_image = builder.get_object("filechooserbutton_background_image")
        self.page_background_image_opacity = builder.get_object("spinbutton_opacity_background_image")
        #--header
        self.page_with_header   = builder.get_object("checkbutton_include_header") 
        self.page_header        = builder.get_object("entry_page_header") #text
        self.page_header_font   = builder.get_object("fontbutton_header") #font and size
        self.page_header_color  = builder.get_object("colorbutton_header") #color
        # ---pagenumber
        self.with_pagenumber    = builder.get_object("checkbutton_include_pagenumber") #nummer
        self.pagenumber         = builder.get_object("spinbutton_pagenumber") #nummer
        self.pagenumber_font    = builder.get_object("fontbutton_pagenumber") #font and size
        self.pagenumber_color   = builder.get_object("colorbutton_pagenumber") #color
        self.total_pages        = builder.get_object("checkbutton_total_pages") #y/n
        # ---pagemargins
        self.pagemargin_top     = builder.get_object("spinbutton_pagemargin_top")
        self.pagemargin_bottom  = builder.get_object("spinbutton_pagemargin_bottom")
        self.pagemargin_left    = builder.get_object("spinbutton_pagemargin_left")
        self.pagemargin_right   = builder.get_object("spinbutton_pagemargin_right")
        self.pagemargin_units   = builder.get_object("combobox_units_pagemargin")
        self.temp   = builder.get_object("combobox_units_pagemargin")
        self.pagemargin_old_units = self.temp.get_active_text()


        # ------------------- image options tab -------------------------
        self.numofrows          = builder.get_object("spinbutton_number_of_rows")
        self.numofcols          = builder.get_object("spinbutton_number_of_columns")
        self.image_whiteborder  = builder.get_object("spinbutton_image_whiteborder")
        self.image_whiteborder_units = builder.get_object("combobox_image_whiteborder_units")
        self.include_imagename  = builder.get_object("checkbutton_include_imagename")
        self.imagename_with_extension = builder.get_object("checkbutton_with_extension")
        self.image_aspectratio  = builder.get_object("combobox_image_size_or_ratio")
        self.image_rotate       = builder.get_object("checkbutton_rotate_images")

        self.caption_font       = builder.get_object("fontbutton_font_caption")
        self.caption_font_color = builder.get_object("colorbutton_font_caption_color")
        
        # exif information
        self.include_exif               = builder.get_object("checkbutton_include_exif")
        self.include_exif_datetime      = builder.get_object("checkbutton_exif_datetime")
        self.include_exif_shutterspeed  = builder.get_object("checkbutton_exif_shutterspeed")
        self.include_exif_ISO           = builder.get_object("checkbutton_exif_ISO")
        self.include_exif_focal         = builder.get_object("checkbutton_exif_focal")
        self.include_exif_lightsource   = builder.get_object("checkbutton_exif_lightSource")
        self.include_exif_diafragm      = builder.get_object("checkbutton_exif_diafragm")
        

        # ------------------- other tab ----------------------------------
        self.include_list_imagenames = builder.get_object("checkbutton_include_list_imagenames")
        self.direct_printing        = builder.get_object("checkbutton_direct_printing")

        self.images_sort_alphanumeric = builder.get_object("checkbutton_images_sorted")
        self.exif_sort              = builder.get_object("checkbutton_sorting_exif")
        self.exif_sort_datetime     = builder.get_object("checkbutton_exif_sort_datetime")
        self.exif_sort_someexif     = builder.get_object("checkbutton_exif_sort_someexif")


        try:
            import pyexiv2
            self.pyexiv2_loaded = True
        except ImportError, e :
            #self.on_error(_("PyExiv2 not installed!"), _("Disabling exif functions.\n"+str(e)))
            self.pyexiv2_loaded = False

        # ---- if pyexiv2 not installed disable exif options ------------
        if self.pyexiv2_loaded == False:
            self.include_exif.set_sensitive(False)
            self.include_exif_datetime.set_sensitive(False)
            self.include_exif_shutterspeed.set_sensitive(False)
            self.include_exif_ISO.set_sensitive(False)
            self.exif_sort.set_sensitive(False)
            self.exif_sort_datetime.set_sensitive(False)
            self.exif_sort_someexif.set_sensitive(False)
        else:
            self.include_exif.set_sensitive(True)
            self.include_exif_datetime.set_sensitive(True)
            self.include_exif_shutterspeed.set_sensitive(True)
            self.include_exif_ISO.set_sensitive(True)
            self.exif_sort.set_sensitive(True)
            self.exif_sort_datetime.set_sensitive(True)
            self.exif_sort_someexif.set_sensitive(True)

        # -- to do: also when ghostscript is not installed


        # -------------- Load config file if exist ---------------------
        #self.config_dir = gimp.directory
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "config/indexprint.cfg")
        self.load_config('DEFAULT')
        self.dialog.show()


# *****************************************************************************
    def main(self):
        gtk.main()  # event loop


# *****************************************************************************
# ****************************** Callback's ***********************************
# *****************************************************************************
    '''
    ************** Callback functions, signals emitted by Glade *********
    ** Callbacks are as far as possible grouped per notebook tab
    '''
# --------------- on the read&save tab -----------------------

# ** no callbacks on this tab


# --------------- on the page options tab --------------------
# *****************************************************************************
    def on_combobox_sheet_size_changed(self, widget):
        '''
        gray out custom size and units when custom not selected
        not working correct, should grey out directly if not custom
        '''
        if self.paper_size.get_active_text() == "custom":
            self.paper_height.set_sensitive(True)
            self.paper_width.set_sensitive(True)
            self.paper_units.set_sensitive(True)
            self.page_orientation_portrait.set_sensitive(False)
            self.page_orientation_landscape.set_sensitive(False)
        else:
            self.paper_height.set_sensitive(False)
            self.paper_width.set_sensitive(False)
            self.paper_units.set_sensitive(False)
            self.page_orientation_portrait.set_sensitive(True)
            self.page_orientation_landscape.set_sensitive(True)


# *****************************************************************************
    def on_combobox_units_customsize_changed(self, widget):
        '''
        change dynamicly adjustment of height and width.
        mm: min 100 max 1000 step 0,1
        inch: min 4 max 25 step 0,01
        '''
        # save value
        height = self.paper_height.get_value()
        width  = self.paper_width.get_value()
        if self.paper_units.get_active_text() == "mm":      # mm
            # set range
            self.paper_height.set_range(100,1000)
            self.paper_width.set_range(100,1000)
            # restore converted value from inches to mm
            self.paper_height.set_value(self.inch2mm(height))
            self.paper_width.set_value(self.inch2mm(width))
        else:                                               # inch
            # set range
            self.paper_height.set_range(4,25)
            self.paper_width.set_range(4,25)
            # restore converted value from mm to inches
            self.paper_height.set_value(self.mm2inch(height))
            self.paper_width.set_value(self.mm2inch(width))

# *****************************************************************************
    def on_checkbutton_with_background_toggled(self, widget):
        '''
        gray out frame background when 'background' not selected
        '''
        if self.page_with_background.get_active() == True:
            if self.page_rb_bg_solidcolor.get_active() == True:
                self.page_background_color.set_sensitive(True)
                self.page_background_image.set_sensitive(False)
                self.page_background_image_opacity.set_sensitive(False)
            else:
                self.page_background_color.set_sensitive(False)
                self.page_background_image.set_sensitive(True)
                self.page_background_image_opacity.set_sensitive(True)
            self.page_rb_bg_solidcolor.set_sensitive(True)
            self.page_rb_bg_image.set_sensitive(True)
        else:
            self.page_rb_bg_solidcolor.set_sensitive(False)
            self.page_rb_bg_image.set_sensitive(False)
            self.page_background_image.set_sensitive(False)
            self.page_background_image_opacity.set_sensitive(False)
            self.page_background_color.set_sensitive(False)

# *****************************************************************************
    def on_radiobutton_background_solidcolor_toggled(self,widget):
        if self.page_rb_bg_solidcolor.get_active() == True:
            self.page_background_image.set_sensitive(False)
            self.page_background_image_opacity.set_sensitive(False)
            self.page_background_color.set_sensitive(True)
        else:
            self.page_background_image.set_sensitive(True)
            self.page_background_image_opacity.set_sensitive(True)
            self.page_background_color.set_sensitive(False)

# *****************************************************************************
    def on_checkbutton_include_header_toggled(self, widget):
        '''
        gray out frame header when 'header' not selected
        '''
        if self.page_with_header.get_active() == True:
            self.page_header.set_sensitive(True)
            self.page_header_font.set_sensitive(True)
            self.page_header_color.set_sensitive(True)
        else:
            self.page_header.set_sensitive(False)
            self.page_header_font.set_sensitive(False)
            self.page_header_color.set_sensitive(False)

# *****************************************************************************
    def on_checkbutton_include_pagenumber_toggled(self, widget):
        '''
        gray out frame pagenumber when 'pagenumber' not selected
        '''
        if self.with_pagenumber.get_active() == True:
            self.pagenumber.set_sensitive(True)
            self.pagenumber_font.set_sensitive(True)
            self.pagenumber_color.set_sensitive(True)
            self.total_pages.set_sensitive(True)
            
        else:
            self.pagenumber.set_sensitive(False)
            self.pagenumber_font.set_sensitive(False)
            self.pagenumber_color.set_sensitive(False)
            self.total_pages.set_sensitive(False)


# *****************************************************************************
    def on_combobox_units_pagemargin_changed(self, widget):
        '''
        change dynamicly adjustment of pagemargins.
        mm: min 0 max 50 step 0,1
        inch: min 0 max 2 step 0,01
        pt: min 0 max 150 step 1
        %: min 0 max 10 step 0,1     (% of the width of the papersize)

        on_combobox_units_pagemargin_changed(self, widget, old_units):
        '''
        # Save values for converting
        top     = self.pagemargin_top.get_value()
        bottom  = self.pagemargin_bottom.get_value()
        left    = self.pagemargin_left.get_value()
        right   = self.pagemargin_right.get_value()
        new_units = self.pagemargin_units.get_active_text()
        old_units = self.pagemargin_old_units
        
        # ---- define ranges ------
        if self.pagemargin_units.get_active_text() == "mm":
            range_min = 0
            range_max = 50
            digits = 1
            step = 0.1
            pagestep = 10
        elif self.pagemargin_units.get_active_text() == "inch":
            range_min = 0
            range_max = 2
            digits = 2
            step = 0.01
            pagestep = 0.05
        elif self.pagemargin_units.get_active_text() == "pt":
            range_min = 0
            range_max = 150
            digits = 0
            step = 1
            pagestep = 50
        else:
            range_min = 0               # % 
            range_max = 10
            digits = 1
            step = 0.1
            pagestep = 1

        # ----- apply ranges ------
        self.pagemargin_top.set_range(range_min, range_max)
        self.pagemargin_top.set_digits(digits)
        self.pagemargin_top.set_increments(step,pagestep)

        self.pagemargin_bottom.set_range(range_min, range_max)
        self.pagemargin_bottom.set_digits(digits)
        self.pagemargin_bottom.set_increments(step,pagestep)

        self.pagemargin_left.set_range(range_min, range_max)
        self.pagemargin_left.set_digits(digits)
        self.pagemargin_left.set_increments(step,pagestep)

        self.pagemargin_right.set_range(range_min, range_max)
        self.pagemargin_right.set_digits(digits)
        self.pagemargin_right.set_increments(step,pagestep)

        # restore converted value
        if self.pagemargin_units.get_active_text() == old_units:
            #Log('oude en nieuwe units zijn hetzelfde')    # do nothing
            pass
        elif ((old_units == "mm") and (self.pagemargin_units.get_active_text() == "inch")):
            #Log('converteer van mm naar inch')
            self.pagemargin_top.set_value(self.mm2inch(top))
            self.pagemargin_bottom.set_value(self.mm2inch(bottom))
            self.pagemargin_left.set_value(self.mm2inch(left))
            self.pagemargin_right.set_value(self.mm2inch(right))
            
        elif ((old_units == "mm") and (self.pagemargin_units.get_active_text() == "pt")):
            #Log('converteer van mm naar pt')
            self.pagemargin_top.set_value(self.mm2pt(top))
            self.pagemargin_bottom.set_value(self.mm2pt(bottom))
            self.pagemargin_left.set_value(self.mm2pt(left))
            self.pagemargin_right.set_value(self.mm2pt(right))
            
        elif ((old_units == "mm") and (self.pagemargin_units.get_active_text() == "%")):
            #Log('converteer van mm naar %')
            self.pagemargin_top.set_value(self.unit2procent(top,old_units,True))
            self.pagemargin_bottom.set_value(self.unit2procent(bottom,old_units,True))
            self.pagemargin_left.set_value(self.unit2procent(left,old_units,False))
            self.pagemargin_right.set_value(self.unit2procent(right,old_units,False))

        elif (old_units == "inch" and self.pagemargin_units.get_active_text() == "mm"):
            #Log('converteer van inch naar mm')
            self.pagemargin_top.set_value(self.inch2mm(top))
            self.pagemargin_bottom.set_value(self.inch2mm(bottom))
            self.pagemargin_left.set_value(self.inch2mm(left))
            self.pagemargin_right.set_value(self.inch2mm(right))

        elif (old_units == "inch" and self.pagemargin_units.get_active_text() == "pt"):
            #Log('converteer van inch naar pt')
            self.pagemargin_top.set_value(self.inch2pt(top))
            self.pagemargin_bottom.set_value(self.inch2pt(bottom))
            self.pagemargin_left.set_value(self.inch2pt(left))
            self.pagemargin_right.set_value(self.inch2pt(right))
            
        elif (old_units == "inch" and self.pagemargin_units.get_active_text() == "%"):
            self.pagemargin_top.set_value(self.unit2procent(top,old_units,True))
            self.pagemargin_bottom.set_value(self.unit2procent(bottom,old_units,True))
            self.pagemargin_left.set_value(self.unit2procent(left,old_units,False))
            self.pagemargin_right.set_value(self.unit2procent(right,old_units,False))
            #Log('converteer van inch naar %')

        elif (old_units == "pt" and self.pagemargin_units.get_active_text() == "mm"):
            #Log('converteer van pt naar mm')
            self.pagemargin_top.set_value(self.pt2mm(top))
            self.pagemargin_bottom.set_value(self.pt2mm(bottom))
            self.pagemargin_left.set_value(self.pt2mm(left))
            self.pagemargin_right.set_value(self.pt2mm(right))

        elif (old_units == "pt" and self.pagemargin_units.get_active_text() == "inch"):
            #Log('converteer van pt naar inch')
            self.pagemargin_top.set_value(self.pt2inch(top))
            self.pagemargin_bottom.set_value(self.pt2inch(bottom))
            self.pagemargin_left.set_value(self.pt2inch(left))
            self.pagemargin_right.set_value(self.pt2inch(right))

        elif (old_units == "pt" and self.pagemargin_units.get_active_text() == "%"):
            self.pagemargin_top.set_value(self.unit2procent(top,old_units,True))
            self.pagemargin_bottom.set_value(self.unit2procent(bottom,old_units,True))
            self.pagemargin_left.set_value(self.unit2procent(right,old_units,False))
            self.pagemargin_right.set_value(self.unit2procent(left,old_units,False))
            #Log('converteer van pt naar %')

        elif (old_units == "%"):
            self.pagemargin_top.set_value(self.procent2unit(top,new_units,True))
            self.pagemargin_bottom.set_value(self.procent2unit(bottom,new_units,True))
            self.pagemargin_left.set_value(self.procent2unit(left,new_units,False))
            self.pagemargin_right.set_value(self.procent2unit(right,new_units,False))
            #Log('converteer van % naar mm/inch/pt')

        else:
            Log('error in on_combobox_units_pagemargin_changed')

        old_units = self.pagemargin_units.get_active_text()
        self.pagemargin_old_units = old_units






# ------------------- on the image options tab -------------------------

# ------------------- on the other tab ---------------------------------


# *****************************************************************************
    def on_checkbutton_include_imagename_toggled(self, widget):
        '''
        gray out extension when 'include imagename' not selected
        '''
        if self.include_imagename.get_active() == True:
            self.imagename_with_extension.set_sensitive(True)
        else:
            self.imagename_with_extension.set_sensitive(False)
            
# *****************************************************************************
    def on_combobox_image_whiteborder_changed(self, widget):
        '''
        change dynamicly adjustment of whiteborder.
        mm: min 0 max 25 step 0,1
        inch: min 0 max 1 step 0,01 (1" ~ 25mm)
        pt: min 0 max 70 step 1 (1pt=0,375mm: 70pt ~ 25mm)
        %: min 0 max 10 step 0,1
        '''
        # ---- define ranges ------
        if self.image_whiteborder_units.get_active_text() == "mm":
            range_min = 0
            range_max = 25
            digits = 1
            step = 0.1
            pagestep = 2.5
        elif self.image_whiteborder_units.get_active_text() == "inch":
            range_min = 0
            range_max = 1
            digits = 2
            step = 0.01
            pagestep = 0.1
        elif self.image_whiteborder_units.get_active_text() == "pt":
            range_min = 0
            range_max = 70
            digits = 0
            step = 1
            pagestep = 10
        else:
            range_min = 0               # % of the width of the image
            range_max = 10
            digits = 1
            step = 0.1
            pagestep = 1

        # ----- apply ranges ------
        self.image_whiteborder.set_range(range_min, range_max)
        self.image_whiteborder.set_digits(digits)
        self.image_whiteborder.set_increments(step, pagestep)



# *****************************************************************************
    def on_checkbutton_include_exif_toggled(self,widget):
        if self.include_exif.get_active() == True :
            self.include_exif_datetime.set_sensitive(True)
            self.include_exif_ISO.set_sensitive(True)
            self.include_exif_shutterspeed.set_sensitive(True)
            self.include_exif_focal.set_sensitive(True)
            self.include_exif_lightsource.set_sensitive(True)
            self.include_exif_diafragm.set_sensitive(True)
        else:
            self.include_exif_datetime.set_sensitive(False)
            self.include_exif_ISO.set_sensitive(False)
            self.include_exif_shutterspeed.set_sensitive(False)
            self.include_exif_focal.set_sensitive(False)
            self.include_exif_lightsource.set_sensitive(False)
            self.include_exif_diafragm.set_sensitive(False)

# *****************************************************************************
    def on_checkbutton_sorting_exif_toggled(self,widget):
        if self.exif_sort.get_active() == True :
            self.exif_sort_datetime.set_sensitive(True)
            self.exif_sort_someexif.set_sensitive(True)
        else:
            self.exif_sort_datetime.set_sensitive(False)
            self.exif_sort_someexif.set_sensitive(False)


# --------------- main page ---------------
# *****************************************************************************
    def on_dialog1_destroy( self, widget ):
        gtk.main_quit()   

# *****************************************************************************
    def on_dialog1_response(self, widget, responseID):
        '''
        Callback when user clicks on any button in "internal action_area" of dialog.
        In Glade: Add toplevel DialogBox.  
          Set dialog1>Signals>response to "on_dialog1_response" (one of the choices
          and this callback method should be named the same.)
          Add buttons to internal_action area.
          For each button, set General>Response ID property to correspond, eg. 1.
          No need to set button Signals properties.
        This is a dispatcher.
        '''
        if responseID == 1: # same as responseID property set in Glade on Cancel button
            gtk.main_quit()
        elif responseID == 2: # OK button
            # Crux
            self.docontactsheet()
            gtk.main_quit()
        elif responseID == 3: # Help button
            self.helpMessage.show()
        elif responseID == 4: # About button
            self.aboutDialog.show()
        elif responseID == -4:  # on destroy, not set in Glade but sent by pygtk
            pass
        else :
            Log(_("Unhandled response ID for dialog:") + responseID)
            print _("Unhandled response ID for dialog:"), responseID


# *****************************************************************************
    def on_messagedialog1_response(self, widget, responseID):
        if responseID == 1:
            widget.hide()

# *****************************************************************************
    def on_aboutdialog1_response(self, widget, responseID = None):
        widget.hide()


# *****************************************************************************
# ****************************** Utilitys *************************************
# *****************************************************************************
    '''
    ****************  Utilitys
    '''
# *****************************************************************************

# ************* return the integer value of a hexadecimal string s ************
    def hex2dec(self, s):
        return int(s, 16)
    
# ***************** extract font name form the FontButton *********************
    def extract_font_name (self, inFont):
        delim = " "
        delim_idx = inFont.rfind(delim)
        if delim_idx >= 0 :
            return inFont[0: delim_idx]
        else :
            return ""

# ***************** extract font size form the FontButton *********************
    def extract_font_size (self, inFont):
        delim = " "
        delim_idx = inFont.rfind(delim)
        if delim_idx >= 0 :
            return inFont[delim_idx + 1: len(inFont)]
        else :
            return ""

# ****************** extract color definition (r,g,b) *************************
    def extract_color (self, inColor):
        red_hexa = inColor.to_string()[1:3]
        green_hexa = inColor.to_string()[5:7]
        blue_hexa = inColor.to_string()[9:11]
        return (self.hex2dec(red_hexa),
                self.hex2dec(green_hexa),
                self.hex2dec(blue_hexa))

# ************************** convert inches to mm  ****************************
    def inch2mm(self, s):
        return float(s*25.4)

# ************************** convert mm to inches  ****************************
    def mm2inch(self, s):
        return float(s/25.4)

# ************************** convert points to mm  ****************************
    def pt2mm(self, s):
        return float(s*0.375)

# ************************** convert mm to points  ****************************
    def mm2pt(self, s):
        return float(s/0.375)

# ************************** convert points to inches  ************************
    def pt2inch(self, s):
        return float(s*0.375/25.4)

# ************************** convert inches to points  ************************
    def inch2pt(self, s):
        return float(s*25.4/0.375)

# ************************** convert unit to %  ************************
    def unit2procent(self, margin, unit, height):
        '''
        margin contains the value of mm, inch or pt size
        unit contains one of these words: mm, inch or pt
        height is a boolean to decide using width or hight papersize
        sizes noted here are in mm
        '''
        #--get the papersize in mm
        if (self.paper_size.get_active_text() == "Jumbo"):          #Jumbo
            width,height = (102,152)
        elif (self.paper_size.get_active_text() == "6x8"):          #6x8
            width,height = (152,203)
        elif (self.paper_size.get_active_text() == "8x10"):         #8x10
            width,height = (203,254)
        elif (self.paper_size.get_active_text() == "A5"):           #A5
            width,height = (148,210)    
        elif (self.paper_size.get_active_text() == "A4"):           #A4
            width,height = (210,297)
        elif (self.paper_size.get_active_text() == "A3"):           #A3
            width,height = (297,420)
        elif (self.paper_size.get_active_text() == "A2"):           #A2
            width,height = (420,594)
        elif (self.paper_size.get_active_text() == "A1"):           #A1
            width,height = (594,841)
        elif (self.paper_size.get_active_text() == "A0"):           #A0
            width,height = (841,1189)        
        elif (self.paper_size.get_active_text() == "Letter"):       #Letter
            width,height = (216,279)
        elif (self.paper_size.get_active_text() == "Legal"):        #Legal
            width,height = (216,356)
        elif (self.paper_size.get_active_text() == "Tabloid"):      #Tabloid
            width,height = (279,432)
        elif (self.paper_size.get_active_text() == "banner1"):      #banner A4 width
            width,height = (210,1000)
        elif (self.paper_size.get_active_text() == "banner2"):      #banner A3 width
            width,height = (297,1000)
        elif (self.paper_size.get_active_text() == "custom"):       #free sizes
            width,height = (self.paper_width.get_value(), self.paper_height.get_value())
        else:
            width,height = (210,297)          #use default if in error
            Log("error in pagesize, pagesize doesnot exist: " + ContactSize)

        #--convert unit inch or pt to mm if neccessary
        if unit == "inch":
            width = 25,4 * width
            height = 25,4 * height
        elif unit == "pt":
            width = width/0,375
            height = height/0,375
        else:
            # unit is mm
            pass

        #--for top and bottom us height; for left/right use width
        if height == True:
            procent = float(100*margin/height)
        else:
            procent = float(100*margin/width)

        return procent

# ************************** convert unit to %  ************************
    def procent2unit(self, procent, unit, height):
        '''
        procent contains the percentage of the height or width from papersize
        unit contains one of these words: mm, inch or pt
        height is a boolean to decide using width or hight papersize
        sizes noted here are in mm
        '''
        #--get the papersize
        if (self.paper_size.get_active_text() == "Jumbo"):          #Jumbo
            width,height = (102,152)
        elif (self.paper_size.get_active_text() == "6x8"):          #6x8
            width,height = (152,203)
        elif (self.paper_size.get_active_text() == "8x10"):         #8x10
            width,height = (203,254)
        elif (self.paper_size.get_active_text() == "A5"):           #A5
            width,height = (148,210)    
        elif (self.paper_size.get_active_text() == "A4"):           #A4
            width,height = (210,297)
        elif (self.paper_size.get_active_text() == "A3"):           #A3
            width,height = (297,420)
        elif (self.paper_size.get_active_text() == "A2"):           #A2
            width,height = (420,594)
        elif (self.paper_size.get_active_text() == "A1"):           #A1
            width,height = (594,841)
        elif (self.paper_size.get_active_text() == "A0"):           #A0
            width,height = (841,1189)        
        elif (self.paper_size.get_active_text() == "Letter"):       #Letter
            width,height = (216,279)
        elif (self.paper_size.get_active_text() == "Legal"):        #Legal
            width,height = (216,356)
        elif (self.paper_size.get_active_text() == "Tabloid"):      #Tabloid
            width,height = (279,432)
        elif (self.paper_size.get_active_text() == "banner1"):      #banner A4 width
            width,height = (210,1000)
        elif (self.paper_size.get_active_text() == "banner2"):      #banner A3 width
            width,height = (297,1000)
        elif (self.paper_size.get_active_text() == "custom"):       #free sizes
            width,height = (self.paper_width.get_value(), self.paper_height.get_value())
        else:
            width,height = (210,297)          #use default if in error
            Log("error in pagesize, pagesize doesnot exist: " + ContactSize)

        #-- calculate the margin in mm
        if height == True:
            margin = float(procent * height/100)
        else:
            margin = float(procent * width/100)
        
        #-- if neccessary convert to inch or pt
        if unit == "inch":
            margin = float(margin/25.4)
        elif unit == "pt":
            margin = float(margin/0,375)
        else:
            # unit is mm
            pass

        return margin


# ******************************* main caller *********************************
    def docontactsheet(self):
        '''
        This procedure converts the input to the old (PF) style parameters. Goal
        is not to make big changes to the original code
        '''
        # --------------- read&save tab ---------------------
        # ---read
        filetype                = ""
        filetype                = self.makefiletype(filetype)   #make string of filetypes
        select_part_of_filename = self.select_part_of_filename.get_text()
        open_from_location      = self.open_from_location.get_filename()
        include_subdirs         = self.include_subdirs.get_active()
        # ---save
        save_to_location        = self.save_to_location.get_filename()
        filename                = self.filename.get_text()
        if self.extension_jpg.get_active() == True:
            contact_type = ".jpg"
        else:
            contact_type = ".png"
        
        # --------------- page options tab ----------------------
        # ---sheetsize
        paper_size      = self.paper_size.get_active_text()
        CS              = self.paper_size.get_active()  #pointer paper_size
        paper_height    = self.paper_height.get_value()
        paper_width     = self.paper_width.get_value()
        paper_units     = self.paper_units.get_active()  #pointer paper_units

        if self.page_orientation_portrait.get_active() == True:
            orient = "port"
        else:
            orient = "land"

        page_resolution         = self.page_resolution.get_value()
        # ---background
        page_with_background    = self.page_with_background.get_active()
        page_rb_bg_solidcolor   = self.page_rb_bg_solidcolor.get_active()    #radiobutton
        page_rb_bg_image        = self.page_rb_bg_image.get_active()         #radiobutton
        page_background_color   = self.page_background_color.get_color()
        page_background_image   = self.page_background_image.get_filename()
        page_background_image_opacity = self.page_background_image_opacity.get_value() 


        page_with_header  = self.page_with_header.get_active()
        page_header       = self.page_header.get_text()
        page_header_font  = self.page_header_font.get_font_name() #-->output is: sans 12
        page_header_color = self.page_header_color.get_color()

        with_pagenumber     = self.with_pagenumber.get_active()
        pagenumber          = self.pagenumber.get_value()
        total_pages         = self.total_pages.get_active()
        pagenumber_font     = self.pagenumber_font.get_font_name()
        # print(pagenumber_font) #-->output is: sans 12
        pagenumber_color    = self.pagenumber_color.get_color()
        #print(pagenumber_color) # output is: #000

        # --- pagemargins
        topmargin       = self.pagemargin_top.get_value()
        bottommargin    = self.pagemargin_bottom.get_value()
        leftmargin      = self.pagemargin_left.get_value()
        rightmargin     = self.pagemargin_right.get_value()
        pagemargin_units = self.pagemargin_units.get_active()
        
        # ------- image options tab ----------------------
        NumOfRows               = self.numofrows.get_value()
        NumOfCols               = self.numofcols.get_value()
        image_whiteborder       = self.image_whiteborder.get_value()
        image_whiteborder_units = self.image_whiteborder_units.get_active()    #pointer whiteborder_units

        image_aspectratio = self.image_aspectratio.get_active_text()
        AR              = self.image_aspectratio.get_active()  #pointer aspectratio
        image_rotate    = self.image_rotate.get_active()

        # ---caption
        include_imagename       = self.include_imagename.get_active()
        imagename_with_extension = self.imagename_with_extension.get_active()
        caption_fontsize        = 3 #self.caption_fontsize.get_value()
        caption_font            = self.caption_font.get_font_name()
        caption_font_color      = self.caption_font_color.get_color()
        
        if self.pyexiv2_loaded == True:
            include_exif = self.include_exif.get_active()
        else:
            include_exif = False

        include_exif_shutterspeed   = self.include_exif_shutterspeed.get_active()
        include_exif_ISO            = self.include_exif_ISO.get_active()
        include_exif_datetime       = self.include_exif_datetime.get_active()
        include_exif_focal          = self.include_exif_focal.get_active()
        include_exif_lightsource    = self.include_exif_lightsource.get_active()
        include_exif_diafragm       = self.include_exif_diafragm.get_active()
 
        # ------------- other tab --------------------------
        include_list_imagenames = self.include_list_imagenames.get_active()
        direct_printing         = self.direct_printing.get_active()

        images_sort_alphanumeric = self.images_sort_alphanumeric.get_active()
        # ===> to do: sorting on several objects i.e. filename or exifdata
        exif_sort           = self.exif_sort.get_active()
        exif_sort_datetime  = self.exif_sort_datetime.get_active()
        exif_sort_someexif  = self.exif_sort_someexif.get_active()

        # --------- saving configuration for future use ---------
        self.save_config( 'DEFAULT',
            filetype, open_from_location, include_subdirs,
            save_to_location, filename, contact_type,
            paper_size, CS, paper_height, paper_width, paper_units,
            orient, page_resolution,
            page_with_background, page_rb_bg_solidcolor, page_rb_bg_image,
            page_background_color,
            page_background_image, page_background_image_opacity,
            page_with_header, page_header, page_header_font, page_header_color,
            with_pagenumber,pagenumber, pagenumber_font, pagenumber_color, total_pages,
            topmargin, bottommargin, leftmargin, rightmargin, pagemargin_units,
            NumOfCols, NumOfRows,
            image_whiteborder, image_whiteborder_units, AR, image_rotate,
            caption_fontsize, caption_font, caption_font_color,
            include_imagename, imagename_with_extension,
            include_exif, include_exif_datetime, include_exif_ISO,
            include_exif_shutterspeed, include_exif_focal, include_exif_lightsource,
            include_exif_diafragm,
            include_list_imagenames, direct_printing,
            images_sort_alphanumeric,
            exif_sort, exif_sort_datetime, exif_sort_someexif)


        # ********** now we have first to convert some variables ************
        # ********** before entering the main routine ***********************

#        page_background_color    = self.extract_color(self.page_background_color.get_color())

        # extract fontname, size and colorinformation
        pagenumber_font     = self.extract_font_name(self.pagenumber_font.get_font_name())
        pagenumber_fontsize = self.pt2mm(int(self.extract_font_size(self.pagenumber_font.get_font_name())))
        pagenumber_color    = self.extract_color(self.pagenumber_color.get_color())

        page_header_font    = self.extract_font_name(self.page_header_font.get_font_name())
        page_header_fontsize  = self.pt2mm(int(self.extract_font_size(self.page_header_font.get_font_name())))
        page_header_color   = self.extract_color(self.page_header_color.get_color())

        caption_font        = self.extract_font_name(self.caption_font.get_font_name())
        caption_fontsize    = self.pt2mm(int(self.extract_font_size(self.caption_font.get_font_name())))
        caption_font_color  = self.extract_color(self.caption_font_color.get_color())
        
        # --- if papersize is in inches convert it to mm before calling
        if self.paper_units.get_active_text() == "inch":
            paper_height    = self.inch2mm(paper_height)
            paper_width     = self.inch2mm(paper_width)

        # ----------------- do the job -------------------
        GenerateIndexprint.contactsheet(filetype, select_part_of_filename,
            open_from_location, include_subdirs,
            save_to_location, filename, contact_type,
            paper_size, paper_height, paper_width,
            orient, page_resolution,
            page_with_background, page_rb_bg_solidcolor,
            page_background_color,
            page_background_image, page_background_image_opacity, 
            page_with_header, page_header, page_header_font, page_header_color,
            with_pagenumber, pagenumber, pagenumber_font, pagenumber_color, total_pages,
            topmargin, bottommargin, leftmargin, rightmargin,
            NumOfCols, NumOfRows,
            image_whiteborder, AR, image_rotate,
            caption_fontsize, caption_font, caption_font_color,
            include_imagename, imagename_with_extension,
            include_exif,
            include_list_imagenames, direct_printing,
            images_sort_alphanumeric)


# *****************************************************************************
# ====> to do make case insensitive
    def makefiletype(self, filetype):
        '''
        make from all selected filetypes one extended string and return it.
        Input: filetypes
        Output: string of filetypes
        '''
        if self.jpg.get_active() == True:
            filetype = filetype + " .jpg .jpeg .JPG .JPEG"
        if self.png.get_active() == True:
            filetype = filetype + " .png .PNG"
        if self.xcf.get_active() == True:
            filetype = filetype + " .xcf .XCF"
        if self.tif.get_active() == True:
            filetype = filetype + " .tiff .tif .TIF .TIFF"
        if self.pcx.get_active() == True:
            filetype = filetype + " .pcx .PCX"
        if self.bmp.get_active() == True:
            filetype = filetype + " .bmp .BMP"
        if self.gif.get_active() == True:
            filetype = filetype + " .gif .GIF"
        if self.eps.get_active() == True:
            filetype = filetype + " .ps .PS .eps .EPS"
        if self.raw.get_active() == True:
            filetype = filetype + " .RW2 .rw2 .CRW .crw .CR2 .cr2 .NEF .nef .PEF .pef .SR2 .sr2 .RAW .raw .RAF .raf .PEF .pef .DNG .dng"
        if self.wdp.get_active() == True:
            filetype = filetype + " .WDP .wdp .HDP .hdp .JXR .jxr"
        if self.svg.get_active() == True:
            filetype = filetype + " .svg .SVG"
        if self.psd.get_active() == True:
            filetype = filetype + " .psd .PSD"

        return filetype

# *****************************************************************************
    def profile_sections(self, profile):
        '''
        define the profile sections
        '''
        sec_readsave = profile +':' + 'retrieve'
        sec_page = profile +':' + 'page'
        sec_image = profile +':' + 'margins'
        sec_other = profile +':' + 'general'
        return sec_readsave, sec_page, sec_image, sec_other

# *****************************************************************************
    # --------- Save plugin options for nex time -------
    def save_config(self, profile,
            filetype, open_from_location, include_subdirs,
            save_to_location, filename, contact_type,
            paper_size, CS, paper_height, paper_width, paper_units,
            orient, page_resolution,
            page_with_background, page_rb_bg_solidcolor, page_rb_bg_image,
            page_background_color,
            page_background_image, page_background_image_opacity,
            page_with_header, page_header, page_header_font, page_header_color,
            with_pagenumber, pagenumber, pagenumber_font, pagenumber_color, total_pages,
            topmargin, bottommargin, leftmargin, rightmargin, pagemargin_units,
            NumOfCols, NumOfRows,
            image_whiteborder, image_whiteborder_units, AR, image_rotate,
            caption_fontsize, caption_font, caption_font_color,
            include_imagename, imagename_with_extension,
            include_exif, include_exif_datetime, include_exif_ISO, include_exif_shutterspeed,
            include_exif_focal, include_exif_lightsource, include_exif_diafragm,
            include_list_imagenames, direct_printing, images_sort_alphanumeric,
            exif_sort, exif_sort_datetime, exif_sort_someexif
            ):

        sec_readsave, sec_page, sec_image, sec_other = self.profile_sections(profile)
    
        cfg = ConfigParser.RawConfigParser()
        
        # ------------- options to remembered per tab ------------
        # ------------- read&save section ------------------
        cfg.add_section(sec_readsave)
        cfg.set (sec_readsave, 'filetype', filetype)
        # (part of) filename not to be remembered
        cfg.set (sec_readsave, 'open_from_location', open_from_location)
        cfg.set (sec_readsave, 'include_subdirs', include_subdirs)
        cfg.set (sec_readsave, 'save_to_location', save_to_location)
        cfg.set (sec_readsave, 'filename', filename)
        cfg.set (sec_readsave, 'contact_type', contact_type)
        
        # ------------- page options section ---------------
        cfg.add_section(sec_page)
        cfg.set (sec_page, 'paper_size', paper_size)
        cfg.set (sec_page, 'CS', CS)
        cfg.set (sec_page, 'paper_height', paper_height)
        cfg.set (sec_page, 'paper_width', paper_width)
        cfg.set (sec_page, 'paper_units', paper_units)
        cfg.set (sec_page, 'orient', orient)
        cfg.set (sec_page, 'page_resolution', page_resolution)

        cfg.set (sec_page, 'page_with_background', page_with_background)
        cfg.set (sec_page, 'page_rb_bg_solidcolor', page_rb_bg_solidcolor) #radiobutton
        cfg.set (sec_page, 'page_rb_bg_image', page_rb_bg_image) #radiobutton
        cfg.set (sec_page, 'page_background_color', page_background_color)
        cfg.set (sec_page, 'page_background_image', page_background_image) #to be remembered??
        cfg.set (sec_page, 'page_background_image_opacity', page_background_image_opacity)

        cfg.set (sec_page, 'page_with_header', page_with_header)
        cfg.set (sec_page, 'page_header', page_header)
        cfg.set (sec_page, 'page_header_font', page_header_font)
        cfg.set (sec_page, 'page_header_color', page_header_color)

        cfg.set (sec_page, 'with_pagenumber', with_pagenumber)
        cfg.set (sec_page, 'pagenumber', pagenumber)
        cfg.set (sec_page, 'total_pages', total_pages)
        cfg.set (sec_page, 'pagenumber_font', pagenumber_font)
        cfg.set (sec_page, 'pagenumber_color', pagenumber_color)
        
        cfg.set (sec_page, 'topmargin', topmargin)
        cfg.set (sec_page, 'bottommargin', bottommargin)
        cfg.set (sec_page, 'leftmargin', leftmargin)
        cfg.set (sec_page, 'rightmargin', rightmargin)
        cfg.set (sec_page, 'pagemargin_units', pagemargin_units)

        # ------------- image options section --------------
        cfg.add_section(sec_image)
        cfg.set (sec_image, 'NumOfCols', NumOfCols)
        cfg.set (sec_image, 'NumOfRows', NumOfRows)
        cfg.set (sec_image, 'image_whiteborder', image_whiteborder)
        cfg.set (sec_image, 'image_whiteborder_units', image_whiteborder_units)
        cfg.set (sec_image, 'AR', AR)
        cfg.set (sec_image, 'image_rotate', image_rotate)
        cfg.set (sec_image, 'caption_fontsize', caption_fontsize)

        cfg.set (sec_image, 'caption_font', caption_font)
        cfg.set (sec_image, 'caption_font_color', caption_font_color)

        cfg.set (sec_image, 'include_imagename', include_imagename)
        cfg.set (sec_image, 'imagename_with_extension', imagename_with_extension)
        cfg.set (sec_image, 'include_exif', include_exif)
        cfg.set (sec_image, 'include_exif_datetime', include_exif_datetime)
        cfg.set (sec_image, 'include_exif_ISO', include_exif_ISO)
        cfg.set (sec_image, 'include_exif_shutterspeed', include_exif_shutterspeed)
        cfg.set (sec_image, 'include_exif_focal', include_exif_focal)
        cfg.set (sec_image, 'include_exif_lightsource', include_exif_lightsource)
        cfg.set (sec_image, 'include_exif_diafragm', include_exif_diafragm)
        
        # ------------- other section ----------------------
        cfg.add_section(sec_other)
        cfg.set (sec_other, 'include_list_imagenames', include_list_imagenames)
        cfg.set (sec_other, 'direct_printing', direct_printing)
        cfg.set (sec_other, 'images_sort_alphanumeric', images_sort_alphanumeric)
        cfg.set (sec_other, 'exif_sort', exif_sort)
        cfg.set (sec_other, 'exif_sort_datetime', exif_sort_datetime)
        cfg.set (sec_other, 'exif_sort_someexif', exif_sort_someexif)

        with open(self.config_file, 'wb') as configfile:
          cfg.write(configfile)

        return True


# *****************************************************************************
# ******************** load stored configuration ******************************
# *****************************************************************************
    def load_config(self, profile):
        '''
        load stored configuration from configuration file
        '''
        if not os.path.exists(self.config_file):
            Log(_("config file doesnot exist"))
            return False
        else:
            try:
                sec_readsave, sec_page, sec_image, sec_other = self.profile_sections(profile)
                cfg = ConfigParser.RawConfigParser()
                cfg.read(self.config_file)

                # ------------- read&save section ------------------
                try:
                    try:
                        filetype = cfg.get(sec_readsave, 'filetype')
                        if re.search('jpg', filetype):
                            self.jpg.set_active(True)
                        if re.search('png', filetype):
                            self.png.set_active(True)
                        if re.search('tif', filetype):
                            self.tif.set_active(True)
                        if re.search('xcf', filetype):
                            self.xcf.set_active(True)
                        if re.search('pcx', filetype):
                            self.pcx.set_active(True)
                        if re.search('bmp', filetype):
                            self.bmp.set_active(True)
                        if re.search('gif', filetype):
                            self.gif.set_active(True)
                        if re.search('eps', filetype):
                            self.eps.set_active(True)
                        if re.search('rw2', filetype):
                            self.raw.set_active(True)
                        if re.search('wdp', filetype):
                            self.wdp.set_active(True)
                        if re.search('svg', filetype):
                            self.svg.set_active(True)
                        if re.search('psd', filetype):
                            self.psd.set_active(True)
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    # ----(part of) filename not to be remembered

                    try:
                        open_from_location = cfg.get(sec_readsave, 'open_from_location')
                        self.open_from_location.set_current_folder(open_from_location)
                        include_subdirs = cfg.getboolean(sec_readsave, 'include_subdirs')
                        self.include_subdirs.set_active(include_subdirs)
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    try:
                        save_to_location = cfg.get(sec_readsave, 'save_to_location')
                        self.save_to_location.set_current_folder(save_to_location)
                        
                        filename = cfg.get(sec_readsave, 'filename')
                        self.filename.set_text(filename)

                        contact_type = cfg.get(sec_readsave, 'contact_type')
                        if contact_type == '.jpg':
                            self.extension_jpg.set_active(True)
                        else:
                            self.extension_png.set_active(True)
                            
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                except ConfigParser.NoSectionError, err:
                    Log(_("Missing section in config file. %s") + err)
                    print _("Missing section in config file. %s") %err

                # ------------- page options section ---------------

                try:
                    try:
                        paper_units  = cfg.getint(sec_page, 'paper_units')
                        self.paper_units.set_active(paper_units)
                        
                        paper_height = cfg.getfloat(sec_page, 'paper_height')
                        paper_width  = cfg.getfloat(sec_page, 'paper_width')
                        self.paper_height.set_value(paper_height)
                        self.paper_width.set_value(paper_width)
                        

                        paper_size = cfg.get(sec_page, 'paper_size')
                        if  paper_size == "custom":
                            self.paper_height.set_sensitive(True)
                            self.paper_width.set_sensitive(True)
                            self.paper_units.set_sensitive(True)
                        else:
                            self.paper_height.set_sensitive(False)
                            self.paper_width.set_sensitive(False)
                            self.paper_units.set_sensitive(False)
                            
                        CS = cfg.getint(sec_page, 'CS')
                        self.paper_size.set_active(CS)

                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    try:
                        orient = cfg.get(sec_page, 'orient')
                        if orient == 'port':
                            self.page_orientation_portrait.set_active(True)
                        else:
                            self.page_orientation_landscape.set_active(True)

                        page_resolution = cfg.getfloat(sec_page, 'page_resolution')
                        self.page_resolution.set_value(page_resolution)
                            
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass
                   
                    try:
                        page_with_background  = cfg.getboolean(sec_page, 'page_with_background')
                        page_rb_bg_solidcolor = cfg.get(sec_page, 'page_rb_bg_solidcolor') #radiobutton
                        
                        page_background_color = cfg.get(sec_page, 'page_background_color')
                        page_background_image = cfg.get(sec_page, 'page_background_image')
                        page_background_image_opacity = cfg.getfloat(sec_page, 'page_background_image_opacity')

                        self.page_with_background.set_active(page_with_background)
                        self.page_background_color.set_color(gtk.gdk.Color(page_background_color))
                        # set_color() : color should be a GdkColor
                        
                        #-- remember background image????           
                        #self.page_background_image.set_current_folder(page_background_image)
                        self.page_background_image_opacity.set_value(page_background_image_opacity)

                        if page_with_background:
                            if page_rb_bg_solidcolor:
                                self.page_rb_bg_solidcolor.set_active(True)
                                self.page_background_image.set_sensitive(False)
                                self.page_background_image_opacity.set_sensitive(False)
                                self.page_background_color.set_sensitive(True)
                            else:
                                self.page_rb_bg_image.set_active(True)
                                self.page_background_image.set_sensitive(True)
                                self.page_background_image_opacity.set_sensitive(True)
                                self.page_background_color.set_sensitive(False)
                        else:
                            if page_rb_bg_solidcolor:
                                self.page_rb_bg_solidcolor.set_active(True)
                            else:
                                self.page_rb_bg_image.set_active(True)

                            self.page_rb_bg_solidcolor.set_sensitive(False)
                            self.page_rb_bg_image.set_sensitive(False)
                            self.page_background_image.set_sensitive(False)
                            self.page_background_image_opacity.set_sensitive(False)
                            self.page_background_color.set_sensitive(False)
                        
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass


                    try:
                        page_with_header    = cfg.getboolean(sec_page, 'page_with_header')
                        page_header         = cfg.get(sec_page, 'page_header')
                        page_header_font    = cfg.get(sec_page, 'page_header_font')
                        page_header_color   = cfg.get(sec_page, 'page_header_color')

                        self.page_with_header.set_active(page_with_header)
                        self.page_header.set_text(page_header)
                        self.page_header_font.set_font_name(page_header_font)
                        self.page_header_color.set_color(gtk.gdk.Color(page_header_color))

                        with_pagenumber = cfg.getboolean(sec_page, 'with_pagenumber')
                        pagenumber      = cfg.getfloat(sec_page, 'pagenumber')
                        total_pages     = cfg.getboolean(sec_page, 'total_pages')
                        pagenumber_font = cfg.get(sec_page, 'pagenumber_font')
                        pagenumber_color = cfg.get(sec_page, 'pagenumber_color')

                        self.with_pagenumber.set_active(with_pagenumber)
                        self.pagenumber.set_value(pagenumber)
                        self.total_pages.set_active(total_pages)
                        self.pagenumber_font.set_font_name(pagenumber_font)
                        self.pagenumber_color.set_color(gtk.gdk.Color(pagenumber_color))
                        
                        if self.page_with_header.get_active() == True:
                            self.page_header.set_sensitive(True)
                            self.page_header_font.set_sensitive(True)
                            self.page_header_color.set_sensitive(True)
                        else:
                            self.page_header.set_sensitive(False)
                            self.page_header_font.set_sensitive(False)
                            self.page_header_color.set_sensitive(False)


                        if self.with_pagenumber.get_active() == True:
                            self.pagenumber.set_sensitive(True)
                            self.pagenumber_font.set_sensitive(True)
                            self.pagenumber_color.set_sensitive(True)
                            self.total_pages.set_sensitive(True)
                            
                        else:
                            self.pagenumber.set_sensitive(False)
                            self.pagenumber_font.set_sensitive(False)
                            self.pagenumber_color.set_sensitive(False)
                            self.total_pages.set_sensitive(False)

                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    try:    
                        #Log('margins')
                        topmargin       = cfg.getfloat(sec_page, 'topmargin')
                        bottommargin    = cfg.getfloat(sec_page, 'bottommargin')
                        leftmargin      = cfg.getfloat(sec_page, 'leftmargin')
                        rightmargin     = cfg.getfloat(sec_page, 'rightmargin')
                        
                        self.pagemargin_top.set_value(topmargin)
                        self.pagemargin_bottom.set_value(bottommargin)
                        self.pagemargin_left.set_value(leftmargin)
                        self.pagemargin_right.set_value(rightmargin)

                        # pagemargin_units is a pointer not text !
                        pagemargin_units = cfg.getint(sec_page, 'pagemargin_units')
                        self.pagemargin_units.set_active(pagemargin_units)

                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass
                    
                except ConfigParser.NoSectionError, err:
                    Log(_("Missing section in config file. %s") + err)
                    print _("Missing section in config file. %s") %err

                # ------------- image options section --------------    
                try:
                    try:
                        NumOfCols  = cfg.getfloat(sec_image, 'NumOfCols')
                        NumOfRows  = cfg.getfloat(sec_image, 'NumOfRows')
                        self.numofrows.set_value(NumOfRows)
                        self.numofcols.set_value(NumOfCols)
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    try:
                        image_whiteborder = cfg.getfloat(sec_image, 'image_whiteborder')
                        self.image_whiteborder.set_value(image_whiteborder)
                        image_whiteborder_units = cfg.getint(sec_image, 'image_whiteborder_units')
                        self.image_whiteborder_units.set_active(image_whiteborder_units)
                        
                        AR = cfg.getint(sec_image, 'AR')
                        self.image_aspectratio.set_active(AR)
                        image_rotate = cfg.getboolean(sec_image, 'image_rotate')
                        self.image_rotate.set_active(image_rotate)
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    try:
                        include_exif                = cfg.getboolean(sec_image, 'include_exif')
                        include_exif_datetime       = cfg.getboolean(sec_image, 'include_exif_datetime')
                        include_exif_ISO            = cfg.getboolean(sec_image, 'include_exif_ISO')
                        include_exif_shutterspeed   = cfg.getboolean(sec_image, 'include_exif_shutterspeed')
                        include_exif_focal          = cfg.getboolean(sec_image, 'include_exif_focal')
                        include_exif_lightsource    = cfg.getboolean(sec_image, 'include_exif_lightsource')
                        include_exif_diafragm       = cfg.getboolean(sec_image, 'include_exif_diafragm')
                        
                        self.include_exif.set_active(include_exif)
                        self.include_exif_datetime.set_active(include_exif_datetime)
                        self.include_exif_ISO.set_active(include_exif_ISO)
                        self.include_exif_shutterspeed.set_active(include_exif_shutterspeed)
                        self.include_exif_focal.set_active(include_exif_focal)
                        self.include_exif_lightsource.set_active(include_exif_lightsource)
                        self.include_exif_diafragm.set_active(include_exif_diafragm)

                        if include_exif and self.pyexiv2_loaded :
                            self.include_exif_datetime.set_sensitive(True)
                            self.include_exif_ISO.set_sensitive(True)
                            self.include_exif_shutterspeed.set_sensitive(True)
                            self.include_exif_focal.set_sensitive(True)
                            self.include_exif_lightsource.set_sensitive(True)
                            self.include_exif_diafragm.set_sensitive(True)
                        else:
                            self.include_exif_datetime.set_sensitive(False)
                            self.include_exif_ISO.set_sensitive(False)
                            self.include_exif_shutterspeed.set_sensitive(False)
                            self.include_exif_focal.set_sensitive(False)
                            self.include_exif_lightsource.set_sensitive(False)
                            self.include_exif_diafragm.set_sensitive(False)

                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                    try:
                        caption_fontsize = cfg.getfloat(sec_image, 'caption_fontsize')
                        #self.caption_fontsize.set_value(caption_fontsize)

                        caption_font = cfg.get(sec_image, 'caption_font')
                        self.caption_font.set_font_name(caption_font)

                        caption_font_color = cfg.get(sec_image, 'caption_font_color')
                        self.caption_font_color.set_color(gtk.gdk.Color(caption_font_color))
                        
                        include_imagename       = cfg.getboolean(sec_image, 'include_imagename')
                        imagename_with_extension = cfg.getboolean(sec_image, 'imagename_with_extension')
                        self.include_imagename.set_active(include_imagename)
                        self.imagename_with_extension.set_active(imagename_with_extension)

                        if include_imagename :
                            self.imagename_with_extension.set_sensitive(True)
                        else:
                            self.imagename_with_extension.set_sensitive(False)
                        
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                except ConfigParser.NoSectionError, err:
                    Log(_("Missing section in config file. %s") + err)
                    print _("Missing section in config file. %s") %err

                # ------------- other section ----------------------
                try:
                    try:
                        include_list_imagenames = cfg.getboolean(sec_other, 'include_list_imagenames')
                        images_sort_alphanumeric = cfg.getboolean(sec_other, 'images_sort_alphanumeric')
                        direct_printing         = cfg.getboolean(sec_other, 'direct_printing')
                        
                        self.include_list_imagenames.set_active(include_list_imagenames)
                        self.images_sort_alphanumeric.set_active(images_sort_alphanumeric)
                        self.direct_printing.set_active(direct_printing)

                        exif_sort           = cfg.getboolean(sec_other, 'exif_sort')
                        exif_sort_datetime  = cfg.getboolean(sec_other, 'exif_sort_datetime')
                        exif_sort_someexif  = cfg.getboolean(sec_other, 'exif_sort_someexif')

                        self.exif_sort.set_active(exif_sort)
                        self.exif_sort_datetime.set_active(exif_sort_datetime)
                        self.exif_sort_someexif.set_active(exif_sort_someexif)

                        if exif_sort and self.pyexiv2_loaded:
                            self.exif_sort_datetime.set_sensitive(True)
                            self.exif_sort_someexif.set_sensitive(True)
                        else:
                            self.exif_sort_datetime.set_sensitive(False)
                            self.exif_sort_someexif.set_sensitive(False)
                                                
                    except ConfigParser.NoOptionError, err:
                        pass
                    except ValueError, err:
                        pass

                except ConfigParser.NoSectionError, err:
                    Log(_("Missing section in config file. %s") + err)
                    print _("Missing section in config file. %s") %err


            except ConfigParser.Error, err:
                Log(_("Cannot parse configuration file. %s") + err)
                print _("Cannot parse configuration file. %s") %err
                self.on_error(_("Configuration file error"),
                              _("Cannot parse configuration file. ") + str(err))
            except IOError, err:
                Log(_("Problem opening configuration file. %s") + err)
                print _("Problem opening configuration file. %s") %err
                self.on_error(_("Configuration file loading error"),
                              _("Problem opening configuration file.") + str(err))



# *****************************************************************************
# ************************ function to log messages ***************************
# *****************************************************************************
#
def Log(text):
    '''
    Function used for testpurpose and error logging because 'print'
    doesn't work on windows systems
    
    Input: text to log
    Output: error file
    '''
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'errorlog/Error.log')
    f=file(filename, "a+")
    f.write(text+"\n")

    f.close()
