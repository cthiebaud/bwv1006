\version "2.25.26"

\include "bwv1006_ly_main.ly"
\include "tie-attributes.ily"

% One-line score for notehead extraction
\book {
  \paper {
    indent = 0
    line-width = 20000\mm       % absurdly wide
    page-breaking = #ly:one-line-breaking
    systems-per-page = 1
    print-page-number = ##f
  }

  \score {
    \bwvOneThousandSixScoreNoTabs
    \layout {
      \context {
        \Voice
        \override StringNumber.stencil = ##f
      }
      \context {
        \Voice
        \consists \Tie_grob_engraver
      }
    }
    \midi {}
  }
}