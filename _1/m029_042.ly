\include "defs.ly"

guitarTwentynineFortytwo = {
  \override Glissando.breakable = ##t
  \override Glissando.after-line-breaking = ##t
  % 29 -32
  e,16-0\6\P [ fis -1\4\M e   -4\5\I fis -1\4\M ] gis -3\4\I [ b     -0\2\A    e     \5\I fis     \4\M ]    gis   \4\I [ b     \2\A    e     \5\I fis   \4\M    ] | % 29
  gis -4\5\P [ a   -1\4\M gis -4\5\I a   -1\4\M ] b   -3\4\I [ e    '-0\1\A    gis   \5\I a       \4\M ]    b     \4\I [ e  '  \1\A    gis   \5\I a     \4\M    ] | % 30
  b   -3\4\P [ cis'-1\3\M b   -3\4\I cis'-1\3\M ] d  '-2\3\I [ gis  '-4\2\A    b     \4\I cis  '  \3\M ]    d  '  \3\I [ gis'  \2\A    b     \4\I cis'  \3\M    ] | % 31
  d  '-1\3\P [ b  '-2\1\M gis'-4\2\I e  '-0\1\A ] d  '-3\3\I [ b     -0\2\A    gis -1\4\M e     -2\5\P ]    d   -0\4\M [ cis -4\5\I    d   -0\4\M b  ,-2\5\I    ] | % 32
  % 33 - 42                                                                                                                                                          
  cis -4\5\P [ dis -1\4\M cis -4\5\I dis -1\4\M ] eis -3\4\I [ gis   -1\3\A    cis   \5   dis     \4   ]    eis   \4   [ gis   \3      cis   \5   dis   \4      ] | % 33
  eis -4\5\P [ fis -1\4\M eis -4\5\I fis -1\4\M ] gis -1\4\I [ cis  '-1\3\A    eis -3\4\I fis   -4\4\M ]    gis   \4   [ cis'  \3      eis   \4   fis   \4      ] | % 34
  gis -4\5\P [ a   -1\4\M gis -4\5\I a   -1\4\M ] b   -2\4\I [ eis  '-3\3\A    gis        a            ]    b          [ eis'          gis        a             ] | % 35
  b   -1\4\P [ gis'-2\2\I eis'-3\3\M cis'-4\4\P ] b  '-1\1\M [ gis  '-2\2\M \G a  '-2\2\I fis  '-3\3\M ] \G eis'-3\3\I [ gis'-2\2\A    cis'-4\4\I b   -0\2\M    ] | % 36
  a   -2\4\I [ cis'-1\2\M a   -2\4\I fis -4\5\P ] fis'-2\2\M [ dis  '-3\3\I    e  '-1\2\M cis  '-2\3\I ] \G bis -2\3\M [ dis'-1\2\A    gis -3\4\I fis -1\4\M    ] | % 37
  e   -4\5\P [ gis -3\4\A e   -4\5\M cis -1\5\I ] e   -4\5\P [ gis   -2\4\I    cis'-3\3\M gis   -2\4\I ]    e  '-1\2\M [ cis'-3\3\I    gis'-1\1\M cis'-3\3\I    ] | % 38
  bis -2\3\M [ dis'-1\2\A bis -2\3\M gis -3\4\I ] gis'-1\1\M [ fisis'-4\2\I    gis'-1\1\M fisis'-4\2\I ]    gis'-1\1\M [ dis'-2\2\I \G e  '-2\2\M cis'-3\3\I    ] | % 39
  bis -3\3\M [ dis'-2\2\A bis -3\3\M gis -4\4\I ] fis'-1\1\M [ eis  '-4\2\I    fis'-1\1\M eis  '-4\2\I ]    fis'-1\1\M [ dis'-2\2\I \G e  '-2\2\M cis'-3\3\I \G ] | % 40
  bis -3\3\M [ dis'-2\2\A bis -3\3\M gis -4\4\I ] a   -1\3\M [ gis   -4\4\I    a   -1\3\M gis   -4\4\I ]    a16 -1\3\M [ dis -4\5\I    e   -1\4\M cis -2\5\I    ] | % 41
  bis,-1\5\P [ fis -2\4\M cis -1\5\I fis -2\4\A ] dis -4\5\P [ fis  -2 \4\M    cis -1\5\I fis   -2\4\A ]    bis,-1\5\P [ fis -2\4\M    dis -4\5\I fis -1\4\A    ] | % 42
}              

bassTwentynineFortytwo = {
  e,4                                             r                                                         r                                                     | % 29
  e                                               r                                                         r                                                     | % 30
  e,                                              r                                                         r                                                     | % 31
  e                                               r                                                         r                                                     | % 32
  eis8                    cis'                    cis'                         cis'                         cis'                       cis'                       | % 33
  r  8                    gis                     gis                          gis                          gis                        gis                        | % 34
  r  8                    eis                     eis                          eis                          eis                        eis                        | % 35
  r  8                    cis                     cis                          cis                          cis                        cis                        | % 36
  %% < eis cis' >4                                   r2                                                                                                              | % 33
  %% gis 4                                           r2                                                                                                              | % 34
  %% eis 4                                           r2                                                                                                              | % 35
  %% cis 4                                           r2                                                                                                              | % 36
  fis,4                                           r8                           fis                          gis                        bis,                       | % 37
  cis4                                            r8                           e                            cis                        e                          | % 38
  gis2. ~                                                                                                                                                         | % 39
  gis2. ~                                                                                                                                                         | % 40
  gis2. ~                                                                                                                                                         | % 41
  gis2.                                                                                                                                                           | % 42
}
       