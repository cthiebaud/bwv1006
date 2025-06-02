\version "2.25.26"

\include "defs.ily"
\include "highlight-bars.ily"
\include "bwv1006_ly_main.ly"

#(set-global-staff-size 18) % Slightly smaller staff

% Define a helper to detect SVG mode
#(define is-svg?
   (equal? (ly:get-option 'backend) 'svg))

#(if (not is-svg?)
     (set-global-staff-size 16))   

% ================================================================
% REMOVE ALL OF THIS COMPLEX STRUCTURE LOGIC:
% - break-structure definition
% - breakEvery function  
% - generate-layout-breaks function
% - layoutBreaks variable
% - calculate-line-starts function
% - line-starting-bars variable
% - highlight-line-breaks function
% ================================================================

% Formatted one-pager for display
\book {
  \bookOutputName "bwv1006"
  \paper {
    indent = 0
    page-breaking = #(if is-svg?
                         ly:one-page-breaking
                         ly:page-turn-breaking)

    line-width = #(if is-svg?
                      (* 260 mm)
                      (* 160 mm))

    paper-width = #(if is-svg?
                       (* 270 mm)
                       (* 210 mm))
  }

  \score {
    \bwvOneThousandSixScore
    \layout {
      % Apply larger note heads only for SVG output
      #(if is-svg?
           (ly:parser-include-string 
             "\\override NoteHead.font-size = #2")
           )
      \context {
        \Voice
        \override StringNumber.stencil = ##f
      }
      % Apply simple highlighting only for SVG output
      #(if is-svg?
           (ly:parser-include-string 
             "\\context {
               \\Staff
               \\consists #Simple_highlight_engraver
               \\consists Staff_highlight_engraver
               \\consists #Bar_timing_collector
             }
             \\context {
               \\Score
               \\override StaffHighlight.after-line-breaking = #add-data-bar-to-highlight
             }")
           )
    }
  }
}