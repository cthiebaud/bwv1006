\include "defs.ly"

guitarFiftynineSixtysix = {
  % 59 - 66
  <<
    {
      \voiceOne
      
      cis'16-2\3\P \startModernBarre #5 [ 
                   e' -1\2\I   a'  -1\1\M ( gis'-4\2   ) ] r16        e'8-1\2\M [ \stopBarre
                                                                                            e'\1\A  ]         e'\1\M           [ e'16\1\A]   | % 59
      r   16       a' -2\1\I [ gis'-1\1\M ( fis'-4\2   ) ] e'8-1\2\A           [ fis'-4\2\M ]        e'-1\2\A       [ d'-4\3\M ]             | % 60
      r   16       e'8  \1\M [              e  '  \1\A   ]            e '  \1\M            [  e'\1\A  ]        e'\1\M            [ e'16\1\A ]  | % 61
      r   16       a' -2\1\I [ gis'-1\1\M ( fis'-4\2   ) ] e'8-1\2\M           [ fis'-4\2\A ]       e'-1\2\M        [ d'-4\3\A ]             | % 62
    }
    \\
    {
      \voiceTwo
      s   4                                                a'8-1\1\A           [ d  '-3\3\I ]       cis'-2\3\P     [ b -1\3\I ]             | % 59
      a   4-3\4\P                                          r 16      a8-3\4\P             [ a\4\I ]           a\4\P           [  a16\4\I ]   | % 60
      cis'8-2\3\P            [ b -1\3\I ]                  cis'-2\3\P          [  d' -3\3\I  ]       cis'-2\3\P     [ b -1\3\I ]             | % 61
      a   4-3\4\P                                          r 16      a8-3\4\I             [ a\4\P  ]          a\4\I            [ a16\4\P ]   | % 62
    }
  >>
  <<
    {
      \voiceOne
      cis'8-2\3\M            [ a   -4\4\A    ]              gis-4\4\M           [  a   -1\3\A  ]       b -4\3\M   [     gis-1\3\A ]             | % 63
      a    -2\3\M            [ cis'-3\2\A    ]              b  -0\2\M           [  cis'-3\2\A  ]       d'-4\2\M   [     b  -0\2\A ]             | % 64
      cis' -3\2\M            [ a   -2\3\A    ]              gis-1\3\M           [  a   -2\3\A  ]       b -4\3\M   [     gis-1\3\A ]             | % 65
      a    -1\3\M            [ cis'-2\2\A    ]              b  -0\2\M           [  cis'-2\2\A  ]       d'-3\2\M   [     b  -0\2\A ]             | % 66
    }
    \\
    {
      \voiceTwo
      r16          a,8    \I              [ a, \P  ]                  a, \I               [   a, \P ]           a, \I          [   a,16 \P ]   | % 63
      r            a,8    \I              [ a  \P  ]                  a  \I               [   a  \P ]           a  \I          [   a 16 \P ]   | % 64
      r            a,8    \I              [ a, \P  ]                  a, \I               [   a, \P ]           a, \I          [   a,16 \P ]   | % 65
      r            a,8    \I              [ a  \P  ]                  a  \I               [   a  \P ]           a  \I          [   a 16 \P ]   | % 66
    }
  >>
}

bassFiftynineSixtysix = {
  a,4 r r | % 59
  \stemDown r8 a16 b cis'8 d' cis' b  |  % 60
  a4 r r | % 61
  \stemUp r8 a,16 b, cis8 d cis b,  |  % 62

  a,4 r r | % 63
  R2. | % 64
  a,4 r r | % 65
  R2. | % 66
}