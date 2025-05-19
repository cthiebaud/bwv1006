\include "defs.ly"

guitarNinetynineHundredheight = {
  \override Glissando.breakable = ##t
  \override Glissando.after-line-breaking = ##t
    % 99 - 108
  fis,16  \6\P [  a     \3\A    fis-4\4\M   cis -3\5\I ]  a  ,-2\6\P [   cis   \5\I  fis   \4\M      cis   \5\I  ] a   -4\4\M [ cis   \5\I    fis   \4\M   cis   \5\I    ] | % 99
  eis     \5\P [  gis   \4\M    eis\5  \I   cis   \6\P ]  eis   \5\I [   gis   \4\M  cis'  \3\I      gis   \4\P  ] eis'  \2\M [ cis'  \3\I    gis'  \2\A   b     \4\I    ] | % 100
  a     -4\5\P [  cis'-3\4\A    a  -4\5\M   fis   \5\I ]  a16   \5\P [   cis'  \4\I  fis'  \3\M      cis'  \4\I  ] a  '  \2\M [ fis'  \3\I    cis'' \1\A   fis'  \3\I \G ] | % 101
  eis'    \3\M [  gis'  \2\A    eis' \3\M   cis'  \4\I ]  cis'' \1\M [   bis'  \2\I  cis'' \1\M      bis'  \2\I  ] cis'' \1\M [ gis'  \3\I    a'    \2\M   fis'  \3\I \G ] | % 102
  eis'    \3\M [  gis'  \2\A    eis' \3\M   cis'  \4\I ]  b  '  \1\M [   ais'  \2\I  b  '  \1\M      ais'  \2\I  ] b  '  \1\M [ gis'  \2\I \G a'    \2\M   fis'  \3\I \G ] | % 103
  eis'    \3\M [  gis'  \2\A    eis' \3\M   cis'  \4\I ]  d  '  \3\M [   cis'  \4\I  d  '  \3\M      cis'  \4\I  ] d  '  \3\M [ gis   \5\I    a     \4\M   fis   \5\I \G ] | % 104
  eis     \5\P [  gis   \4\I    cis' \3\M   b  '  \1\I ]  b  '  \1\M [ ( gis'  \2 )  a  '  \1\A      fis'  \2\M  ] eis'  \3\I [ gis'  \2\I    cis'  \3\I ( b     \4 )    ] | % 105
  a       \4\P [  cis'  \3\I    fis' \2\M   cis'' \1\I ]  cis'' \1\M [ ( a  '  \2 )  b  '  \1\M      gis'  \2\I  ] fis'  \3\I [ a  '  \2\M    d  '  \3\I ( cis'  \4 )    ] | % 106
  b       \2\M [  d  '-4\4\I \H g    \3\I ( fis   \4 ) ]  eis   \4\I [   gis   \3\M  cis   \5\I    ( b  ,  \5 )  ] a  ,  \6\P [ cis   \5\I    fis   \4\M   gis   \3\A    ] | % 107
  a       \3\M [  fis   \4\I    b    \2\M   fis   \4\I ]  cis'  \2\M [   fis   \4\I < b,\P    d'\A > fis   \4\I  ] cis   \5\M [ fis   \4\I    gis   \3\M   eis   \4\I    ] | % 108
}

bassNinetynineHundredheight = {
  fis,4 r8 a, fis, a, | % 99
  cis4 r8 eis cis eis | % 100
  fis4 r8 a fis a | % 101
  cis'2. ~ | % 102
  cis'2. ~ | % 103
  cis'2. ~ | % 104
  cis'8 gis' eis' fis' gis' eis' | % 105
  fis'  a    fis  gis  a    fis  | % 106
  b     b,   cis  eis  fis  e    | % 107
  d     gis, a,   b,   cis  cis  | % 108
}
