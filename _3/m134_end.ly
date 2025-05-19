
guitarEnd = {
  % 134 - end
  <<
    {
      \voiceOne
      a' 4. -2\2 b'8\1 gis'4 \1 ~ | % 134 
      gis' 16 \1 ( [ a'16 \1 gis' \1 a'32 \1 fis' \2  ] \tupletUp \tuplet 3/4 { gis'32 \2 fis' \2 gis' \2 } ) fis'4 \2 e'8 \3 | % 135               
      < e, \6 gis \5 e' \1 >4 r16 e'' 8 \1 [ e''\1 ] e''\1 [ e'' 16 \1 ]  | % 136
      e'4 \3                 r16 e'  8 \1 [ e' \1 ] e' \1 [ e'  16 \1 ]  | % 137
    }
    \\
    {
      \voiceTwo
      < b -1\4 fis' -3\3    >2 < e,\6 b\3 e'\2 >4 ~ | % 134
      < a, \5 cis' \3 e' \2 >4 b, \6  < b, \6 a \4 > | % 135
      \once \override Rest.direction = #UP
      r16 e'' \1 [ dis'' \1 cis'' \1 ] b'8 \2 [ a' \2 ] gis' \2 [ fis' \3 ] | % 136
      \once \override Rest.direction = #DOWN
      r16 e'  \1 [ dis'  \3 cis'  \4 ] b 8 \2 [ a \harmonic \5 ] gis  \5 [ fis  \5 ] | % 137
    }  
  >> 
  e16 \harmonic \6 [ gis \5 b \2 dis' \3] e' \1 
    [
    < e, gis'\harmonic > \6 ^\markup { \tiny \circle "9" }
    b  '   \harmonic \2  
    < dis' dis''\harmonic >  \3 ] 
    e  ''4 \harmonic \1 
    \fermata \bar "|." | % 138    
}

bassEnd = {
  b,2 e4 | % 134
  a4 b b, | % 135
  e r r  | % 136
  r8  e,  e,  e,  e,  e, | % 137
  %% e,4 r2 | % 137
  e,2 r4 | % 138
}
