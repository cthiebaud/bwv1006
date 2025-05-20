\version "2.25.26"

\include "bwv1006_ly_main.ly"

% Formatted one-pager for display
\book {
  \bookOutputName "bwv1006"
  \paper {
    indent = 0
    page-breaking =
    #(if (equal? (ly:get-option 'backend) 'svg)
      ly:one-page-breaking
      ly:page-turn-breaking) % fallback for other backends
  }

  \score {
    \bwvOneThousandSixScore
    \layout {
      \context {
        \Voice
        \override StringNumber.stencil = ##f
      }
    }
  }
}
