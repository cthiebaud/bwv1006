\include "defs.ily"

guitarSixtysevenSeventyheight = <<
  \new Voice = "one" {
    \voiceOne
    \override Script.direction = #up
    cis'8  \I-> [          cis'  \A          ] cis' \M  [          cis' \A           ] cis' \M  [          cis' \A           ] | % 67
    cis'   \I-> [          cis'  \A          ] cis' \M  [          cis' \A           ] cis' \M  [          cis' \A           ] | % 68
    cis'   \I-> [          cis'  \A          ] cis' \M  [          cis' \A           ] cis' \M  [          cis' \A           ] | % 69
    d  '   \I-> [          d'    \A          ] d  ' \M  [          d'   \A           ] d  ' \M  [          d'   \A           ] | % 70
    d  '   \I-> [          d'    \A          ] d  ' \M  [          d'   \A           ] d  ' \M  [          d'   \A           ] | % 71
    cis'   \I-> [          cis'  \A          ] cis' \M  [          cis' \A           ] cis' \M  [          cis' \A           ] | % 72
    cis'   \I-> [          cis'  \A          ] cis' \M  [          cis' \A           ] cis' \M  [          cis' \A           ] | % 73
    b      \I-> [          b     \A          ] b    \M  [          b    \A           ] b    \M  [          b    \A           ] | % 74
    b      \I-> [          b     \A          ] b    \M  [          b    \A           ] b    \M  [          b    \A           ] | % 75
    a      \I-> [          a     \A          ] a    \M  [          a    \A           ] a    \M  [          a    \A           ] | % 76
    a      \I-> [          a     \A          ] a    \M  [          a    \A           ] a    \M  [          a    \A           ] | % 77
    gis    \I-> [          gis   \A          ] gis  \M  [          gis  \A           ] gis  \M  [          gis  \A           ] | % 78
  }
  \new Voice = "two" {
    \voiceTwo
    \override Script.direction = #up
    r16        [  a  8  \I          a     \P              a     \I          a     \P              a     \I          a   16  \P ] ~ | % 67
    a          [  a  8  \I          gis \4\P              a     \I          gis \4\P              a     \I          gis 16\4\P ] ~ | % 68
    gis        [  a  8  \I          g   \4\P              a     \I          g   \4\P              a     \I          g   16\4\P ] ~ | % 69
    g          [  a  8  \I          fis \4\P              a     \I          fis \4\P              a     \I          fis 16\4\P ] ~ | % 70
    fis        [  a  8  \I          e   \4\P              a     \I          e   \4\P              a     \I          e   16\4\P ] ~ | % 71
    e          [  a  8  \I          e   \4\P              a     \I          e   \4\P              a     \I          e   16\4\P ] ~ | % 72
    e          [  a  8  \I          d   \5\P              a     \I          d   \5\P              a     \I          d   16\5\P ] ~ | % 73
    d          [  gis8\4\I          d   \5\P              gis \4\I          d   \5\P              gis \4\I          d   16\5\P ] ~ | % 74
    d          [  e  8  \I          cis \5\P              e     \I          cis \5\P              e     \I          cis 16\5\P ] ~ | % 75
    cis        [  e  8  \I          cis \5\P              e     \I          cis \5\P              e     \I          cis 16\5\P ] ~ | % 76
    cis        [  d  8  \I          b  ,\5\P              d     \I          b  ,\5\P              d     \I          b  ,16\5\P ] ~ | % 77
    b  ,       [  d  8  \I          b  ,\5\P              d     \I          b  ,\5\P              d     \I          b  ,16\5\P ]   | % 78
  }
>>

bassSixtysevenSeventyheight = 
%% {
%%    \repeat unfold 12 { R2. |  }   % 67-78
%% }
<<
  \new Voice = "one" {
    \voiceTwo
      < a  ,   e       a       >4  s2 |
      < e      a       cis'    >4  s2 |
      < e      cis'    e  '    >4  s2 |
      < fis    a       d  '    >4  s2 |
      < e      a       d  '    >4  s2 |
      < e      a       cis'    >4  s2 |
      < d      fis     cis'    >4  s2 |
      < d      gis     b       >4  s2 |
      < cis    e       b       >4  s2 |
      < cis    e       a       >4  s2 |
      < b  ,   d       a       >4  s2 |
      < b  ,   d       gis     >4  s2 |
  }
  \new Voice = "two" {
    \voiceOne
    %% \repeat unfold 12 { R2. |  }   % 67-78
    \repeat unfold 12 { r8 a, [ a, a, a, a, ] |  }   % 67-78
  }
>>    