#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PhotoLab :: Web Gallery
# Copyright Raymond Ostertag 2007-2009
# Licence GPL

# Version 2.1
# - ported to GIMP-2.6
# Version 2.0.1
# - forgotten to sort the filepathnames
# Version 2.0
# - can use GIMP if PyImaging is not there
# - made that small picture are not duplicate in fullsize dir
# - ported to GIMP-2.4
# - try to recognize system lang
# - try to recognize system encodage
# - use unicode
# - use gettext 
# - moved to glob function and file pathname
# Version 1.0
# - initial release

# Installation : put the python-fu .py file in your $HOME/.gimp-2.n/plug-ins.
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
sizehtmlpage = 900  # must be coherent with webgallery.css file
dirthumb = "thumbnails"
dirscaled = "scaled"
dirfullsize = "fullsize"
dirhtml = "html"
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
Photolab_webgallery_help = _("Create a photo gallery for the Web.")
Photolab_webgallery_description = Photolab_webgallery_help

#
# HTML embedded Templates Image
#
HTML_HEADER = """<!DOCTYPE html 
\tPUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"
\t\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"HT_LANG\" lang=\"HT_LANG\">
<head>
\t<title>HT_TITLE
\t</title>
\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
HT_META_REDIRECTION
\t<link rel=\"stylesheet\" type=\"text/css\" href=\"HT_PATH_THEME/webgallery.css\" />
\t<link rel=\"start\" href=\"HT_LINK_INDEX\" />
\t<link rel=\"up\" href=\"HT_LINK_INDEX\" />
\t<link rel=\"next\" href=\"HT_LINK_NEXT\" />
\t<link rel=\"prev\" href=\"HT_LINK_PREVIOUS\" />
\t<link rel=\"index\" href=\"HT_LINK_INDEX\" />
</head>
<body>
\t<div id=\"mainpage\">
\t\t<div id=\"title\">
\t\t\t<p>HT_TITLE
\t\t\t</p>
\t\t</div>  
\t\t<div class=\"navigbar\">
\t\t\t<table>
\t\t\t\t<tr>
\t\t\t\t\t<td align=\"left\">
\t\t\t\t\t\t<a href=\"HT_LINK_PREVIOUS\" title=\"previous\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/HT_ICON_PREVIOUS\" alt=\"previous\" /></a>
\t\t\t\t\t</td>
\t\t\t\t\t<td>
\t\t\t\t\t\t<a href=\"HT_LINK_INDEX\" title=\"back to index\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-up.png\" alt=\"back to index\" /></a>
\t\t\t\t\t</td>
\t\t\t\t\t<td>
\t\t\t\t\t\t<a href=\"HT_LINK_SLIDESHOW\" title=\"slideshow\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/HT_ICON_SLIDESHOW\" alt=\"slideshow\" /></a>
\t\t\t\t\t</td>
\t\t\t\t\t<td align=\"right\">
\t\t\t\t\t\t<a href=\"HT_LINK_NEXT\" title=\"next\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/HT_ICON_NEXT\" alt=\"next\" /></a>
\t\t\t\t\t</td>    
\t\t\t\t</tr>
\t\t\t</table>  
\t\t</div>
\t\t<div class=\"image-area\">
\t\t\t<p>
\t\t\t\tHT_LINK_FULLSIZE<img src=\"HT_SRC\" alt=\"HT_ALT\" />HT_END_FULLSIZE
\t\t\t</p>
\t\t\t<p class=\"image-comment\">HT_COMMENT
\t\t\t</p>
\t\t</div>     
\t\t<div class=\"navigbar\">
\t\t\t<table>
\t\t\t\t<tr>
\t\t\t\t\t<td align=\"left\">
\t\t\t\t\t\t<a href=\"HT_LINK_PREVIOUS\" title=\"previous\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/HT_ICON_PREVIOUS\" alt=\"previous\" /></a>
\t\t\t\t\t</td>
\t\t\t\t\t<td>
\t\t\t\t\t\t<p>HT_INDEX/HT_ENDINDEX</p>
\t\t\t\t\t</td>
\t\t\t\t\t<td align=\"right\">
\t\t\t\t\t\t<a href=\"HT_LINK_NEXT\" title=\"next\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/HT_ICON_NEXT\" alt=\"next\" /></a>
\t\t\t\t\t</td>    
\t\t\t\t</tr>
\t\t\t</table>
\t\t</div>
\t\t<div id=\"footer\">
\t\t\t<p>HT_FOOTER
\t\t\t</p>
\t\t</div>
\t</div>
</body>
</html>"""

# HTML embedded Templates Index
#
INDEX_HEADER = """<!DOCTYPE html 
\tPUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"
\t\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"HT_LANG\" lang=\"HT_LANG\">
<head>
\t<title>HT_TITLE
\t</title>
\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
\t<link rel=\"stylesheet\" type=\"text/css\" href=\"HT_PATH_THEME/webgallery.css\" />
</head>
<body>
\t<div id=\"mainpage\">
\t\t<div id=\"title\">
\t\t\t<p>HT_TITLE
\t\t\t</p>
\t\t</div>  
\t\t<div class=\"navigbar\">
\t\t\t<table>
\t\t\t\t<tr>
HT_TD_PREVIOUS
\t\t\t\t\t<td>
\t\t\t\t\t\t<a href=\"HT_LINK_INDEX\" title=\"back to meta-index\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-up.png\" alt=\"back to meta-index\" /></a>
\t\t\t\t\t</td>
HT_TD_NEXT
\t\t\t\t</tr>
\t\t\t</table>  
\t\t</div>
\t\t<div class=\"image-area\">
\t\t\t<table cellspacing=\"1em\">\n"""
 
HT_TD_PREVIOUS = """\t\t\t\t\t<td align=\"left\">
\t\t\t\t\t\t<a href=\"HT_LINK_PREVIOUS\" title=\"previous\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-prev.png\" alt=\"previous\" /></a>
\t\t\t\t\t</td>"""

HT_TD_NEXT = """\t\t\t\t\t<td align=\"right\">
\t\t\t\t\t\t<a href=\"HT_LINK_NEXT\" title=\"next\">
\t\t\t\t\t\t\t<img src=\"HT_PATH_THEME/images/icon-next.png\" alt=\"next\" /></a>
\t\t\t\t\t</td>"""    
 
HT_TD_EMPTY = """\t\t\t\t\t<td align=\"right\">
\t\t\t\t\t\t<p>&nbsp;</p>
\t\t\t\t\t</td>"""     
 
INDEX_THUMB = """\t\t\t\t\t<td>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t<a href=\"HT_LINK_SCALED\">
\t\t\t\t\t\t\t\t<img src=\"HT_LINK_THUMB\" alt=\"HT_ALT\" /></a>
\t\t\t\t\t\t\t<br />
\t\t\t\t\t\t\tHT_COMMENT
\t\t\t\t\t\t</p>
\t\t\t\t\t</td>\n"""
 
INDEX_FOOTER = """\t\t\t</table>
\t\t</div>
\t\t<div class=\"navigbar\">
\t\t\t<table>
\t\t\t\t<tr>
HT_TD_PREVIOUS
\t\t\t\t\t<td>
\t\t\t\t\t\t<p>HT_INDEX/HT_ENDINDEX</p>
\t\t\t\t\t</td>
HT_TD_NEXT
\t\t\t\t</tr>
\t\t\t</table>
\t\t</div>
\t\t<div id=\"footer\">
\t\t\t<p>HT_FOOTER
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
      commentfile = open( u''+filebasename+'.txt', 'r' )
      filecomment = commentfile.readline( )
      commentfile.close( ) 
      return filecomment
  except:  
    return filebasename       
          
def htmlisation( indexpage, index, lastfile, 
  filename, filebasename, prevbasename, nextbasename, 
  title, footer, dirtheme, slidetime, comments ):

  htmlfilename = sephtml.join( [dirhtml, 'ht_'+filebasename+'.html'] )
  slfilename = sephtml.join( [dirhtml, 'sl_'+filebasename+'.html'] )
  htmlindexname = sephtml.join( ['..', 'index_'+str( indexpage )+'.html'] )

  TITLE = title
  PATH_THEME = sephtml.join( ['..', dirtheme] )
  if ( prevbasename == '' ):
    LINK_PREVIOUS =  htmlindexname
    LINK_SL_PREVIOUS =  htmlindexname
    ICON_PREVIOUS = 'icon-up.png'
  else:
    LINK_PREVIOUS =  'ht_'+prevbasename+'.html'
    LINK_SL_PREVIOUS = 'sl_'+prevbasename+'.html'
    ICON_PREVIOUS = 'icon-prev.png'
  if ( nextbasename == '' ):
    LINK_NEXT = htmlindexname  
    LINK_SL_NEXT = htmlindexname
    ICON_NEXT = 'icon-up.png'    
  else:
    LINK_NEXT = 'ht_'+nextbasename+'.html'
    LINK_SL_NEXT = 'sl_'+nextbasename+'.html'
    ICON_NEXT = 'icon-next.png'
  LINK_SL_NEXT = urllib.quote(LINK_SL_NEXT.encode( encodage )) # encode URL in META DATA
  META_REDIRECTION = '\t<meta http-equiv="Refresh" content="'+str( slidetime )+'; URL=\''+LINK_SL_NEXT+'\'">'  
  LINK_INDEX = htmlindexname
  LINK_SLIDESHOW = 'sl_'+filebasename+'.html'
  LINK_NOSLIDESHOW = 'ht_'+filebasename+'.html'
  ICON_SLIDESHOW = 'icon-slideshow.png'
  ICON_NOSLIDESHOW = 'icon-stop.png'
  SRC = sephtml.join( ['..', dirscaled, 'sc_'+filename] )
  ALT = _("image")+' '+filename
  if ( os.path.exists( sephtml.join( [dirfullsize, 'fs_'+filename] ))):
    LINK_FULLSIZE = '<a href="'+sephtml.join( ['..', dirfullsize, 'fs_'+filename] )+'">'
    END_FULLSIZE = '</a>'
  else:
    LINK_FULLSIZE = '' 
    END_FULLSIZE = ''     
  COMMENT = findcomment( comments, index, filebasename )
        
  htmlfile = open( u''+htmlfilename,'w' )
  html_text = string.replace( HTML_HEADER, 'HT_LANG', langhtml )
  html_text = string.replace( html_text, 'HT_META_REDIRECTION', '' )
  html_text = string.replace( html_text, 'HT_TITLE', TITLE )
  html_text = string.replace( html_text, 'HT_PATH_THEME', PATH_THEME )
  html_text = string.replace( html_text, 'HT_LINK_PREVIOUS', LINK_PREVIOUS )
  html_text = string.replace( html_text, 'HT_ICON_PREVIOUS', ICON_PREVIOUS )
  html_text = string.replace( html_text, 'HT_LINK_INDEX', LINK_INDEX )
  html_text = string.replace( html_text, 'HT_LINK_SLIDESHOW', LINK_SLIDESHOW )
  html_text = string.replace( html_text, 'HT_ICON_SLIDESHOW', ICON_SLIDESHOW )
  html_text = string.replace( html_text, 'HT_LINK_NEXT', LINK_NEXT )
  html_text = string.replace( html_text, 'HT_ICON_NEXT', ICON_NEXT )
  html_text = string.replace( html_text, 'HT_SRC', SRC )
  html_text = string.replace( html_text, 'HT_ALT', ALT )
  html_text = string.replace( html_text, 'HT_LINK_FULLSIZE', LINK_FULLSIZE )
  html_text = string.replace( html_text, 'HT_END_FULLSIZE', END_FULLSIZE )
  html_text = string.replace( html_text, 'HT_FOOTER', footer )
  html_text = string.replace( html_text, 'HT_COMMENT', COMMENT )
  html_text = string.replace( html_text, 'HT_INDEX', str( index +1 ))
  html_text = string.replace( html_text, 'HT_ENDINDEX', str( lastfile +1 ))  
  htmlfile.write( html_text )
  htmlfile.close( )
  
  htmlfile = open( u''+slfilename,'w' )
  html_text = string.replace( HTML_HEADER, 'HT_LANG', langhtml )
  html_text = string.replace( html_text, 'HT_META_REDIRECTION', META_REDIRECTION )
  html_text = string.replace( html_text, 'HT_TITLE', TITLE )
  html_text = string.replace( html_text, 'HT_PATH_THEME', PATH_THEME )
  html_text = string.replace( html_text, 'HT_LINK_PREVIOUS', LINK_PREVIOUS )
  html_text = string.replace( html_text, 'HT_ICON_PREVIOUS', ICON_PREVIOUS )
  html_text = string.replace( html_text, 'HT_LINK_INDEX', LINK_INDEX )
  html_text = string.replace( html_text, 'HT_LINK_SLIDESHOW', LINK_NOSLIDESHOW )
  html_text = string.replace( html_text, 'HT_ICON_SLIDESHOW', ICON_NOSLIDESHOW )
  html_text = string.replace( html_text, 'HT_LINK_NEXT', LINK_NEXT )
  html_text = string.replace( html_text, 'HT_ICON_NEXT', ICON_NEXT )
  html_text = string.replace( html_text, 'HT_SRC', SRC )
  html_text = string.replace( html_text, 'HT_ALT', ALT )
  html_text = string.replace( html_text, 'HT_LINK_FULLSIZE', LINK_FULLSIZE )
  html_text = string.replace( html_text, 'HT_END_FULLSIZE', END_FULLSIZE )
  html_text = string.replace( html_text, 'HT_FOOTER', footer )
  html_text = string.replace( html_text, 'HT_COMMENT', COMMENT )
  html_text = string.replace( html_text, 'HT_INDEX', str( index +1 ))
  html_text = string.replace( html_text, 'HT_ENDINDEX', str( lastfile +1 ))  
  htmlfile.write( html_text )
  htmlfile.close( )

def indexisation( indexpage, endindexpage, rows, 
  fileprocessed, startfile, endfile,
  title, footer, metaindex, dirtheme, comments ):

  htmlfilename = 'index_'+str( indexpage )+'.html'

  TITLE = title
  PATH_THEME = dirtheme
  if ( indexpage != 1 ):
    TD_PREVIOUS = HT_TD_PREVIOUS
    LINK_PREVIOUS =  'index_'+str( indexpage-1 )+'.html'
  else:
    TD_PREVIOUS = HT_TD_EMPTY
    LINK_PREVIOUS =  ''
  if ( indexpage != endindexpage ):
    TD_NEXT = HT_TD_NEXT  
    LINK_NEXT = 'index_'+str( indexpage+1 )+'.html'
  else:
    TD_NEXT = HT_TD_EMPTY
    LINK_NEXT = ''
  LINK_INDEX = metaindex

  htmlfile = open( u''+htmlfilename,'w' )
  html_text = string.replace( INDEX_HEADER, 'HT_TD_PREVIOUS', TD_PREVIOUS )
  html_text = string.replace( html_text, 'HT_TD_NEXT', TD_NEXT )
  html_text = string.replace( html_text, 'HT_LANG', langhtml )
  html_text = string.replace( html_text, 'HT_TITLE', TITLE )
  html_text = string.replace( html_text, 'HT_PATH_THEME', PATH_THEME )
  html_text = string.replace( html_text, 'HT_LINK_INDEX', LINK_INDEX )
  html_text = string.replace( html_text, 'HT_LINK_PREVIOUS', LINK_PREVIOUS )
  html_text = string.replace( html_text, 'HT_LINK_NEXT', LINK_NEXT )
  htmlfile.write( html_text )
 
  indexrow = 1 
  indexfile = startfile
  for filepathname in fileprocessed[ startfile:endfile+1 ]:
    if ( indexrow == 1 ):
      htmlfile.write( '\t\t\t\t<tr>\n' )
    filename = os.path.basename( filepathname )
    filebasename = string.split( filename, '.' )[0] 
    LINK_SCALED = sephtml.join( [dirhtml, 'ht_'+filebasename+'.html'] )
    html_text = string.replace( INDEX_THUMB, 'HT_LINK_SCALED', LINK_SCALED )
    LINK_THUMB = sephtml.join( [dirthumb, 'th_'+filename] )
    html_text = string.replace( html_text, 'HT_LINK_THUMB', LINK_THUMB )
    ALT = _("image")+' '+filename
    html_text = string.replace( html_text, 'HT_ALT', ALT )
    COMMENT = findcomment( comments, indexfile, filebasename ) 
    html_text = string.replace( html_text, 'HT_COMMENT', COMMENT )
    htmlfile.write( html_text )
    if ( indexrow == rows ):
      htmlfile.write( '\t\t\t\t</tr>\n' )
      indexrow = 1
    else:
      indexrow = indexrow +1   
    indexfile = indexfile +1       
  if ( indexrow != 1 ):
    htmlfile.write( '\t\t\t\t</tr>\n' )
   
  html_text = string.replace( INDEX_FOOTER, 'HT_TD_PREVIOUS', TD_PREVIOUS )
  html_text = string.replace( html_text, 'HT_TD_NEXT', TD_NEXT )
  html_text = string.replace( html_text, 'HT_PATH_THEME', PATH_THEME )
  html_text = string.replace( html_text, 'HT_INDEX', str( indexpage ) )
  html_text = string.replace( html_text, 'HT_ENDINDEX', str( endindexpage ) )
  html_text = string.replace( html_text, 'HT_LINK_PREVIOUS', LINK_PREVIOUS )
  html_text = string.replace( html_text, 'HT_LINK_NEXT', LINK_NEXT )
  html_text = string.replace( html_text, 'HT_FOOTER', footer )
  htmlfile.write( html_text )
  htmlfile.close( )  

def python_fu_webgallery_xtns( 
  dirname, 
  ext,
  title, 
  footer,
  metaindex,
  dirtheme,
  sizethumb,
  sizescaled,
  sizefullsize,
  slidetime ):
  
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
      dirhtmlpathname = os.path.join( u''+dirname, dirhtml )
      if os.path.exists( dirhtmlpathname ):
        shutil.rmtree( dirhtmlpathname )
      os.mkdir( dirhtmlpathname )
      #
      # Overwrite Title, Meta-Index, Footer with txt files when exists
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
        pdb.gimp_message( _("metaindex.txt not found use metaindex value: %s") %( metaindex )) 
      try:
        footerfile = open( 'footer.txt', 'r' )
        encodedfooter = footerfile.readline( )
        footer = encodedfooter.decode( textencodage ) 
        footerfile.close( ) 
        pdb.gimp_message( _("footer.txt found use encodage: %s") %(textencodage) )                
      except:  
        pdb.gimp_message( _("footer.txt not found use footer value: %s") %( footer )) 
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
        pdb.gimp_message( _("comment.txt not found use individual comment files or filenames"))
      #    
      # Let start serious things  
      pdb.gimp_message( _("File processing is starting, please wait...") )
      fileprocessed = []      
      for filepathname in filepathnames:
        try:
          file = open( u''+filepathname, 'rb' )
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
        # HTML for Index
        rows = int( sizehtmlpage / sizethumb ) -1 # Number of rows
        if ( rows == 0 ) :
          pdb.gimp_message( "Error: scaled size is not enough bigger than thumb size" )
        else:  
          if (( rows == 1 ) or ( rows == 2 )):
            lines = 1
          else:
            lines = rows -2 
          fileperpage = rows * lines  # Number of files per page   
          indexpage = 1 # Index for pages
          endindexpage = int( (len( fileprocessed ) -1 )/ fileperpage )+1
          #DEBUG print 'endindexpage', endindexpage
          lastfile = len( fileprocessed ) -1 # Fix last file
          startfile = 0 # Initialize interval for files/thumb
          endfile = fileperpage -1
          if ( endfile > lastfile ):
            endfile = lastfile
          while ( indexpage <= endindexpage ): # Make each page
            indexisation( indexpage, endindexpage, rows, 
              fileprocessed, startfile, endfile,
              title, footer, metaindex, dirtheme, comments )
            # HTML for each Images
            indexfile = startfile           
            for filepathname in fileprocessed[ startfile:endfile+1 ]:
              filename = os.path.basename(fileprocessed[indexfile]) 
              filebasename = string.split( filename, '.' )[0] #basename without extension
              if ( indexfile != 0 ):
                prevbasename = string.split( os.path.basename(fileprocessed[indexfile-1]), '.')[0]
              else:
                prevbasename = ''
              if ( indexfile != lastfile ):
                nextbasename = string.split( os.path.basename(fileprocessed[indexfile+1]), '.' )[0]
              else:
                nextbasename = ''
              htmlisation( indexpage, indexfile, lastfile,
                filename, filebasename, prevbasename, nextbasename, 
                title, footer, dirtheme, slidetime, comments )
              indexfile = indexfile +1  
            # While loop parameters  
            startfile = endfile +1
            endfile = startfile + fileperpage -1
            if ( endfile > lastfile ):
              endfile = lastfile
            indexpage = indexpage +1
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
  "WebGalleryXtns",
  Photolab_webgallery_description,
  Photolab_webgallery_help,
  "Raymond Ostertag",
  "GPL License",
  "2007-2009",
  _("Web Gallery"),
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
    (PF_INT, "slidetime", _("Time between two slides (s)"), 5),      
  ],
  [],
  python_fu_webgallery_xtns,
  menu="<Image>/Filters"+"/"+_("Photolab")+"/"+_("Gallery"),
  domain=( "gimp20-photolab", locale_directory )         
  )

main()
