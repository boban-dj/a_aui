#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Web Image Menu
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.1
# - ported to GIMP-2.6
# Version 2.0.2
# - new vertical and 2 pieces css for navigbar icons
# - don't show the validation icon if not needed
# - cut title in html header
# Version 2.0.1
# - forgotten to sort the filepathnames
# Version 2.0
# - can use GIMP if PyImaging is not there
# - don't crash when list or description text files don't have enough lines
# - make that small picture are only in scaled dir
# - ported to GIMP-2.4
# - try to recognize system lang
# - try to recognize system encodage
# - use unicode
# - use gettext 
# - moved to glob function and file pathname
# Version 1.0
# - initial release

# Installation : put the photolab_filerename.py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *
import os, locale, glob, shutil, string, urllib

# Optionnal module needed : PyImaging
# http://www.pythonware.com/products/pil/
#
try:
  import Image
  usegimp = False # If PyImaging is not there then use GIMP
except:
  usegimp = True
#usegimp = True # Force to use GIMP aniway here

# Constants
#
dirthumb = "thumbnails"
dirscaled = "scaled"
dirfullsize = "fullsize"
sephtml = "/" # HTML separator in URL, probably better not change this one

# System locale
try:
  encodage = locale.getpreferredencoding('CODESET')
except:
  encodage = locale.getpreferredencoding('') 
#encodage = myCODESET (force encodage here)
  
# Text files encodage
textencodage = "UTF-8" # This Python use UTF-8 encoded text files in entry
  
# System lang
langhtml = locale.getdefaultlocale()[0] #default lang declaration in HTML pages is your locale lang
#langhtml= "en" (force lang here)
  
# i18n
#
import gettext
locale_directory = gimp.locale_directory 
gettext.install( "gimp20-photolab", locale_directory, unicode=True )

#
Photolab_webimagemenu_help = _("Create a photo menu for the Web.")
Photolab_webimagemenu_description = Photolab_webimagemenu_help

# HTML embedded Image Menu
#
MENUIMAGE_HEADER = """<!DOCTYPE html 
\tPUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"
\t\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"HT_LANG\" lang=\"HT_LANG\">
<head>
\t<title>HT_SHORT_TITLE
\t</title>
\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
\t<link rel=\"stylesheet\" type=\"text/css\" href=\"HT_PATH_THEME/webimagemenu.css\" />
</head>
<body>
\t<div id=\"mainpage\">
\t\t<div id=\"titlelarge\">
\t\t\t<p>HT_TITLE
\t\t\t</p>
\t\t</div>  
HT_MENUIMAGE_NAVIGBAR
\t\t<div class=\"menu\">
\t\t\t<ul>\n"""

MENUIMAGE_NAVIGBAR_LINKICON = """\t\t\t\tHT_LINK_FULLSIZE
\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-ok_G2.png\" alt=\"OK\" /></a>   
"""

MENUIMAGE_NAVIGBAR ="""\t\t<div class=\"navigstop\">
\t\t\t<p>
\t\t\t\t<a href=\"HT_LINK_INDEX\" title=\"HT_TEXT_INDEX\">
\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-stop_G2.png\" alt=\"HT_TEXT_INDEX\" /></a>   
\t\t\t</p> 
\t\t</div>
\t\t<div class=\"HT_NAVIGBAR\">
\t\t\t<p>
\t\t\t\t<a href=\"HT_LINK_PREVIOUS\" title=\"HT_TEXT_PREVIOUS\">
\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-up_G2.png\" alt=\"HT_TEXT_PREVIOUS\" /></a>
\t\t\t\t<a href=\"HT_LINK_NEXT\" title=\"HT_TEXT_NEXT\">
\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-down_G2.png\" alt=\"HT_TEXT_NEXT\" /></a>
HT_MENUIMAGE_NAVIGBAR_LINKICON
\t\t\t</p>  
\t\t</div>"""
  
MENUIMAGE_THUMB = """\t\t\t\t<li>
\t\t\t\t\t<p>
\t\t\t\t\t\t<a href=\"HT_LINK_SCALED\" 
\t\t\t\t\t\t\ttitle=\"
\t\t\t\t\t\t\t\tHT_COMMENT
\t\t\t\t\t\t\t\">
\t\t\t\t\t\t\t<img src=\"HT_LINK_THUMB\" alt=\"HT_ALT\" /></a>
\t\t\t\t\t\t<br />
\t\t\t\t\t\tHT_COMMENT
\t\t\t\t\t</p>
\t\t\t\t</li>\n"""
 
MENUIMAGE_FOOTER = """\t\t\t</ul>
\t\t</div>
\t\t<div class=\"image-area\">
\t\t\t<p class=\"image-comment\">
\t\t\t\tHT_COMMENT
\t\t\t</p>
\t\t\t<p class=\"image-desc\">
\t\t\t\tHT_DESCRIPTION
\t\t\t</p>
\t\t\t<p>
\t\t\t\tHT_LINK_FULLSIZE<img src=\"HT_SRC\" alt=\"HT_ALT\" />HT_END_FULLSIZE
\t\t\t</p>
\t\t</div>
\t\t<div id=\"footer\">
\t\t\t<p class=\"border\">
\t\t\t\tHT_CLICK
\t\t\t</p>
\t\t\t<p>
\t\t\t\tHT_FOOTER
\t\t\t</p>
\t\t</div>
\t</div>
</body>
</html>"""

# Main Program
#

def newsizecalculation( imagewidth, imageheight, thmaxsize ):
  if (imagewidth >= imageheight):
    ratiowidth = float( thmaxsize ) / imagewidth
    newimagewidth = thmaxsize
    newimageheight = ratiowidth * imageheight
  else:
    ratioheight = float( thmaxsize ) / imageheight
    newimageheight = thmaxsize
    newimagewidth = ratioheight * imagewidth
  newsizes = []
  newsizes.append( int(newimagewidth) )
  newsizes.append( int(newimageheight) )
  return list( newsizes )

def GIMPresizer( GIMPimage, scfilepathname, scmaxsize ):
  GIMPlayer= pdb.gimp_image_flatten( GIMPimage ) # flatten image in case there is more than one layer 
  imagewidth = GIMPimage.width
  imageheight = GIMPimage.height
  if ((imagewidth > scmaxsize) or (imageheight > scmaxsize)):
    newsizes = newsizecalculation( imagewidth, imageheight, scmaxsize )
    #DEBUG print( "newsizes=",newsizes[0], newsizes[1]) 
    GIMPimage.scale( newsizes[0], newsizes[1] )
    GIMPlayer= pdb.gimp_image_get_active_layer( GIMPimage )  
  pdb.gimp_file_save( GIMPimage, GIMPlayer, scfilepathname, scfilepathname )

def resizer( imageorig, scfilepathname, scmaxsize ):
  # Size calculation
  imagewidth = imageorig.size[0]
  imageheight = imageorig.size[1]
  if ((imagewidth > scmaxsize) or (imageheight > scmaxsize)):
    newsizes = newsizecalculation( imagewidth, imageheight, scmaxsize )
    #DEBUG print( "newsizes=",newsizes[0], newsizes[1]) 
    imagesc = imageorig.resize( (newsizes[0], newsizes[1]), Image.ANTIALIAS )
    imagesc.save( scfilepathname )
  else:  
    imageorig.save( scfilepathname )  
                   
def findcomment( comments, indexfile, filebasename ):
  try:
    if ( comments ):
      filecomment = comments[ indexfile ]
      return filecomment
    else:
      commentfile = open( filebasename+'.txt', 'r' )
      filecomment = commentfile.readline( )
      commentfile.close( ) 
      return filecomment
  except:  
    return filebasename       
            
def htmlisation( index, fileprocessed, 
  title, footer, metaindex, dirtheme, comments, descs, links ):
  
  if( index != 0 ):
    htmlfilename = 'index_'+str( index )+'.html'
  else:  
    htmlfilename = 'index.html'
  
  TITLE = title
  SHORT_TITLE = string.split( title, '<br' )[0][0:49]
  PATH_THEME = dirtheme
  LINK_INDEX = metaindex
  if ( index != 0 ):
    if ( index == 1 ):
      LINK_PREVIOUS = 'index.html'
    else:  
      LINK_PREVIOUS = 'index_'+str( index -1 )+'.html'
  else:
    LINK_PREVIOUS = 'index_'+str( len( fileprocessed ) -1 )+'.html'
  if ( index != len( fileprocessed ) -1 ):   
    LINK_NEXT = 'index_'+str( index +1 )+'.html'
  else:
    LINK_NEXT = 'index.html'
    
  htmlfile = open( htmlfilename,'w' )
  
  indexfile = index
  html_thumbs = ""
  for filepathname in fileprocessed:
    if (indexfile != index):
      filename = os.path.basename( fileprocessed[ indexfile ] )
      filebasename = string.split( filename, '.' )[0] 
      if ( indexfile != 0 ):
        LINK_SCALED = sephtml.join( ['index_'+str( indexfile )+'.html'] )
      else:
        LINK_SCALED = 'index.html'
      html_thumb = string.replace( MENUIMAGE_THUMB, 'HT_LINK_SCALED', LINK_SCALED )
      LINK_THUMB = sephtml.join( [dirthumb, 'th_'+filename] )
      html_thumb = string.replace( html_thumb, 'HT_LINK_THUMB', LINK_THUMB )
      ALT = _("image")+' '+filename
      html_thumb = string.replace( html_thumb, 'HT_ALT', ALT )
      COMMENT = findcomment( comments, indexfile, filebasename ) 
      html_thumb = string.replace( html_thumb, 'HT_COMMENT', COMMENT )
      html_thumbs = html_thumbs +html_thumb
    # Loop parameters
    if ( indexfile == len( fileprocessed ) -1 ):
      indexfile = 0
    else:  
      indexfile = indexfile +1
  filename = os.path.basename( fileprocessed[ index ] )
  filebasename = string.split( filename, '.' )[0] 
  SRC = sephtml.join( [dirscaled, 'sc_'+filename] )
  ALT = _("image")+' '+filename

  if ( links ):
    havelinks = True;
    try:
      file2link = links[ index ][:-1]
    except:
      file2link= "missinglink" #better not to translate this one
    KeyLangLink = _(":: Click on the image to valid the choice ::")
    LINK_FULLSIZE = '<a href="'+file2link+'"' 
    LINK_FULLSIZE = LINK_FULLSIZE +' title="'+ KeyLangLink +'">'
    END_FULLSIZE = '</a>'
    html_navigbar_linkicon = string.replace( MENUIMAGE_NAVIGBAR_LINKICON, 'HT_PATH_THEME', PATH_THEME )
    html_navigbar_linkicon = string.replace( html_navigbar_linkicon, 'HT_LINK_FULLSIZE', LINK_FULLSIZE )  
  else:
    havelinks = False;
    if ( os.path.exists( os.path.join( dirfullsize, 'fs_'+filename ))):
      KeyLangLink = _(":: Click to enlarge the image ::")
      LINK_FULLSIZE = '<a href="'+sephtml.join( [dirfullsize, 'fs_'+filename] )+'"'
      LINK_FULLSIZE = LINK_FULLSIZE +' title="'+ KeyLangLink +'">'
      END_FULLSIZE = '</a>'
    else:
      KeyLangLink = '' 
      LINK_FULLSIZE = '' 
      END_FULLSIZE = ''  
  COMMENT = findcomment( comments, index, filebasename )
  if ( descs ):
    try:
      DESCRIPTION = descs[ index ]
    except:
      DESCRIPTION = _("Description missing")
  else:
    DESCRIPTION = '' 

  html_navigbar = string.replace( MENUIMAGE_NAVIGBAR, 'HT_PATH_THEME', PATH_THEME )
  html_navigbar = string.replace( html_navigbar, 'HT_LINK_INDEX', LINK_INDEX )
  html_navigbar = string.replace( html_navigbar, 'HT_TEXT_INDEX', _("back to index") )
  html_navigbar = string.replace( html_navigbar, 'HT_LINK_PREVIOUS', LINK_PREVIOUS )
  html_navigbar = string.replace( html_navigbar, 'HT_TEXT_PREVIOUS', _("previous") )
  html_navigbar = string.replace( html_navigbar, 'HT_LINK_NEXT', LINK_NEXT )  
  html_navigbar = string.replace( html_navigbar, 'HT_TEXT_NEXT', _("next") )
  if ( havelinks ):
    html_navigbar = string.replace( html_navigbar, 'HT_NAVIGBAR', 'navigbar3' )   
    html_navigbar = string.replace( html_navigbar, 'HT_MENUIMAGE_NAVIGBAR_LINKICON', html_navigbar_linkicon )
  else:
    html_navigbar = string.replace( html_navigbar, 'HT_NAVIGBAR', 'navigbar2' )   
    html_navigbar = string.replace( html_navigbar, 'HT_MENUIMAGE_NAVIGBAR_LINKICON', '' )    
  
  html_header = string.replace( MENUIMAGE_HEADER, 'HT_LANG', langhtml )
  html_header = string.replace( html_header, 'HT_SHORT_TITLE', SHORT_TITLE )
  html_header = string.replace( html_header, 'HT_TITLE', TITLE )
  html_header = string.replace( html_header, 'HT_PATH_THEME', PATH_THEME )
  html_header = string.replace( html_header, 'HT_MENUIMAGE_NAVIGBAR', html_navigbar )
    
  html_footer = string.replace( MENUIMAGE_FOOTER, 'HT_FOOTER', footer )
  html_footer = string.replace( html_footer, 'HT_CLICK', KeyLangLink )  
  html_footer = string.replace( html_footer, 'HT_COMMENT', COMMENT )
  html_footer = string.replace( html_footer, 'HT_DESCRIPTION', DESCRIPTION )
  html_footer = string.replace( html_footer, 'HT_SRC', SRC )
  html_footer = string.replace( html_footer, 'HT_ALT', ALT )

  html_footer = string.replace( html_footer, 'HT_LINK_FULLSIZE', LINK_FULLSIZE )
  html_footer = string.replace( html_footer, 'HT_END_FULLSIZE', END_FULLSIZE )   


  htmlfile.write( html_header +html_thumbs +html_footer )
  htmlfile.close( )  


def python_fu_template_xtns( 
  dirname, 
  ext,
  title, 
  footer,
  metaindex,
  dirtheme,
  sizethumb,
  sizescaled,
  sizefullsize ): #inImage, inDrawable, 
  
  if os.path.exists( u''+dirname ):
    #
    globpattern = u''+dirname + os.sep + '*.' + ext
    filepathnames = glob.glob( globpattern ) # return complete path name of files
    #
    if filepathnames:
      filepathnames.sort()
      #
      messagebox = pdb.gimp_message_get_handler( ) 
      pdb.gimp_message_set_handler( 2 )
      # need to change to the Working directory
      recoverydir = os.getcwd()
      os.chdir( u''+dirname )        
      #
      dirthumbpathname = os.path.join( u''+dirname, dirthumb )
      if os.path.exists( dirthumbpathname ):
        shutil.rmtree( dirthumbpathname )
      os.mkdir( dirthumbpathname )
      #
      dirscaledpathname = os.path.join( u''+dirname, dirscaled )
      if os.path.exists( dirscaledpathname ):
        shutil.rmtree( dirscaledpathname )
      os.mkdir( dirscaledpathname )
      #
      dirfullsizepathname = os.path.join( u''+dirname, dirfullsize )
      if os.path.exists( dirfullsizepathname ):
        shutil.rmtree( dirfullsizepathname )
      os.mkdir( dirfullsizepathname )
      #
      # Overwrite Title, Meta-index, Footer with txt files when exists
      try:
        titlefile = open( 'title.txt', 'r' )
        encodedtitle = titlefile.readline( )
        title = encodedtitle.decode( textencodage ) 
        titlefile.close( ) 
        pdb.gimp_message( _("title.txt found use encodage: %s") %(textencodage) )                
      except:  
        pdb.gimp_message( _("title.txt not found use title value: %s") %(title) )  
      try:
        metaindexfile = open( 'metaindex.txt', 'r' )
        encodedmetaindex = string.split( metaindexfile.readline( ))[0]
        metaindex = encodedmetaindex.decode( textencodage ) 
        metaindexfile.close( ) 
        pdb.gimp_message( _("metaindex.txt found use encodage: %s") %(textencodage) )                
      except:  
        pdb.gimp_message( _("metaindex.txt not found use metaindex value: %s") %(metaindex) ) 
      try:
        footerfile = open( 'footer.txt', 'r' )
        encodedfooter = footerfile.readline( )
        footer = encodedfooter.decode( textencodage ) 
        footerfile.close( ) 
        pdb.gimp_message( _("footer.txt found use encodage: %s") %(textencodage) )                
      except:  
        pdb.gimp_message( _("footer.txt not found use footer value: %s") %(footer) )
      #  
      # Read comment.txt file when exists
      comments = []
      try:
        commentfile = open( 'comment.txt', 'r' )
        encodedcomments = commentfile.readlines( )
        for encodedcomment in encodedcomments:
          comments.append( encodedcomment.decode( textencodage ))    
        commentfile.close( ) 
        pdb.gimp_message( _("comment.txt found use encodage: %s") %(textencodage) )                
      except:
        pdb.gimp_message( _("comment.txt not found use individual comment files or filenames") )
      #
      # Read description.txt file when exists
      descs = []
      try:
        descfile = open( 'description.txt', 'r' )
        encodeddescs = descfile.readlines( )
        for encodeddesc in encodeddescs:
          descs.append( encodeddesc.decode( textencodage ))
        descfile.close( ) 
        pdb.gimp_message( _("description.txt found use encodage: %s") %(textencodage) )                
      except:
        pdb.gimp_message( _("decription.txt not found") )
      #  
      # Read link.txt file when exists
      links = []
      try:   
        linkfile = open( 'link.txt', 'r' )
        encodedlinks = linkfile.readlines( )
        for encodedlink in encodedlinks:
          links.append( encodedlink.decode( textencodage ))
        linkfile.close( ) 
        pdb.gimp_message( _("link.txt found use encodage: %s") %(textencodage) )
      except:     
        pdb.gimp_message( _("link.txt not found use fullsize images") )
      #        
      # Let start serious things  
      pdb.gimp_message( _("File processing is starting, please wait...") )      
      fileprocessed = []      
      for filepathname in filepathnames:
        try:
          file = open( filepathname, 'rb' )
        except:
          if os.path.exists( filepathname ):
            pdb.gimp_message( "%s is a directory" %(filepathname) )
          else:
            pdb.gimp_message( "%s: Error" %(filepathname) )
          continue    
        # Files processing
        if usegimp: # with GIMP
          try:
            GIMPimage= pdb.gimp_file_load( filepathname , filepathname )
          except:
            pdb.gimp_message( _("%s can't be treated by GIMP") %(filepathname) )
          else:
            undogimp = pdb.gimp_image_undo_disable( GIMPimage )
            thfilepathname = os.path.join( dirthumbpathname, 'th_'+ os.path.basename(filepathname))
            GIMPresizer( GIMPimage, thfilepathname, sizethumb )                        
            #
            GIMPimage= pdb.gimp_file_load( filepathname , filepathname )
            undogimp = pdb.gimp_image_undo_disable( GIMPimage )
            scfilepathname = os.path.join( dirscaledpathname, 'sc_' + os.path.basename(filepathname) )
            GIMPresizer( GIMPimage, scfilepathname, sizescaled )
            #
            fsfilepathname = os.path.join( dirfullsizepathname, 'fs_'+ os.path.basename(filepathname) )   
            if ( sizefullsize > sizescaled ): #check if fullsize is needed or not
              GIMPimage= pdb.gimp_file_load( filepathname , filepathname )
              undogimp = pdb.gimp_image_undo_disable( GIMPimage )
              imagewidth = GIMPimage.width
              if ( imagewidth > sizescaled ): #if false then the full image is still visible in scaled dir
                GIMPresizer( GIMPimage, fsfilepathname, sizefullsize )
            fileprocessed.append( filepathname )
        else: # with PyImaging
          try:
            imageorig = Image.open( u''+filepathname )
          except:
            pdb.gimp_message( _("%s can't be treated by PyImaging") %(filepathname) )          
          else:   
            thfilepathname = os.path.join( dirthumbpathname, 'th_'+ os.path.basename(filepathname))
            resizer( imageorig, thfilepathname, sizethumb )        
            #  
            scfilepathname = os.path.join( dirscaledpathname, 'sc_'+ os.path.basename(filepathname)) 
            resizer( imageorig, scfilepathname, sizescaled )
            # 
            fsfilepathname = os.path.join( dirfullsizepathname, 'fs_'+ os.path.basename(filepathname) )   
            if ( sizefullsize > sizescaled ): #check if fullsize is needed or not
              imagewidth = imageorig.size[0]
              if ( imagewidth > sizescaled ): #if false then the full image is still visible in scaled dir
                resizer( imageorig, fsfilepathname, sizefullsize )
            fileprocessed.append( filepathname )
      #    
      # HTML start here
      pdb.gimp_message( "HTML generation is starting" )
      if ( fileprocessed ):
        indexfile = 0
        for filepathname in fileprocessed:
          filename = os.path.basename(fileprocessed[indexfile])
          htmlisation( indexfile, fileprocessed, 
            title, footer, metaindex, dirtheme, comments, descs, links )
          indexfile = indexfile +1
      # recover directory
      os.chdir( u''+recoverydir )        
      # End of process         
      pdb.gimp_message( _("End of the process") )        
      pdb.gimp_message_set_handler( messagebox )
    else:
      pdb.gimp_message( "%s is empty" %(dirname) )      
  else:
    pdb.gimp_message( "%s is not a directory" %(dirname) )

register(
  "WebImageMenuXtns",
  Photolab_webimagemenu_description,
  Photolab_webimagemenu_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Web Image Menu"),
  "",
  [
    (PF_DIRNAME, "directory", _("Working Directory"), os.getcwd() ),
    (PF_STRING, "ext", _("Extension"), 'jpg' ),
    (PF_STRING, "title", _("Title"), _("Title") ),
    (PF_STRING, "footer", _("Footer"), _("Copyright") ),
    (PF_STRING, "metaindex", _("HTML Path to Meta-Index"), ".."+sephtml+"index.html" ),
    (PF_STRING, "dirtheme", _("HTML Path to Theme"), ".."+sephtml+"theme" ),      
    (PF_INT, "sizethumb", _("Thumbnails Size (px)"), 140),
    (PF_INT, "sizescaled", _("Scaled Size (px)"), 600),
    (PF_INT, "sizefullsize", _("Full Size (px)"), 1600),
  ],
  [],
  python_fu_template_xtns,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Gallery"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
