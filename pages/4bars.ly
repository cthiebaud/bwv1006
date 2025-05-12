\version "2.24.0"

\paper {
  output-format = "svg"
  indent = 0
  tagline = ##f              % ← disables LilyPond footer
  ragged-right = ##t
  ragged-last = ##t
  line-width = 999\mm  % very wide
  page-breaking = #ly:one-line-breaking
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
