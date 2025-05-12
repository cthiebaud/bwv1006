\version "2.24.0"

\paper {
  output-format = "svg"
  indent = 0
  tagline = ##f              % ← disables LilyPond footer
  ragged-right = ##t
  ragged-last = ##t
  line-width = 999\mm  % very wide
  page-breaking = #ly:one-line-breaking
  top-margin = 0
  bottom-margin = 0
  left-margin = 0
  right-margin = 0  

  % Reduce vertical space
  system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 0) (stretchability . 0))
  score-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 0) (stretchability . 0))

  % Limit page height (adjust as needed)
  paper-height = 40\mm  % ← Tighten height here  
}

\layout {
  \context {
    \Score
    \remove "Bar_number_engraver"
  }
  \context {
    \Voice
    \override StringNumber.stencil = ##f
  }
}

% Load the music from m001_008.ly
\include "_1/m001_008.ly"

\score {
\new Staff {
    \clef "treble_8"
    \key e \major
    \time 3/4
    \guitarOneHeight  % Assuming m001_008.ly defines music = { ... }
  }
}
