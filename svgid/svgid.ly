\version "2.25.26"

#(define bar-count-hash (make-hash-table 10))

#(define (add-bar-number-to-barline grob)
   (let* ((staff-context (ly:grob-property grob 'staff-symbol-referred))
          (staff-id (if (ly:grob? staff-context)
                        (object-address staff-context)
                        0))
          (current-bar-number 1))
     
     ;; Get the current bar number or initialize it
     (if (hash-ref bar-count-hash staff-id #f)
         (begin
           (set! current-bar-number (1+ (hash-ref bar-count-hash staff-id)))
           (hash-set! bar-count-hash staff-id current-bar-number))
         (hash-set! bar-count-hash staff-id current-bar-number))
     
     ;; Add the bar number as an output attribute
     (ly:grob-set-property! grob 'output-attributes
                            (append
                             (ly:grob-property grob 'output-attributes '())
                             (list (cons 'data-bar (number->string current-bar-number)))))))

addBarNumberAttributes = {
  \override Score.BarLine.before-line-breaking = #add-bar-number-to-barline
}

\score {
  \new Staff \with {
    \addBarNumberAttributes
  } {
    \key d\minor
    \time 3/4
    \override Score.BarNumber.break-visibility = ##(#t #t #t)
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    <<
      \new Voice {
        \voiceOne
        \partial 2 a'4. a'8 |
        e''4 e''4. e''8 |
        f''4 d''4. c''8 |
        bes'4 a' g'16[( f' e' f')] |
        g'16[( e')  f'( d')]
      }
      \new Voice {
        \voiceThree
        \partial 2 f'2 |
        bes'4 a'2 |
        a'4 s2 |
        g'4 f'4 s4 |
        s4
      }
      \new Voice {
        \voiceFour
        \partial 2 s2 |
        g4  g'2 |
        f'4 f'2 |
        s2. |
        s2
      }
      \new Voice {
        \voiceTwo
        \partial 2 d'2 |
        d'4 cis'2 |
        d'4 bes2 |
        g'4 a cis' |
        d'8 s8
      }
    >>
    
  }
  }


