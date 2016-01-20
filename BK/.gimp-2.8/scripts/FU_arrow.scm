; FU_arrow.scm
; version 2.8 [gimphelp.org]
; last modified/tested by Paul Sherman
; 02/04/2014 on GIMP-2.8.10
;
;==============================================================
;
; Installation:
; This script should be placed in the user or system-wide script folder.
;
;	Windows Vista/7/8)
;	C:\Program Files\GIMP 2\share\gimp\2.0\scripts
;	or
;	C:\Users\YOUR-NAME\.gimp-2.8\scripts
;	
;	Windows XP
;	C:\Program Files\GIMP 2\share\gimp\2.0\scripts
;	or
;	C:\Documents and Settings\yourname\.gimp-2.8\scripts   
;    
;	Linux
;	/home/yourname/.gimp-2.8/scripts  
;	or
;	Linux system-wide
;	/usr/share/gimp/2.0/scripts
;
;==============================================================
;
; LICENSE
;
;    This program is free software: you can redistribute it and/or modify
;    it under the terms of the GNU General Public License as published by
;    the Free Software Foundation, either version 3 of the License, or
;    (at your option) any later version.
;
;    This program is distributed in the hope that it will be useful,
;    but WITHOUT ANY WARRANTY; without even the implied warranty of
;    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;    GNU General Public License for more details.
;
;    You should have received a copy of the GNU General Public License
;    along with this program.  If not, see <http://www.gnu.org/licenses/>.
;
;==============================================================
; Original information 
; Berengar W. Lehr (Berengar.Lehr@gmx.de)
; Medical Physics Group, Department of Diagnostic and Interventional Radiology
; Jena University Hospital, 07743 Jena, Thueringen, Germany
; ================================================================================
;
(define pi (* 4 (atan 1.0)))

(define 
    (FU-help-1Arrow
        inPointToX
        inPointToY
        inPointFromX
        inPointFromY
        theWingLength
        WingAngle
        drawable
        image
        FullHead
        MiddlePoint
    )
    (let*
        (
        ; calculate absolute angle of both wings in image from relative angle 
        ; between wings and arrow-tail and absolut angle of arrow-tail
        (theArrowAngle (if (= (- inPointToY inPointFromY) 0)
            (/ pi (if (< (- inPointToX inPointFromX) 0) 2 -2))
            (+ (atan (/ (- inPointToX inPointFromX) (- inPointToY inPointFromY))) (if (> inPointToY inPointFromY) pi 0))
        ))
        (theLeftAngle  (+ theArrowAngle WingAngle))
        (theRightAngle (- theArrowAngle WingAngle))

        ; calculate end points of both wings
        (theLeftWingEndPointX  (+ inPointToX (* theWingLength (sin theLeftAngle))))
        (theLeftWingEndPointY  (+ inPointToY (* theWingLength (cos theLeftAngle))))
        (theRightWingEndPointX (+ inPointToX (* theWingLength (sin theRightAngle))))
        (theRightWingEndPointY (+ inPointToY (* theWingLength (cos theRightAngle))))

        (points          (cons-array 4 'double))
        (theMiddleWingEndPointX 0)    (theMiddleWingEndPointY 0)
		(PreviousOpacity 100.0)
        )
        (begin
		(set! PreviousOpacity (car (gimp-context-get-opacity)))
		(gimp-context-set-opacity 100.0)
        ; collect points for arrow-tail and draw them
        (aset points 0 inPointToX)               (aset points 1 inPointToY)
        (aset points 2 inPointFromX)             (aset points 3 inPointFromY)
        (gimp-paintbrush-default drawable 4 points) (set! points (cons-array 4 'double))
        ; accordingly for left wing
        (aset points 0 inPointToX)               (aset points 1 inPointToY)
        (aset points 2 theLeftWingEndPointX)     (aset points 3 theLeftWingEndPointY)
        (gimp-paintbrush-default drawable 4 points) (set! points (cons-array 4 'double))
        ; accordingly for right wing
        (aset points 0 inPointToX)               (aset points 1 inPointToY)
        (aset points 2 theRightWingEndPointX)    (aset points 3 theRightWingEndPointY)
        (gimp-paintbrush-default drawable 4 points)

        ; only if head is to be filled
        (if (= FullHead 1) (begin
            ; calculate intersection of connection between the wings end points and arrow tail
            ; shrink distance between this point and arrow head if MiddlePoint < 100
            (set! theMiddleWingEndPointX (+ inPointToX 
                                            (* (/ MiddlePoint 100) (- (/ (+ theLeftWingEndPointX theRightWingEndPointX) 2) inPointToX))
                                         ))
            (set! theMiddleWingEndPointY (+ inPointToY
                                            (* (/ MiddlePoint 100) (- (/ (+ theLeftWingEndPointY theRightWingEndPointY) 2) inPointToY))
                                         ))

            ; collect points for left wing end - intersection - right wing end & draw it
            (set! points (cons-array 6 'double))
            (aset points 0 theLeftWingEndPointX)      (aset points 1 theLeftWingEndPointY)
            (aset points 2 theMiddleWingEndPointX)    (aset points 3 theMiddleWingEndPointY)
            (aset points 4 theRightWingEndPointX)     (aset points 5 theRightWingEndPointY)
            (gimp-paintbrush-default drawable 6 points)

            ; collect points to create selection which will be filled with FG color
            (set! points (cons-array 8 'double))
            (aset points 0 inPointToX)                (aset points 1 inPointToY)
            (aset points 2 theLeftWingEndPointX)      (aset points 3 theLeftWingEndPointY)
            (aset points 4 theMiddleWingEndPointX)    (aset points 5 theMiddleWingEndPointY)
            (aset points 6 theRightWingEndPointX) (aset points 7 theRightWingEndPointY)
            ;(gimp-free-select image 8 points CHANNEL-OP-REPLACE TRUE FALSE 0)
			(gimp-image-select-polygon image CHANNEL-OP-REPLACE 8 points)
            (gimp-edit-bucket-fill drawable FG-BUCKET-FILL NORMAL-MODE 100 0 FALSE 0 0)
            (gimp-selection-none image)
        ))
		(gimp-context-set-opacity PreviousOpacity)
        ) ; begin
    ) ; let
) ; define

(define
    (FU-arrow
        image drawable
        WingLengthRatio
        WingAngle
        FullHead
        MiddlePoint
        BrushThicknessOrRatio
        ; LineThicknessRatio
        ; BrushThickness
        useFirstPointArrowAsHead
        usePathThenRemove
        useNewLayer
        useDoubleHeadArrow
        useless
    )
    (let*
        (
        (theActiveVector (car   (gimp-image-get-active-vectors image)))
        (theFirstStroke  0)          (theStrokePoints 0)
        (theNumPoints    0)
        (inPoint_1X      0)          (inPoint_1Y      0)
        (inPoint_2X      0)          (inPoint_2Y      0)

        (theArrowLength 0)            (theWingLength 0)
        (oldLayer (car (gimp-image-get-active-layer image)))

        (brushName    "arrowBrush")
        (oldBrushName (car (gimp-context-get-brush)))
        )

        (if (not (= theActiveVector -1)) (begin
            (gimp-image-undo-group-start image)

            ; create new layer if asked to do so
            (if (= useNewLayer 1) (begin
                (set! drawable (car (gimp-layer-new image (car (gimp-image-width     image))
                                                          (car (gimp-image-height    image))
                                                          (+ 1 (* 2 (car (gimp-image-base-type image))))
                                                          "Arrow" 100 NORMAL-MODE )))
                (gimp-image-insert-layer image drawable 0 0)
                ; set new layer completely transparent
                (gimp-layer-add-mask drawable (car (gimp-layer-create-mask drawable ADD-BLACK-MASK)))
                (gimp-layer-remove-mask drawable MASK-APPLY)
            ))

            ; get path/vector points
            (set! theFirstStroke  (aref  (cadr (gimp-vectors-get-strokes theActiveVector)) 0))
            (set! theStrokePoints (caddr (gimp-vectors-stroke-get-points theActiveVector theFirstStroke)))
            (set! theNumPoints    (cadr  (gimp-vectors-stroke-get-points theActiveVector theFirstStroke)))

            ; get position of arrow head and arrow tail from active vector
            (set! inPoint_1X    (aref theStrokePoints 2))
            (set! inPoint_1Y    (aref theStrokePoints 3))
            (set! inPoint_2X    (aref theStrokePoints (- theNumPoints 4)))
            (set! inPoint_2Y    (aref theStrokePoints (- theNumPoints 3)))
            
            ; calculate length of arrows depending on the length of the whole arrow
            (define (sqr x) (* x x))
            (set! theArrowLength (exp (* 0.5 (log (+ (sqr (- inPoint_1X inPoint_2X)) (sqr (- inPoint_1Y inPoint_2Y)))))))
            (if (< WingLengthRatio 0)
            	(set! theWingLength (* theArrowLength (/ -1 WingLengthRatio)))
            	(set! theWingLength WingLengthRatio)
            )

            ; define new brush for drawing operation
            (gimp-brush-new brushName)
            (gimp-brush-set-shape brushName BRUSH-GENERATED-CIRCLE)    (gimp-brush-set-spikes brushName 2)
            (gimp-brush-set-hardness brushName 1.00)                   (gimp-brush-set-aspect-ratio brushName 1.0)
            (gimp-brush-set-angle brushName 0.0)                       (gimp-brush-set-spacing brushName 1.0)

            ; set radius of brush according to length of arrow
            (if (< BrushThicknessOrRatio 0)
                (gimp-brush-set-radius brushName (/ theArrowLength (* BrushThicknessOrRatio -1)))
                (gimp-brush-set-radius brushName BrushThicknessOrRatio)
            )
            (gimp-context-set-brush brushName)

            (if (or (= useFirstPointArrowAsHead 1) (= useDoubleHeadArrow 1))
                (FU-help-1Arrow inPoint_1X inPoint_1Y inPoint_2X inPoint_2Y theWingLength (* (/ WingAngle 180) pi) drawable image FullHead MiddlePoint))
            (if (or (= useFirstPointArrowAsHead 0) (= useDoubleHeadArrow 1))
                (FU-help-1Arrow inPoint_2X inPoint_2Y inPoint_1X inPoint_1Y theWingLength (* (/ WingAngle 180) pi) drawable image FullHead MiddlePoint))

            (gimp-context-set-brush oldBrushName)
            (gimp-brush-delete brushName)

            (if (= usePathThenRemove 1) (gimp-image-remove-vectors image theActiveVector))

            (if (= useNewLayer 1) (begin
                (plug-in-autocrop-layer TRUE image drawable)
                (gimp-image-set-active-layer image oldLayer)
            ))
            (gimp-displays-flush)
            (gimp-image-undo-group-end image)
        )(gimp-message "This script needs a path with two points\nto position the arrow head and tail (first and last point of path is used)"))
    ) ; let*
); define

; Register the function with GIMP:

(script-fu-register "FU-arrow"
   "<Image>/Script-Fu/Arrow"
   " Draw an arrow in your image\n\nCreate a path (2 points) before running the script...\nArrow will be created in a separate layer."
   "Berengar W. Lehr <B-Ranger@web.de>"
   "2009, Berengar W. Lehr / MPG@IDIR, UH Jena, Germany."
   "19th November 2009"
   "*"
   SF-IMAGE       "The image"   0
   SF-DRAWABLE    "The drawable"   0
   SF-ADJUSTMENT  "Length of wings * " '(-2.5 -100 500 10 1 1 1)
   SF-ADJUSTMENT  "Angle between arrow and wing in degree" '(25 5 85 5 15 0 0)
   SF-TOGGLE      "\nFill head of arrow?\n" TRUE
   SF-ADJUSTMENT  "Percentage size of notch of arrow head\n(only valid if head of arrow is filled)" '(75 0 100 1 10 0 1)
   SF-ADJUSTMENT  "Brush Thickness * " '(-25 -500 500 1 10 0 1)
   SF-TOGGLE      "\nUse first path point as arrow head?\n(if not the last path point of is used as arrow head)" TRUE
   SF-TOGGLE      "\nDelete path after arrow was drawn?\n" FALSE
   SF-TOGGLE      "Use new layer for arrow?" TRUE
   SF-TOGGLE      "\nDraw double headed arrow?\n" FALSE
   SF-STRING      "\n\n*  POSITIVE values\n    stand for absolute pixel size.\n    NEGATIVE for values\n    relative to length of arrow" "Create a path first!"
)

