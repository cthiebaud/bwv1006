\include "defs.ily"

guitarHundrednineteenHundredtwentytwo = {
<<
    {
      \voiceOne
      r16 e     \5   [ cis'  \3    b     \4    ] cis'  \3    [ e'    \3    a'     \1   gis'  \2    ] a'    \1    [ fis'   \2   cis'   \3   e'     \1   ] | % 119
      r16 fis   \5   [ dis'  \3    cis'  \3    ] dis'  \3    [ fis'  \2    a'     \1   gis'  \2    ] a'    \1    [ fis'   \2   dis'   \3   fis'   \2   ] | % 120
      r16 gis   \4   [ b     \2    a     \4    ] b     \2    [ e'    \2    gis'   \1   fis'  \2    ] gis'  \1    [ e'     \2   b      \2   e'     \1   ] | % 121
      r16 ais   \4   [ cis'  \3    b     \4    ] cis'  \3    [ e'    \3    ais'   \1   gis'  \2    ] ais'  \1    [ e'     \3   cis'   \3   e'     \1   ] | % 122
    }
    \\
    {
      \voiceTwo
      a,4 \5 s2 | % 119
      b,4 \6 s2 | % 120
      b,4 \6 s2 | % 121
      b,4 \6 s2 | % 122
    }
  >>
}

bassHundrednineteenHundredtwentytwo = {
  a,4                 r8          cis         fis         a         | % 119
  b,4                 r8          dis         fis         b         | % 120
  b,4                 r8          e           gis         b         | % 121
  b,8       b,        b,          b,          b,          b,        | % 122
  %% b,4                 b,                      b,                    | % 122
}
