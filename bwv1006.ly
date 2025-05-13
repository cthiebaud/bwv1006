\version "2.25.26"

#(set-global-staff-size 18) % Slightly smaller staff

\header {
  tagline = ##f
}

% Define the key and time signature
keySignature = { \key e \major }
timeSignature = { \time 3/4 }
tempoMarking = { \tempo 4=120 }

% https://lsr.di.unimi.it/LSR/Item?id=952
startModernBarre = 
#(define-event-function (fretnum) 
   (number?)
    #{
      \tweak bound-details.left.text
        \markup 
          \small \bold \concat { 
          %\Prefix
          #(format #f "~@r" fretnum)
          \hspace #.2
          \hspace #.5
        }
      \tweak font-size -1
      \tweak font-shape #'upright
      \tweak style #'dashed-line
      \tweak dash-fraction #0.3
      \tweak dash-period #1 
      \tweak bound-details.left.stencil-align-dir-y #0.35
      \tweak bound-details.left.padding 0.25
      \tweak bound-details.left.attach-dir -1
      \tweak bound-details.left-broken.text ##f
      \tweak bound-details.left-broken.attach-dir -1
      %% adjust the numeric values to fit your needs:
      \tweak bound-details.left-broken.padding 1.5
      \tweak bound-details.right-broken.padding 0
      \tweak bound-details.right.padding 0.25
      \tweak bound-details.right.attach-dir 2
      \tweak bound-details.right-broken.text ##f
      \tweak bound-details.right.text
        \markup
          \with-dimensions #'(0 . 0) #'(-.3 . 0) 
          \draw-line #'(0 . -1)
      \startTextSpan 
   #})

stopBarre = \stopTextSpan

P = #(define-music-function (parser location) () #{ \rightHandFinger #1 #})
I = #(define-music-function (parser location) () #{ \rightHandFinger #2 #})
M = #(define-music-function (parser location) () #{ \rightHandFinger #3 #})
A = #(define-music-function (parser location) () #{ \rightHandFinger #4 #})

% Include all parts
\include "_1/m001_008.ly"
\include "_1/m009_016.ly"
\include "_1/m017_028.ly"
\include "_1/m029_042.ly"
\include "_1/m043_050.ly"
\include "_1/m051_058.ly"
\include "_2/m059_066.ly"
\include "_2/m067_078.ly"
\include "_2/m079_092.ly"
\include "_2/m093_098.ly"
\include "_2/m099_108.ly"
\include "_3/m109_118.ly"
\include "_3/m119_122.ly"
\include "_3/m123_129.ly"
\include "_3/m130_133.ly"
\include "_3/m134_end.ly"

guitarPart = {
  \guitarOneHeight
  \guitarNineSixteen
  \guitarSeventeenTwentyheight
  \guitarTwentynineFortytwo
  \guitarFortythreeFifty
  \guitarFiftyOneFiftyheight
  \guitarFiftynineSixtysix
  \guitarSixtysevenSeventyheight
  \guitarSeventynineNinetytwo
  \guitarNinetythreeNinetyheight
  \guitarNinetynineHundredheight
  \guitarHundrednineHundredeighteen
  \guitarHundrednineteenHundredtwentytwo
  \guitarHundredtwentythreeHundredtwentynine
  \guitarHundredthirtyHundredthirtythree
  \guitarEnd
}

bassPart = {
  \bassOneHeight
  \bassNineSixteen
  \bassSeventeenTwentyheight
  \bassTwentynineFortytwo
  \bassFortythreeFifty
  \bassFiftyOneFiftyheight
  \bassFiftynineSixtysix
  \bassSixtysevenSeventyheight
  \bassSeventynineNinetytwo
  \bassNinetythreeNinetyheight
  \bassNinetynineHundredheight
  \bassHundrednineHundredeighteen
  \bassHundrednineteenHundredtwentytwo
  \bassHundredtwentythreeHundredtwentynine
  \bassHundredthirtyHundredthirtythree
  \bassEnd
}

\paper {
  #(set-paper-size "a4")
  indent = 0\mm
  % bottom-margin = 30\mm  % Increase this value as needed
  page-breaking =
    #(if (equal? (ly:get-option 'backend) 'svg)
       ly:one-page-breaking
       ly:page-turn-breaking) % fallback for other backends  
}

% Score setup
\score {
  <<
    \new StaffGroup <<
       \new Staff = "Guitar" <<
        \set Staff.midiInstrument = #"electric guitar (jazz)"
        \set Staff.midiMinimumVolume = #0.2  % Increase from default 0.2
        \set Staff.midiMaximumVolume = #0.5  % Max volume        
        \clef "treble_8"
        \keySignature
        \timeSignature
        \tempoMarking
        \guitarPart
       >>
      \new TabStaff {
        \clef "moderntab"
        \guitarPart
      }
    >>
    \new Staff = "Bass" <<
      \set Staff.midiInstrument = #"electric bass (finger)"
      \set Staff.midiMinimumVolume = #0.8  % Increase from default 0.2
      \set Staff.midiMaximumVolume = #1.0  % Max volume        
      \clef "bass"
      \keySignature
      \timeSignature
      \bassPart
    >>
  >>
  \layout {
    \context {
      \Voice
      \override StringNumber.stencil = ##f
    }
  }
  \midi {}
}
