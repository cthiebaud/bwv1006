\include "defs.ly"

guitarSixtysevenSeventyheight = {
    \override Script.direction = #up
    cis'16 \I-> [ a     \I cis'  \A a     \P ] cis' \M  [ a     \I cis' \A  a     \P ] cis' \M  [ a     \I cis' \A  a     \P ] | % 67
    cis'   \I-> [ a     \I cis'  \A gis \4\P ] cis' \M  [ a     \I cis' \A  gis \4\P ] cis' \M  [ a     \I cis' \A  gis \4\P ] | % 68
    cis'   \I-> [ a     \I cis'  \A g   \4\P ] cis' \M  [ a     \I cis' \A  g   \4\P ] cis' \M  [ a     \I cis' \A  g   \4\P ] | % 69
    d  '   \I-> [ a     \I d'    \A fis \4\P ] d  ' \M  [ a     \I d'   \A  fis \4\P ] d  ' \M  [ a     \I d'   \A  fis \4\P ] | % 70
    d  '   \I-> [ a     \I d'    \A e   \4\P ] d  ' \M  [ a     \I d'   \A  e   \4\P ] d  ' \M  [ a     \I d'   \A  e   \4\P ] | % 71
    cis'   \I-> [ a     \I cis'  \A e   \4\P ] cis' \M  [ a     \I cis' \A  e   \4\P ] cis' \M  [ a     \I cis' \A  e   \4\P ] | % 72
    cis'   \I-> [ a     \I cis'  \A d   \5\P ] cis' \M  [ a     \I cis' \A  d   \5\P ] cis' \M  [ a     \I cis' \A  d   \5\P ] | % 73
    b      \I-> [ gis \4\I b     \A d   \5\P ] b    \M  [ gis \4\I b    \A  d   \5\P ] b    \M  [ gis \4\I b    \A  d   \5\P ] | % 74
    b      \I-> [ e     \I b     \A cis \5\P ] b    \M  [ e     \I b    \A  cis \5\P ] b    \M  [ e     \I b    \A  cis \5\P ] | % 75
    a      \I-> [ e     \I a     \A cis \5\P ] a    \M  [ e     \I a    \A  cis \5\P ] a    \M  [ e     \I a    \A  cis \5\P ] | % 76
    a      \I-> [ d     \I a     \A b  ,\5\P ] a    \M  [ d     \I a    \A  b  ,\5\P ] a    \M  [ d     \I a    \A  b  ,\5\P ] | % 77
    gis    \I-> [ d     \I gis   \A b  ,\5\P ] gis  \M  [ d     \I gis  \A  b  ,\5\P ] gis  \M  [ d     \I gis  \A  b  ,\5\P ] | % 78
}             

bassSixtysevenSeventyheight = {
    %% \repeat unfold 12 { \stemUp r8 a, a, (a, a, a,) | }        | % 67-78
    %% \repeat unfold 12 { \stemUp a,4  r2 | }        | % 67-78
    \stemUp
    r8  a,  a,  a,  a,  a, |    % 67
    r8  a,  a,  a,  a,  a, |    % 68
    r8  a,  a,  a,  a,  a, |    % 69
    r8  a,  a,  a,  a,  a, |    % 70
    r8  a,  a,  a,  a,  a, |    % 71
    r8  a,  a,  a,  a,  a, |    % 72
    r8  a,  a,  a,  a,  a, |    % 73
    r8  a,  a,  a,  a,  a, |    % 74
    r8  a,  a,  a,  a,  a, |    % 75
    r8  a,  a,  a,  a,  a, |    % 76
    r8  a,  a,  a,  a,  a, |    % 77
    r8  a,  a,  a,  a,  a, |    % 78
}