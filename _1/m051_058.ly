\include "defs.ily"

guitarFiftyOneFiftyheight = {
  cis16 [ cis' b   a   ] gis [ cis' gis fis ] e   [ gis e   dis ] | % 51
  cis16 [ cis' gis fis ] e   [ gis  e   dis ] cis [ e   cis b,  ] | % 52

  <<
    {
      \voiceOne
      r16 fis [ cis' fis ] e' [ fis  cis' fis ] e' [ fis cis' fis ] | % 53
      r16 fis [ cis' fis ] e' [ fis  cis' fis ] e' [ fis cis' fis ] | % 54
    }
    \\
    {
      \voiceTwo
      \stemUp
      ais,4 s4 s4 | % 53
      ais,4 s4 s4 | % 54
    }
  >>

  <<
    {
      \voiceOne
      r16       b'\1  [ ais'\1    gis'\2 ]
    }
    \\
    {
      \voiceTwo
      \stemUp
      b,4 \6
    }
  >>
                                                               fis'16 [ b'   fis' e'   ] dis' [ fis' dis' cis' ] | % 55
  b    [ b' fis' e'   ] dis' [ fis' dis' cis' ] b    [ dis' b    a    ] | % 56

  <<
    {
      \voiceOne
      r16 d' [ e' d' ] gis' [ d' b'  d' ] gis' [ d' e' d' ] | % 57
      r   d' [ e' d' ] gis  [ d' fis d' ] gis  [ d' e  d' ] | % 58
    }
    \\
    {
      \voiceTwo
      gis4 s2 | % 57
      gis4 s2 | % 58
    }
  >>

}

bassFiftyOneFiftyheight = {
  cis8 cis e gis cis'4    | % 51
  r8   cis e gis cis' cis | % 52

  fis4 r r | % 53
  fis, r r | % 54

  r8  b, dis fis b4 | % 55
  r8  b, dis fis b b, | % 56

  e4 r r | % 57
  e, r r | % 58

}
