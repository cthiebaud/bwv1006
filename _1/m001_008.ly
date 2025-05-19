\include "defs.ly"

guitarOneHeight = {
    r8                      e''16-3\1\I     dis''-2\1\M e  ''8-4\1\I            b  '-3\2\M \G  gis' -3\2\I                 b  ' -1\1\M                          | % 1
    e  '16-3\3\I fis'-1\2\M e  ' -3\3\I     dis' -2\3\M e  ' 8-4\3\I            b   -3\4\M \G  gis  -3\4\I                 b    -1\3\M                          | % 2    
    e16 \startModernBarre #4
          -4\5\P b   -1\3\M fis  -1\4\I     b    -1\3\A gis   -3\4\P b   -1\3\M a   -4\4\I     b    -1\3\A gis  -3\4\P     b     -1\3\M fis  -1\4\I b    -1\3\A \stopBarre | % 3
    <<
      { \voiceOne
    r16          e  '-2\2\I dis' -1\2\M     ( cis' -3\3 )
      }
      \\
      { \voiceTwo \stemUp
    e 4-4\5\P }
    >>                                                  b16   -1\3\I e  '-2\2\M dis'-1\2\I     cis' -3\3\I b    -1\3\M     a     -4\4\I gis  -3\4\M fis  -1\4\I | % 4
    e16 \startModernBarre #4
          -4\5\P b   -1\3\M fis  -1\4\I     b    -1\3\A gis   -3\4\P b   -1\3\M a   -4\4\I     b    -1\3\A gis  -3\4\P     b     -1\3\M fis  -1\4\I b    -1\3\A \stopBarre | % 5
    <<
      { \voiceOne
    r16          e  '-2\2\I dis' -1\2\M     ( cis' -3\3 )
      }
      \\
      { \voiceTwo \stemUp
    e 4-4\5\P }
    >>                                                  b16   -1\3\I e  '-2\2\M dis'-1\2\I     cis' -3\3\I b    -1\3\M     a     -4\4\I gis  -3\4\M fis  -1\4\I | % 6
    e   16-3\5\P fis -1\4\M gis  -2\4\I \G  a    -2\4\M b     -4\4\I cis'-1\3\M dis'-3\3\I \G  e  ' -3\3\M fis' -1\2\I     gis'  -3\2\M a  ' -4\2\I fis' -1\2\M | % 7
    gis'  -4\2\I b  '-1\1\A e  ' -3\3\I     fis' -1\2\M gis'  -2\2\I a  '-3\2\M b  '-1\1\I     cis''-2\1\M dis''-4\1\I \G  e  '' -4\1\M cis''-1\1\I dis''-3\1\M | % 8
}

bassOneHeight = {
    e'8                     r                           e                       r                          r4                                                   | % 1
    r8                      e16           [ dis ]       e8                    [ b,                         gis,                         b, ]                    | % 2
    e,8                     r                           r4                                                 r                                                    | % 3
    r4                                                  r16          e'       [ dis'           cis']       b             [ a            gis         fis ]       | % 4
    e8                      r                           r4                                                 r                                                    | % 5
    r4                                                  r16          e        [ dis            cis ]       b,            [ a,           gis,        fis,]       | % 6
    e,8                     r                           r4                                                 r                                                    | % 7
    e,8                     r                           r4                                                 r                                                    | %
}