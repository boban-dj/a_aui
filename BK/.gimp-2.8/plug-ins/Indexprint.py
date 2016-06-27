#!/usr/bin/python2
# -*- coding: UTF-8 -*-

"""
Copyright

Elmar Sullock Enzlin at moroquendo@gmail.com
(C) 2009, ..., 2012 Utrecht, The Netherlands

This plugin was tested with Gimp V2.6/2.8


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
"""

"""
VERSION HISTORY
# Released 27.dec.2012 -- (indexprint-development, later renamed to v4)
# * changed: from one screen to notebook style.
# * changed: ps/eps better rendered.
# * changed: sorting has been changed, still to do: sorting on exif.
# * added: background can be colored or image. Opacity can be set. 
# * added: Some new extensions added.
# * added: Caption, title header, pagenumber: font, size and color can be set. 
# * added: several other measurement units are added.
# * added: list has now chapters.
# * added/changed: a lot of other things. 
#
# Released ??????? -- v3.33
# * added: .svg and .psd format
# * added: scrolled window
# * fixed: ??
#
# v3.32 never been released
#
# Released 05.dec.2011 -- v3.31
# * added: focal length
# * added: jpeg HDR format
# * fixed: on Linux (ubuntu) type error integer expected got float.
#
# Released 02.may.2011 -- v3.30
# * added: several raw format types (panasonic: rw2, canon: crw, cr2, nikon: nef,
#           fuji: raf, samsung: pef, adobe: dng, pentax: pef, sony: sr2, arw)

# Released 15.april.2011 -- v3.22
# * added: more exif information: iso, speed and F-number
# * change: version w/o exif and w exif now combined
# * change: readme
# * fixed: header cannot contain spaces only without chrashing
# * fixed: not correct working switch
# * fixed: several typos
#
# Released 05.march.2011 -- v3.21
# * fixed: temporarily spaces in header
#
# Released 05.febr.2011 -- v3.20
# * added exif information -> pyexiv2 should be installed, seperate install
# * added: header information
# * change: pagenumber and total pages
# * added inda decoder for Linux works also on Windows
# 		removed in version beta mbcs because Linux didn't recognize it
# * added: change background color
# * change: custom paper setting working now
# * change: updated languages
#
# Released 19.nov.2010 -- v3.10
# * change: remember settings between sessions
# * CHANGE: gui improvements
# * change: numbering files now same as on paper (request G.Sprik)
# * change: now possible to select on a piece of the filename (request G.Sprik)
# * change: easier install (one step install)
# * change: no problems with foreign characters anymore
# * change: no problems with non-image files with image extensions
#           (i.e. readme.jpg), reported in an error.log
# * change: added a config dir
# * change: added a errorlog dir, necessary for windows because
#           print doesn't work.
# * change: added a doc dir with the manual
# * change: new dutch translation file
# * change: several other small changes has been made

# Initial working release v3.00
This version works on Gimp 2.6 with python and GTK+ installed 
"""

import os, gettext

# *****************************************************************************
# ********************** initialize internationalisation **********************
# *****************************************************************************
APP = "indexprint"                              #name of the translation file
locale_dir = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  APP), 'locale')
##locale_dir = os.path.join(os.path.dirname(os.path.abspath(indexprint.__file__)),\
##                          indexprint/locale)

#locale.setlocale(locale.LC_ALL, '')            #reset all
gettext.install(APP,\
                locale_dir,\
                unicode=True)


# *****************************************************************************
# ************************* calling the main routine **************************
# *****************************************************************************
def plugin_main():
    import indexprint.gui               # import package that is meat of plugin
    app = indexprint.gui.ContactsheetApp()  # create instance of gtkBuilder app
    app.main()                          # event loop for app


# *****************************************************************************
# ************************ function to log messages ***************************
# *****************************************************************************
# to do: make this function global
#
def Log(text):
    """
    Function used for testpurpose and error logging because 'print'
    doesn't work on windows systems.
    Finally found something usefull to 'bypass' print:
    Starting Gimp in the cmd console with Gimp-xxx.exe > error.txt 2>&1
    redirects stdout and stderr output to error.txt
    
    Input: text to log
    Output: error file
    """
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'errorlog/Error.log')
    f=file(filename, "a+")
    f.write(text+"\n")
    f.close()
    

# *****************************************************************************
# **************************** Gimp registration ******************************
# *****************************************************************************
if __name__ == "__main__":
    from gimpfu import * 
    register(
        "python_fu_indexprint",
        _("Collects images and put them on a sheet of paper."),
        "Indexprint",
        "E. Sullock Enzlin",
        "Copyright 2009, ..., 2012 E. Sullock Enzlin",
        "2009, 2010, 2011, 2012",
        "_Indexprint",
        "", # image types: blank means don't care but no image param
        [],
        [],
        plugin_main,
        menu="<Image>/File/Send")   
        # other: "<Image>/File/Create"
        # domain=("indexprint", gimp.locale_directory))
    
    main()
