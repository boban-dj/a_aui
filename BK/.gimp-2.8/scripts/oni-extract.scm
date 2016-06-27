(define (oni-extract-icon! image)
  (let* ((x (- (/ (car (gimp-image-width image)) 2) 16))
         (y (- (/ (car (gimp-image-height image)) 2) 16)))
    (gimp-image-crop image 32 32 x y)
    (gimp-image-flatten image)
    (gimp-displays-flush)))

(script-fu-register
 "oni-extract-icon!" "Extract a 32x32 icon"
 "Crop the current image to a 32x32 pixels icon focused in the center
of the image."
 "Tom Willemse <tom@ryuslash.org>" "Tom Willemse" "2015-05-18"
 "RGB*, GRAY*" SF-IMAGE "Image" 0)

(script-fu-menu-register "oni-extract-icon!" "<Image>/Webwork")
