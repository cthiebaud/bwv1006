\version "2.25.26"

#(define divisions 384)
#(define quarter (ly:make-moment 1/4))
#(define bar-count-hash (make-hash-table))

BarNumberEngraver =
#(lambda (context)
   (make-engraver
    (acknowledgers
     ((bar-line-interface engraver grob source-engraver)
      (let* ((staff-context (ly:grob-property grob 'staff-symbol-referred))
             (staff-id (if (ly:grob? staff-context)
                           (object-address staff-context)
                           0))
             (current-bar-number 1)
             (moment (ly:context-current-moment context))
             (midiclocks (* divisions (ly:moment-main (ly:moment-div moment quarter)))))

        ;; Get the current bar number or initialize it
        (if (hash-ref bar-count-hash staff-id #f)
            (begin
             (set! current-bar-number (1+ (hash-ref bar-count-hash staff-id)))
             (hash-set! bar-count-hash staff-id current-bar-number))
            (hash-set! bar-count-hash staff-id current-bar-number))

        ;; Add both bar number and MIDI clock as output attributes
        (ly:grob-set-property! grob 'output-attributes
                               (append
                                (ly:grob-property grob 'output-attributes '())
                                (list (cons 'data-bar (number->string current-bar-number))
                                      (cons 'data-midiclock (number->string midiclocks))))))))))
                                            
\layout {
  \context {
    \Score
    %% \override SystemStartBar.collapse-height = #1
  }  
  \context { 
    \Staff 
    \consists \BarNumberEngraver 
    \override BarLine.space-alist.first-note = #'(minimum-space . 0)
    \override BarLine.break-visibility = ##(#f #t #t)
  }
}

\score {
  \new Staff {
    %% \once \override Staff.BarLine.transparent = ##t
    \key d\minor
    \time 3/4
    \bar "|"
    <<   
      \new Voice {
        \voiceOne
        s4  a'4. a'8 |
        e''4 e''4. e''8 |
        f''4 d''4. c''8 |
        bes'4 a' g'16[( f' e' f')] |
        g'16[( e')  f'( d')]
      }
      \new Voice {
        \voiceThree
        s4  f'2 |
        bes'4 a'2 |
        a'4 s2 |
        g'4 f'4 s4 |
        s4
      }
      \new Voice {
        \voiceFour
        s4  s2 |
        g4  g'2 |
        f'4 f'2 |
        s2. |
        s2
      }
      \new Voice {
        \voiceTwo
        s4  d'2 |
        d'4 cis'2 |
        d'4 bes2 |
        g'4 a cis' |
        d'8 s8
      }
    >>
    \bar "|"
  }
}