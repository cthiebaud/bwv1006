\include "defs.ily"

guitarHundrednineHundredeighteen = {
  <<
    {
      \voiceOne
      r16        a 8  \3             [ a   \3 ]            a    \3            [ a   \3 ]              a   \3    [ a 16 \3    ] | % 109
      r16        a 8  \3             [ a   \3 ]            a    \3            [ a   \3 ]              a   \3    [ a 16 \3    ] | % 110
      s4                                     r16           e'8                [ e'     ]              e'        [ e'16       ] | % 111
      r16        e'8                 [ e'     ]            e'                 [ e'     ]              e'        [ e'16 \2    ] | % 112
    }
    \\
    { 
      \voiceTwo
      fis8  \4           [ gis  \4   ]           a      \4         [ gis   \4 ]            fis   \4             [ e    \4    ] | % 109
      dis   \5           [ e    \4   ]           fis    \4         [ gis   \4 ]            a     \4             [ fis  \4    ] | % 110
      gis16 \4   a   \3    gis  \4     fis  \4   e8     \4         [ dis'  \2 ]            cis'  \3             [ b    \3    ] | % 111
      ais   \3           [ b    \3   ]           cis'   \3         [ dis'  \2 ]            e  '  \2             [ cis' \3    ] | % 112
    }
  >>
  <<
    {
      \voiceOne
      s2.                                                                                                                              | r16 b  8    [ b      ] b      [ b       ] b      [ b  16     ] | % 113-114
      cis 4    s2                                                                                                                      | r16 a  8    [ a      ] a      [ a       ] a      [ a  16     ] | % 115-116
      b  ,4 \6 s2                                                                                                                      | r16 gis8 \3 [ gis \3 ] gis \3 [ gis \3  ] gis \3 [ gis16 \3  ] | % 117-118
    }
    \\
    { 
      \voiceTwo
      dis'16     e'  \2    dis' \2     cis' \3   b      \3 cis' \3   dis'  \2   e'    \2   fis' \2    gis' \1    a'    \1   fis'  \2   | b'  8  \1 [ a    \4 ] gis  \4 [ fis  \4 ] e    \4 [ d    \4 ] | % 113-114
      r16        e   \4    fis  \4     gis  \4   a      \3 b    \3   cis'  \3   d  '  \2   e'   \2    fis' \2    gis'  \1   e'    \2   | a'  8  \1 [ gis  \4 ] fis  \4 [ e    \4 ] dis  \5 [ cis  \5 ] | % 115-116
      r16        dis \5    e    \5     fis  \4   gis    \4 a    \4   b     \3   cis'  \3   dis' \3    e'   \2    fis'  \2   dis'  \3   | gis'8  \2 [ fis  \5 ] e    \5 [ d    \5 ] cis  \6 [ b  , \6 ] | % 117-118
    }
  >>
}            

bassHundrednineHundredeighteen = {
  fis,4 fis 4 r8 fis  | % 109
  b4    b  ,4 r8 b  , | % 110
  e4    e  '  r8 cis' | % 111
  fis'4 fis   r8 fis  | % 112

  b   b  ,16 cis  dis 8 fis b   a   | gis4      e  '   r  8  gis    | % 114 
  a   a  ,16 b  , cis 8 e   a   gis | fis4      dis'   r  8  fis    | % 116
  gis gis,16 a  , b  ,8 dis gis fis | e    fis  e    d cis   b  ,   | % 118
}