\version "2.25.26"

\include "highlight-bars.ily"
\include "bwv1006_ly_main.ly"

#(set-global-staff-size 18) % Slightly smaller staff

% Define a helper to detect SVG mode
#(define is-svg?
   (equal? (ly:get-option 'backend) 'svg))

#(if (not is-svg?)
     (set-global-staff-size 16))   

% Define invisible line-break-only voice (adapt to your bar structure)

breakEvery = #(define-music-function (count bars-per-line) (integer? integer?)
  #{
    \repeat unfold #count {
      \repeat unfold #bars-per-line { s2. | }
      \break
    }
  #})

layoutBreaks = {
  \breakEvery 1  2  % 2
  \breakEvery 1  4  % 6
  \breakEvery 1  2  % 8
  \breakEvery 6  4  % 32
  \breakEvery 2  3  % 38
  \breakEvery 11 4  % 82
  \breakEvery 1  3  % 85
  \breakEvery 1  4  % 89
  \breakEvery 1  3  % 92
  \breakEvery 1  6  % 98
  \breakEvery 2  3  % 104
  \breakEvery 2  4  % 112
  \breakEvery 1  6  % 118
  \breakEvery 1  4  % 122
  \breakEvery 1  3  % 125
  \breakEvery 1  4  % 129
  \breakEvery 1  4  % 133
  \breakEvery 1  5  % 138
}

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
      % Conditionally include break logic in SVG only
      %% #(if is-svg?
      %%   #{ 
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
      %%   #}
      %%   #{ <> #})
    >>
    \layout {
      \context {
        \Voice
        \override StringNumber.stencil = ##f
      }
      \context {
        \Staff
        \consists \Auto_measure_highlight_engraver
        \consists Staff_highlight_engraver
        \override StaffHighlight.after-line-breaking = #add-data-bar-to-highlight
      }      
    }
  }
}
