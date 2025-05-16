
guitarSeventeenTwentyheight = <<
  \new Voice = "one" {
    \voiceOne
    % ERROR: not 12 notes in measure
    gis' -3\2\I8 gis'-3\2\M8 gis' \28 gis' \28 gis' \28 gis' \28
    gis' -3\2\I8 gis'-3\2\M8 gis' \28 gis' \28 gis' \28 gis' \28
    ' -3\2\I8 '-3\2\M8 ' \28 ' \28 ' \28 ' \28
    ' -3\2\I8 '-3\2\M8 ' \28 ' \28 ' \28 ' \28
    gis' -2\2\I8 gis'-2\2\M8 gis' \28 gis' \28 gis' \28 gis' \28
    gis' -2\2\I8 gis'-2\2\M8 gis'-4\28 gis'-4\28 gis'-4\28 gis'-4\28
    fis' -3\2\I8 fis'-3\2\A8 fis' \2\M8 fis' \2\A8 fis' \28 fis' \28
    fis' -3\2\I8 fis'-3\2\A8 fis'-4\2\M8 fis'-4\2\A8 fis' \28 fis' \28
    ' -2\2\I8 '-2\2\A8 ' \2\M8 ' \2\A8 '-3\28 '-3\28
    ' -3\2\I8 '-3\2\A8 '-4\2\M8 ' \2\A8 ' \28 ' \28
    dis' -3\2\I8 dis'-3\2\A8 dis' \2\M8 dis' \2\A8 dis' \28 dis' \28
  }
  \new Voice = "two" {
    \voiceTwo
    % ERROR: not 12 notes in measure
    r16 '-0\1\A8 dis'-2\3\P8 ' \18 dis' \38 ' \18 dis' \316
    r16 '-0\1\A8 '-1\3\P8 ' \18 ' \38 ' \18 ' \316
    r16 '-0\1\A8 cis'-4\4\P8 ' \18 cis' \48 ' \18 cis' \416
    r16 '-0\1\A8 b -1\4\P8 ' \18 b \48 ' \18 b \416
    r16 '-0\1\A8 b -1\4\P8 ' \18 b \48 ' \18 b \416
    r16 '-0\1\A8 a -1\4\P8 '-0\18 a -2\48 '-0\18 a -2\416
    r16 dis'-4\3\I8 a -2\4\P8 dis' \3\I8 a \4\P8 dis' \38 a \416
    r16 b -1\3\I8 gis -2\4\P8 b -1\3\I8 gis -3\4\P8 b \38 gis \416
    r16 b -1\3\I8 gis -3\4\P8 b \3\I8 gis -4\4\P8 b -1\38 gis -4\416
    r16 a -1\3\I8 fis -2\4\P8 a \3\I8 fis \4\P8 a \38 fis \416
    r16 a -1\3\I8 fis -2\4\P8 a \3\I8 fis \4\P8 a \38 fis \416
  }
>>
