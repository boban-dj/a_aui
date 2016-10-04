(define (os--split-filename filename)
  (let ((ext (memv #\. (string->list filename))))
    (cons
     (substring filename 0 (- (string-length filename) (length ext)))
     (list->string (cdr ext)))))

(define (os--string-minus str num)
  (substring str 0 (- (string-length str) num)))

(define (os--get-filename image)
  (car (gimp-image-get-filename image)))

(define (os--unretina-save image)
  (let* ((parts (os--split-filename (os--get-filename image)))
         (newname (string-append (os--string-minus (car parts) 3) "."
                                 (cdr parts))))
    (gimp-file-save RUN-NONINTERACTIVE image
                    (car (gimp-image-get-active-drawable image))
                    newname newname)))

;;; Commands

(define (oni-size-scale-50! image)
  (let ((newwidth (/ (car (gimp-image-width image)) 2))
        (newheight (/ (car (gimp-image-height image)) 2)))
    (gimp-image-scale image newwidth newheight))
  (gimp-displays-flush)
  image)

(define (oni-size-scale-30! image)
  (let ((newwidth (/ (car (gimp-image-width image)) 3))
        (newheight (/ (car (gimp-image-height image)) 3)))
    (gimp-image-scale image newwidth newheight))
  (gimp-displays-flush)
  image)

(define (oni-size-unretina image)
  (os--unretina-save (oni-size-scale-50! image)))

(define (oni-size-unretina-all)
  (for-each oni-size-unretina (vector->list (cadr (gimp-image-list)))))

;;; Command registration

(script-fu-register
 "oni-size-scale-50!" "Scale to 50%"
 "Scale the current image down to 50% of its width and height."
 "Tom Willemse <tom@ryuslash.org>" "Tom Willemse" "2014-11-18"
 "RGB*, GRAY*" SF-IMAGE "Image" 0)

(script-fu-register
 "oni-size-scale-30!" "Scale to 33.3%"
 "Scale the current image down to 33.3% of its width and height."
 "Tom Willemse <tom@ryuslash.org>" "Tom Willemse" "2014-11-18"
 "RGB*, GRAY*" SF-IMAGE "Image" 0)

(script-fu-register
 "oni-size-unretina" "Unretina image"
 "Reduce the size of an image and rename for non-retina displays."
 "Tom Willemse <tom@ryuslash.org>" "Tom Willemse" "2014-12-01"
 "RGB*, GRAY*" SF-IMAGE "Image" 0)

(script-fu-register
 "oni-size-unretina-all" "Unretina all images"
 "Call Unretina image on all loaded images."
 "Tom Willemse <tom@ryuslash.org>" "Tom Willemse" "2015-05-18"
 "RGB*, GRAY*" 0)

;;; Menu registration

(script-fu-menu-register "oni-size-scale-50!" "<Image>/Webwork")
(script-fu-menu-register "oni-size-scale-30!" "<Image>/Webwork")
(script-fu-menu-register "oni-size-unretina" "<Image>/Webwork")
(script-fu-menu-register "oni-size-unretina-all" "<Image>/Webwork")
