\include "defs.ily"

guitarNinetythreeNinetyheight = {
  <<
    {
      \voiceOne
      b'16  \2    [ d  ''  \1     b  '  \2    gis'  \3    ] r           b  '  \2    [ gis'  \2    eis'  \3    ] r           b  '   \2   [ a  '  \2    gis'  \2    ] | % 93
      r             gis'   \2   [ a  '  \2    fis'  \3    ] r           a  '  \2    [ gis'  \2    fis'  \3    ] r           gis'   \2   [ fis'  \2    eis'  \3    ] | % 94
      r             e  '   \3   [ fis'  \3    d  '  \4    ] r           fis'  \2    [ e  '  \3    d  '  \3    ] r           e  '   \3   [ d  '  \3    cis'  \3    ] | % 95
      r             cis'   \3   [ d  '  \3    b     \4    ] r           d  '  \3    [ cis'  \3    b     \4    ] r           cis'   \3   [ b     \4    a     \4    ] | % 96
    }
    \\
    {
      \voiceTwo
      r4          eis'  \3    cis'  \4    | % 93
      fis'  \3    b     \4    cis'  \4    | % 94
      d  '  \4    gis   \4    ais   \4    | % 95
      b     \4    eis   \5    fis   \5    | % 96
    }
  >>

  gis16  \4   [ a    \4     b     \4    a    \4     ] gis   \4    [ b    \2     a    \4     b   \2      ] gis    \4   [ b   \2      fis   \5    b     \2    ] | % 97
  eis    \5   [ fis  \5     gis   \4    a    \4     ] b     \2    [ eis  \4     d'   \2     eis \4      ] cis'   \2   [ eis \4      b     \2    eis   \4    ] | % 98
}

bassNinetythreeNinetyheight = {
    r8 cis cis ( cis cis cis ) | % 93
    %% cis 4 r r | % 93
    fis 4 r r | % 94
    R2. | % 95
    R2. | % 96
    R2. | % 97
    R2. | % 98
}
