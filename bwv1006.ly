\version "2.25.26"

\include "highlight-bars.ily"
\include "bwv1006_ly_main.ly"

#(set-global-staff-size 18) % Slightly smaller staff

% Define a helper to detect SVG mode
#(define is-svg?
   (equal? (ly:get-option 'backend) 'svg))

#(if (not is-svg?)
     (set-global-staff-size 16))   

breakEvery = #(define-music-function (count bars-per-line) (integer? integer?)
  #{
    \repeat unfold #count {
      \repeat unfold #bars-per-line { s2. | }
      \break
    }
  #})     

% Common break structure - list of (count bars-per-line) pairs
#(define break-structure
   (list (list 1  2)
         (list 1  4)
         (list 1  2)
         (list 6  4)
         (list 2  3)
         (list 11 4)
         (list 1  3)
         (list 1  4)
         (list 1  3)
         (list 1  6)
         (list 2  3)
         (list 2  4)
         (list 1  6)
         (list 1  4)
         (list 1  3)
         (list 1  4)
         (list 1  4)
         (list 1  5)))

% Generate layoutBreaks from the structure
#(define (generate-layout-breaks structure)
   (let ((music-list (list)))
     (for-each
      (lambda (break-item)
        (let ((count (car break-item))
              (bars-per-line (cadr break-item)))
          (set! music-list 
                (append music-list 
                        (list #{
                          \breakEvery #count #bars-per-line
                        #})))))
      structure)
     (make-sequential-music music-list)))

% Generate the layoutBreaks using our structure
layoutBreaks = #(generate-layout-breaks break-structure)

% Generate line-starting bars from the structure  
#(define (calculate-line-starts structure)
   (let ((line-starts (list 1))  ; Start with bar 1
         (current-bar 1))
     
     ;; Process each break item
     (for-each
      (lambda (break-item)
        (let ((count (car break-item))
              (bars-per-line (cadr break-item)))
          ;; For each line in this break-item
          (do ((line-num 0 (+ line-num 1)))
              ((>= line-num count))
            ;; Move to the start of the next line
            (set! current-bar (+ current-bar bars-per-line))
            ;; Add this as a line start
            (set! line-starts (cons current-bar line-starts)))))
      structure)
     
     ;; Sort and return (keep all but the very last calculated bar)
     (let ((sorted-list (sort line-starts <)))
       (reverse (cdr (reverse sorted-list))))))

% Debug: Print the calculated line starts
#(display (format #f "Line starting bars: ~a~%" (calculate-line-starts break-structure)))

% Generate the line-starting bars list
#(define line-starting-bars (calculate-line-starts break-structure))

% Define the condition function using the calculated line starts
#(define (highlight-line-breaks bar-num colors-list)
   (if (member bar-num line-starting-bars) 
       0
       1))

% The highlighting will be applied in the \layout block of the score

% Debug: Print the calculated line starts (uncomment to see)
% #(display (format #f "Line starting bars: ~a~%" line-starting-bars))

% Formatted one-pager for display
\book {
  \bookOutputName "bwv1006"
  \paper {
    indent = 0
    page-breaking = #(if is-svg?
                         ly:one-page-breaking
                         ly:page-turn-breaking)

    line-width = #(if is-svg?
                      (* 260 mm)
                      (* 160 mm))

    paper-width = #(if is-svg?
                       (* 270 mm)
                       (* 210 mm))
  }

  \score {
    <<
      \bwvOneThousandSixScore
      % Include break logic
      \new Staff \with {
        \remove "Staff_symbol_engraver"
        \remove "Clef_engraver"
        \remove "Time_signature_engraver"
        \remove "Bar_engraver"
        \override VerticalAxisGroup.staff-staff-spacing = #'((basic-distance . 0))
        \override StaffSymbol.line-count = #0
      } 
      <<
        \new Voice \with {
          \remove "Note_heads_engraver"
          \remove "Rest_engraver"
          \remove "Stem_engraver"
          \remove "Beam_engraver"
          \remove "Tuplet_engraver"
        } \layoutBreaks
      >>
    >>
    \layout {
      \override NoteHead.font-size = #2
      \context {
        \Voice
        \override StringNumber.stencil = ##f
      }
      % Apply highlighting only for SVG output
      #(if (equal? (ly:get-option 'backend) 'svg)
           (ly:parser-include-string 
             "\\context {
               \\Staff
               \\consists #(make-conditional-highlight-engraver 
                            '(\"gainsboro\" \"whitesmoke\") 
                            highlight-line-breaks)
               \\consists Staff_highlight_engraver
             }
             \\context {
               \\Score
               \\override StaffHighlight.after-line-breaking = #add-data-bar-to-highlight
             }")
           )
    }
  }
}