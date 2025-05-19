\include "defs.ly"

guitarFortythreeFifty = {
  % 43 - 50
  <<
    {
      \voiceOne
      r16 fis   -1\4\I [ dis' -3\2\A fis   \4\I ] bis  -4\3\M [ fis   \4 dis' \2 fis   \4 ] bis  \3 [ fis   \4 dis' \2 fis   \4 ] | % 43
      r   e     -1\4\I [ cis' -3\3\M e     \4\I ] e'   -4\2\A [ e     \4 cis' \3 e     \4 ] e'   \2 [ e     \4 cis' \3 e     \4 ] | % 44
      r   fis   -1\4\I [ dis' -3\2\A fis   \4\I ] bis  -4\3\M [ fis   \4 dis' \2 fis   \4 ] bis  \3 [ fis   \4 dis' \2 fis   \4 ] | % 45
      r   e     -1\4\I [ cis' -3\3\M e     \4\I ] e'   -4\2\A [ e     \4 cis' \3 e     \4 ] e'   \2 [ e     \4 cis' \3 e     \4 ] | % 46
      r16 fisis -2\4\I [ cis' -4\3\M fisis \4\I ] e'   -3\2\A [ fisis \4 cis' \3 fisis \4 ] e'   \2 [ fisis \4 cis' \3 fisis \4 ] | % 47
      r   fisis -2\4\I [ cis' -4\3\M fisis \4\I ] e'   -3\2\A [ fisis \4 cis' \3 fisis \4 ] e'   \2 [ fisis \4 cis' \3 fisis \4 ] | % 48
      r   gis   -3\4\I [ cis' -4\3\M gis   \4\I ] dis' -1\2\A [ gis   \4 cis' \3 gis   \4 ] dis' \2 [ gis   \4 cis' \3 gis   \4 ] | % 49
      r   fis   -2\4\I [ bis  -4\3\M fis   \4\I ] dis' -3\2\A [ fis   \4 bis  \3 fis   \4 ] dis' \2 [ fis   \4 bis  \3 fis   \4 ] | % 50
    }
    \\
    {
      \voiceTwo
      \stemUp
      gis,4 -2\6\P s2 | % 43
      gis,4 -2\6\P s2 | % 44
      gis,4 -2\6\P s2 | % 45
      gis,4 -2\6\P s2 | % 46
      gis,4 -1\6\P s2 | % 47
      gis,4 -1\6\P s2 | % 48
      gis,4 -1\6\P s2 | % 49
      gis,4 -1\6\P s2 | % 50
    }
  >>
}

bassFortythreeFifty = {
  r8  gis,  gis,  gis,  gis,  gis,  | % 43
  r8  gis,  gis,  gis,  gis,  gis,  | % 44
  r8  gis,  gis,  gis,  gis,  gis,  | % 45
  r8  gis,  gis,  gis,  gis,  gis,  | % 46
  gis,4 gis4 r8 gis, | % 47
  gis,4 gis4 r8 gis, | % 48
  gis,4 gis4 r8 gis, | % 49
  gis,4 gis4 r8 gis, | % 50

  %%  %% \repeat unfold 8 { gis,4 s2 |  }   % 43-50
  %%  gis,4 s2 |    % 43
  %%  gis,4 s2 |    % 44
  %%  gis,4 s2 |    % 45
  %%  gis,4 s2 |    % 46
  %%  gis,4 s2 |    % 47
  %%  gis,4 s2 |    % 48
  %%  gis,4 s2 |    % 49
  %%  gis,4 s2 |    % 50  
}