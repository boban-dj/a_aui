#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
from math import trunc,sqrt
import ConfigParser, os, sys, locale, gettext

GAT_DIR = os.path.dirname(os.path.abspath(__file__))
GAT_LOC = ''
GAT_LANG = 'de'

s = locale.getdefaultlocale()
s = s[0]
if s.lower <> 'none':
  s = s.split('_')
  GAT_LANG = s[0]

if sys.platform.startswith('linux'):
  GAT_LOC = GAT_DIR + '/locale'
elif sys.platform.startswith('win'):
  GAT_LOC = GAT_DIR + r'\locale'
else:  
  sys.exit(_('Platform not supported'))

# internationalziation i18n
trans = gettext.translation("gat_tools", GAT_LOC, [GAT_LANG], fallback=True) 
trans.install()


terms_of_use = """
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
"""

nutzungsbedingung = """
  Dieses programm ist freie Software. Sie dürfen es weiterverteilen und / 
  oder modifizieren. Es gelten die Bedingungen der GNU General Public License,
  Version 2, wie sie von dr Free Software Foundation veröffentlicht wurden. 
  
  Dieses Programm wird in Umlauf gebracht in der Hoffnung das es gebraucht wird.
  Trotz allem Bemühen können fehlert nicht ausgeschlossen werde. Es kann deshalb
  keine Garantie für Schäden an Hard und Software übernommen werden, welche durch
  die Ausführung dieses Programmes entsteht.
"""

#### global definitions ###########
if not sys.platform == 'win32':
  GAT_CFG = os.environ['HOME'] + '/.gimp-2.6/gat_tools.cfg'
else :
  GAT_CFG = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\\.gimp-2.6\\gat_tools.cfg'


PHI = (1 + sqrt(5))/2
###################################

def GAT_001(img, draw):           #Center Guides
  v = str(trunc(img.height/2))
  h = str(trunc(img.width/2))
  GAT_002(img, draw, v, h)

def GAT_00101(img, draw):         #Center hrizontal guide
  v = str(trunc(img.height/2))
  h = ""
  GAT_002(img, draw, v, h)

def GAT_00102(img, draw):         #Center vertical guide
  v = ''
  v = str(trunc(img.width/2))
  GAT_002(img, draw, v, h)

def GAT_00103(img, draw):         #golden ratio
  b = trunc(img.height/(PHI + 1))
  a = img.height - b
  v = str(trunc(a)) + ',' + str(trunc(b))
  
  b = trunc(img.width/(PHI + 1))
  a = img.width - b
  h = str(trunc(a))  + ',' + str(trunc(b))
  GAT_002(img, draw, v, h)


def GAT_00104(img, draw):         #fields 3:4
  v = str(trunc(img.height/4.0))  + ',' + str(trunc(img.height/2.0)) + ',' + str(trunc(img.height/4.0*3))
  h = str(trunc(img.width/3.0))   + ',' + str(trunc(img.width/3.0*2))
  GAT_002(img, draw, v, h)

def GAT_00105(img, draw):         #fields 3:3
  v = str(trunc(img.height/3.0))  + ',' + str(trunc(img.height/3.0*2)) 
  h = str(trunc(img.width/3.0))   + ',' + str(trunc(img.width/3.0*2))
  GAT_002(img, draw, v, h)

def GAT_00106(img, draw):         #fields 4:3
  v = str(trunc(img.height/3.0))  + ',' + str(trunc(img.height/3.0*2))
  h = str(trunc(img.width/4.0))   + ',' + str(trunc(img.width/2.0)) + ',' + str(trunc(img.width/4.0*3))
  GAT_002(img, draw, v, h)

def GAT_00107(img, draw):         #fields 4:4
  v = str(trunc(img.height/4.0))  + ',' + str(trunc(img.height/2.0)) + ',' + str(trunc(img.height/4.0*3))
  h = str(trunc(img.width/4.0))   + ',' + str(trunc(img.width/2.0)) + ','  + str(trunc(img.width/4.0*3))
  GAT_002(img, draw, v, h)

def GAT_00108(img, draw):         #rule of third
  v = str(trunc(img.height/3.0))  + ',' + str(trunc(img.height/3.0*2))
  h = str(trunc(img.width/3.0))   + ',' + str(trunc(img.width/3.0*2))
  GAT_002(img, draw, v, h)

def GAT_00109(img,draw):          #from selection
  if pdb.gimp_selection_is_empty(img):
    fail("There is no selection")
  pdb.gimp_image_get_selection(img)
  non_empty, sx1, sy1, sx2, sy2 = pdb.gimp_selection_bounds(img)
  v = str(sy1) + ',' + str(sy2)
  h = str(sx1) + ',' + str(sx2)
  GAT_002(img,draw, v, h)

def GAT_00110(img, draw, xFields, yFields):        #free fields
  v = ''
  i = 1
  while i < xFields:
    if v == '':
      v = str(trunc(img.width / xFields * i ))
    else:
      v = v + ',' + str(trunc(img.width / xFields * i ))
      
    i = i + 1

  h = ''
  i = 1
  while i < yFields:
    if h == '':
      h = str(trunc(img.height / yFields * i )) 
    else:
      h = h + ',' + str(trunc(img.height / yFields * i )) 

    i = i + 1

  GAT_002(img, draw, h, v)

  
##### free selection ############################
def GAT_002(img, draw, hGuides, vGuides):
  _("""creates a number of guides on given position.
Parameter hGuides and vGuides ar comma seperated strings""")
  guides   = hGuides.split(',')

  #draw horizontal guides
  for guide in guides:
    percent  = False
    if guide.find('%') >= 0:
      percent = True
      guide   = guide.replace('%','')

    try:
      pos = int(guide)
    except ValueError:
      pos = -1
    except TypeError:  
      pos = -1
    
    if pos > img.height:
      pos = -1
    
    if pos >= 0:
      if percent:
        pos = trunc(img.height /100.0 * pos)

      guide = pdb.gimp_image_add_hguide(img, pos) 


  #draw vertical guides
  guides=vGuides.split(',')
  for guide in guides:
    percent  = False
    if guide.find('%') >= 0:
      percent = True
      guide   = guide.replace(r"%","")
        
    try:
      pos = float(guide)
    except ValueError:
      pos = -1
    except TypeError:  
      pos = -1
    
    if pos > img.width:
      pos = -1
    
    if pos >= 0:
      if percent:
        pos = trunc(img.width /100.0 * pos)
      guide = pdb.gimp_image_add_vguide(img, pos) 

  pdb.gimp_progress_set_text('www.gimp-atelier.org')



def GAT_003(img, draw, rmGuides, hGuides, vGuides):
  _("""creates a number of guides on given position.
Parameter hGuides and vGuides ar comma seperated strings""")
  if rmGuides == True:
    GAT_005(img, draw)
  GAT_002(img, draw, hGuides, vGuides)

def GAT_004(img, draw, rmGuides, setGuides, nhFields, nvFields):
  _("""creates set of guides""")
  if rmGuides == True:
    GAT_005(img, draw)

  if setGuides == 0:       #center horizontal
    GAT_00101(img, draw)
  elif setGuides == 1:     #center vertical
    GAT_00102(img, draw)
  elif setGuides == 2:     #center cross line
    GAT_001(img, draw) 
  elif setGuides == 3:     #golden ratio
    GAT_00103(img, draw)
  elif setGuides == 4:     #rule of thirds
    GAT_00108(img, draw)
  elif setGuides == 5:     #from selection
    GAT_00109(img, draw) 
  elif setGuides == 6:     #fields 3:4
    GAT_00106(img, draw)
  elif setGuides == 7:     #fields 3:3
    GAT_00105(img,draw)
  elif setGuides == 8:     #fields 4:3
    GAT_00104(img, draw)
  elif setGuides == 9:     #fields 4:4
    GAT_00107(img, draw)
  elif setGuides == 10:    #free fields
    GAT_00110(img, draw, nhFields, nvFields)
  else:
    gimp.message(_('Nothing to do!'))
  pdb.gimp_progress_set_text('www.gimp-atelier.org')
  
  
def GAT_005(img, draw):
  _("remove guides")
  guideId = pdb.gimp_image_find_next_guide(img, 0)
  while guideId <> 0:
    pdb.gimp_image_delete_guide(img, guideId)
    guideId = pdb.gimp_image_find_next_guide(img, 0)

  pdb.gimp_progress_set_text('www.gimp-atelier.org')

def GAT_006(img,draw):
  _("read existing guides from image")
  v = ""
  h = ""
  guideId = pdb.gimp_image_find_next_guide(img, 0)
  while guideId <> 0:
    orientation = pdb.gimp_image_get_guide_orientation(img, guideId)

    if orientation == ORIENTATION_HORIZONTAL:
      if h <> '':
        h = h +  ','
      h = h + str(pdb.gimp_image_get_guide_position(img, guideId))
    else:
      if v <> '':
        v = v +  ','
      v = v + str(pdb.gimp_image_get_guide_position(img, guideId))

    guideId = pdb.gimp_image_find_next_guide(img, guideId)
  
  return (v,h)


def GAT_007(img, draw, rmGuides, SectionName):
  _("reads from cfg file and runs multiple guides")
  if rmGuides:
    GAT_005(img, draw)

  conf = ConfigParser.RawConfigParser()
  conf.read(GAT_CFG)
  v = conf.get(SectionName, 'vertical')
  h = conf.get(SectionName, 'horizontal')
  GAT_002(img, draw, h, v)
  

def GAT_008(img, draw, SectionName):
  _("""reads guides from image an store it in file gat_tools.cfg
sorry, its not possibel to list existing section from file""")
  v,h = GAT_006(img, draw) # get guides

  conf = ConfigParser.RawConfigParser()
  conf.read(GAT_CFG)
  if not conf.has_section(SectionName):
    conf.add_section(SectionName)
  
  conf.set(SectionName, 'vertical',   v)
  conf.set(SectionName, 'horizontal', h)

  # Writing our configuration file to 'example.cfg'
  with open(GAT_CFG, "wb", os.O_CREAT) as cFile:
    conf.write(cFile)
  #os.close(cFile)
  
  
  
# Register with The Gimp
register( "GimpAtelier_tools_003DE",
  _("Gimp Atelier Tools: Multiple Guides"),
  _("a set of Gimp atelier tools"),
  "Hans-G. Normann",
  "© 2010, Hans-G. Normann, Licence GPL",
  "2010-11-15",
  _("<Image>/Tools/Gimp-Atelier/Multiple Guides"),
  "*",
  [
    (PF_BOOL,   "rmGuides", _("Remove existing guides"), True),
    (PF_STRING, "hGuides",  _("Position horziontal guides (y1,y2,....)"),"0"),
    (PF_STRING, "vGuides",  _("Position vertical guides (x1,x2,....)"),"0")
  ],
  '',
  GAT_003)

register( "GimpAtelier_tools_004DE",
  _("Gimp Atelier Tools: Guide Sets"),
  _("a set of Gimp atelier tools"),
  "Hans-G. Normann",
  "© 2010, Hans-G. Normann, Licence GPL",
  "2010-11-15",
  _("<Image>/Tools/Gimp-Atelier/Guide Sets"),
  "*",
  [
    (PF_BOOL,   "rmGuides", _("Remove Existing Guides"),    True),
    (PF_OPTION, "setGuides",_("Set of Guides")         ,      2, [_('Center Horizontal'), _('Center Vertical'), _('Center Cross'),
                                                                  _('Golden Ratio'),      _('Rule of Third'),   _('From Selection'), 
                                                                  _('Fields 3:4'),        _('Fields 3:3'),      _('Fields 4:3'), 
                                                                  _('Fields 4:4'),        _('Free Fields')]),
    (PF_SLIDER, "nhFields", _("Number Of Horizontal Fields"), 1, (1,50,1)),
    (PF_SLIDER, "nvFields", _("Number Of Vertical Fields"),   1, (1,50,1))
  ],
  '',
  GAT_004)


register("GimpAtelier_tools_007DE",
  _("GIMP Atelier Tools: Load From File"),
  _("safe guides in a file"),
  "Hans-G. Normann",
  "© 2010, Hans-G. Normann. Licence GPL",
  "2010-11-15",
  _("<Image>/Tools/Gimp-Atelier/Load Guides From file"),
  "*",
  [
    (PF_BOOL,   "rmGuides",    _("Remove existing guides"), True),
    (PF_STRING, 'SectionName', _("Name of Set"), "Set1")
  ],
  '',
  GAT_007)

register("GimpAtelier_tools_009DE",
  _("GIMP Atelier Tools: Save To File"),
  _("safe guides in a file"),
  "Hans-G. Normann",
  "© 2010, Hans-G. Normann. Licence GPL",
  "2010-11-15",
  _("<Image>/Tools/Gimp-Atelier/Save Guides To File"),
  "*",
  [
    (PF_STRING, 'SectionName', _("Name of Set"), "Set1")
  ],
  '',
  GAT_008)

main()
