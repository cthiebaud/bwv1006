% highlight-bars.ily
% Auto-highlight each measure with a cycling color.
% Includes special handling for pickup measures (\partial)

Auto_measure_highlight_engraver =
#(lambda (context)
   (let ((last-bar -1)
         (colors '("lightblue" "lightgreen" "lightyellow" "lightpink")))
     (make-engraver
      ((process-music engraver)


       (let* ((raw-bar     (ly:context-property context 'currentBarNumber 0))
              (pos         (ly:context-property context 'measurePosition (ly:make-moment 0)))
              ;; Treat negative measure positions (pickup) as bar 0
              (current-bar (if (negative? (ly:moment-main-numerator pos)) 0 raw-bar)))

         ;; Debug: print bar status
         ;; (display
         ;;   (format #f ">>> raw = ~a, moment = ~a, numerator = ~a~%"
         ;;           raw-bar pos (ly:moment-main-numerator pos)))
         ;; (display (format #f ">>> Tick: raw = ~a, effective = ~a, pos = ~a, last = ~a~%"
         ;;                  raw-bar current-bar pos last-bar))

         (when (> current-bar last-bar)
           ;; (newline)
           (let* ((color (list-ref colors (modulo current-bar (length colors))))
                  (start (ly:make-stream-event
                          (ly:make-event-class 'staff-highlight-event)
                          (list (cons 'span-direction START)
                                (cons 'color color)
                                (cons 'bar-number current-bar)))))
             ;; (display (format #f ">>> Highlighting bar ~a with ~a" current-bar color))
             (ly:broadcast (ly:context-event-source context) start))
           (set! last-bar current-bar)))))))

#(define (debug-print-grob-properties grob)
   (let ((props '(name cause stencil color span-direction
                       direction after-line-breaking
                       output-attributes extent bar-number)))
     (display ">>>> grob debug dump:\n")
     (for-each
      (lambda (key)
        (let ((val (ly:grob-property grob key #f)))
          (when val
            (display (format #f "    ~a = ~a\n" key val)))))
      props)))


#(define (add-data-bar-to-highlight grob)
   (let* ((ev     (ly:grob-property grob 'cause))
          (clazz  (and ev (ly:event-property ev 'class)))
          (bar-num (and ev (ly:event-property ev 'bar-number))))
     (display
      (format #f ">>>> event class: ~a, bar-num: ~a~%"
              clazz
              (if (number? bar-num) bar-num "NOT A NUMBER")))
     (when (and (list? clazz)
                (member 'staff-highlight-event clazz)
                (number? bar-num))
       (ly:grob-set-property! grob 'output-attributes
                              (list (cons "data-bar" (number->string bar-num)))))
     '()))
