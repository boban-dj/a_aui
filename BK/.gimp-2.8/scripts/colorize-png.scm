; colorize all PNG files in current directory, original file will be overwritten!
; save this script as ~/.gimp-2.8/scripts/colorize-png.scm
; from the directory with the PNG files run:
; gimp -i -b '(colorize-png "*.png" <hue> <saturation> <lightness>)' -b '(gimp-quit 0)'
; example green-blue hue: gimp -i -b '(colorize-png "*.png" 180 50 0)' -b '(gimp-quit 0)'

(define (colorize-png pattern hue saturation lightness)
    (let* ((filelist (cadr (file-glob pattern 1))))     
        (while (not (null? filelist))
           (let* ((filename (car filelist))
              (image (car (file-png-load 1 filename filename)))
              (drawable (car (gimp-image-active-drawable image))))
              (gimp-colorize drawable hue saturation lightness)
              (gimp-file-save RUN-NONINTERACTIVE image drawable filename filename)
              (gimp-image-delete image))
           (set! filelist (cdr filelist))   
        )   
    )
)