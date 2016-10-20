#!/usr/bin/python2

# - Brian Parma -
#  Demonstrate SVG scaling with rsvg vs. gtk.gdk.Pixbuf

import sys
#import cairo
import rsvg
import gtk

class SVGCompare(gtk.Window):
    def __init__(self, svg):
        gtk.Window.__init__(self)
        pix = svg.get_pixbuf()
        self.w = svg.props.width
        self.h = svg.props.height
        self.ratio = self.w/self.h
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0
        self.sx, self.sy = 1, 1
        self.ds = 0.1
        self.interp = 1
        self.interp_text = ['Nearest neighbor sampling',
                            'Tiles',
                            'Bilinear',
                            'Hyperbolic']
        
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | 
                    gtk.gdk.POINTER_MOTION_MASK |
                    gtk.gdk.POINTER_MOTION_HINT_MASK |
                    gtk.gdk.SCROLL_MASK |
                    gtk.gdk.LEAVE_NOTIFY_MASK)

        if (self.ratio < 1):
            horizontal = True
            box = gtk.HBox()
            self.set_default_size(svg.props.width*2, svg.props.height)
        else:
            horizontal = False
            box = gtk.VBox()
            self.set_default_size(svg.props.width, svg.props.height*2)
            
        self.add(box)
        
        svg_da = gtk.DrawingArea()
     #   pix_da = gtk.DrawingArea()
        f = gtk.Frame()
        f.add(svg_da)
        box.add(f)
     #   f = gtk.Frame()
     #   f.add(pix_da)
     #   box.add(f)
        
        self.connect('delete-event',gtk.main_quit)
    #    win.connect('expose-event',win_expose, svg)
        self.connect('button-press-event',self.butt_event)
        self.connect('scroll-event',self.scroll_event)
        self.connect('key-press-event',self.key_event)
        self.connect('motion-notify-event',self.move_event)
        svg_da.connect('expose-event', self.svg_expose, svg)
#        pix_da.connect('expose-event', self.pix_expose, pix)
        
        self.show_all()
        
    def key_event(self, widget, event):
        #print 'key',event.keyval
        if event.keyval in [gtk.keysyms.plus, gtk.keysyms.equal,
                            gtk.keysyms.KP_Add]:
            self.sx += self.ds
            self.sy += self.ds
            self.queue_draw()
        elif event.keyval in [gtk.keysyms.minus, gtk.keysyms.KP_Subtract]:
            self.sx -= self.ds
            self.sy -= self.ds
            self.queue_draw()
        elif event.keyval in [gtk.keysyms.i, gtk.keysyms.I]:
            self.interp = (self.interp + 1) % 4
            print 'Switching interpolation method to: %s ' % self.interp_text[self.interp]
            self.queue_draw()
        
    
    def butt_event(self, widget, event):
        print 'butt',event.button
        if event.button == 1:
            self.x, self.y = event.x, event.y
        elif event.button == 4:
            self.sx += self.ds
            self.sy += self.ds
            self.queue_draw()
        elif event.button == 5:
            self.sx -= self.ds
            self.sy -= self.ds
            self.queue_draw()
            
    def scroll_event(self, widget, event):
        if event.direction == gtk.gdk.SCROLL_UP:
            self.sx += self.ds
            self.sy += self.ds
            self.queue_draw()
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            self.sx -= self.ds
            self.sy -= self.ds
            self.queue_draw()
        
    def move_event(self, widget, event):
        #print 'move',int(event.state),int(gtk.gdk.BUTTON1_MASK)
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x, y, state = event.x, event.y, event.state
            
        if event.state & gtk.gdk.BUTTON1_MASK:
            self.dx += x - self.x
            self.dy += y - self.y
            self.x, self.y = x, y
            print self.dx, self.dy
            self.queue_draw()
        
    def svg_expose(self, da, event, svg):
        x, y, w, h = da.allocation
        if svg is not None:
            ctx = da.window.cairo_create()
            
            ctx.translate(self.dx,self.dy)  # Translate
            ctx.scale(self.sx,self.sy)      # Scale
            
            svg.render_cairo(ctx)
        
        return True

    def pix_expose(self, da, event, pix):
        
        interp = [gtk.gdk.INTERP_NEAREST,
                  gtk.gdk.INTERP_TILES,
                  gtk.gdk.INTERP_BILINEAR,
                  gtk.gdk.INTERP_HYPER]
                  
        # one way to scale
        mod_pix = pix.scale_simple(self.w*self.sx, self.h*self.sy, interp[self.interp])
                  
        if pix is not None:
#            ctx = da.window.cairo_create()

#            ctx.translate(self.dx,self.dy)  # Translate
#            ctx.scale(self.sx,self.sy)      # another way to scale

#            ctx.set_source_pixbuf(mod_pix, 0, 0)
#            ctx.paint()
            da.window.draw_pixbuf(None,mod_pix,0,0,self.dx,self.dy)
        
        return True

#def test_event(widget, event):
    ##print 'event!',int(event.type),int(event.state),event.is_hint,int(gtk.gdk.BUTTON1_MASK)
    #if event.is_hint:
        #x, y, state = event.window.get_pointer()
        #print 'hint',x,y,int(state),event.x,event.y,int(event.state)
    #if not event.is_hint:
        #print 'no hint',event.x,event.y,int(event.state)
    

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print sys.argv[0]+':','usage:',sys.argv[0],'<filename>'
    else:
        try:
            svgc = SVGCompare(rsvg.Handle(sys.argv[1]))
            gtk.main()
        except KeyboardInterrupt:
            gtk.main_quit()
