# Lilypond to MIDI Pitch Number Equivalence Table

This table provides a comprehensive reference for converting between Lilypond notation and MIDI note numbers. In Lilypond, the octave numbering follows the scientific pitch notation where C4 (middle C) is MIDI note 60.

## Notation Explanation
- Lilypond notation uses lowercase letters (c, d, e, f, g, a, b) for notes
- Accidentals: 
  - Sharp: `is` (e.g., `cis` = C♯)
  - Double sharp: `isis` (e.g., `cisis` = C𝄪/C double sharp)
  - Flat: `es` or `s` for e and a (e.g., `des` = D♭, `es` = E♭, `as` = A♭)
  - Double flat: `eses` or `ses` for e and a (e.g., `deses` = D𝄫/D double flat)
- Octaves:
  - `'` (apostrophe) raises by one octave
  - `,` (comma) lowers by one octave
  - `c` is C3 (one octave below middle C)
  - `c'` is C4 (middle C)
  - `c''` is C5, etc.

## Lilypond <-> MIDI Pitch Number Table

| Octave | Note | Lilypond | MIDI |  | Note | Lilypond | MIDI |  | Note | Lilypond | MIDI |
|--------|------|----------|------|--|------|----------|------|--|------|----------|------|
| -1     | C    | c,,,     | 0    |  | C♯/D♭ | cis,,, / des,,, | 1  |  | D    | d,,,     | 2    |
|        | D♯/E♭ | dis,,, / ees,,, | 3 |  | E    | e,,,     | 4    |  | F    | f,,,     | 5    |
|        | F♯/G♭ | fis,,, / ges,,, | 6 |  | G    | g,,,     | 7    |  | G♯/A♭ | gis,,, / aes,,, | 8 |
|        | A    | a,,,     | 9    |  | A♯/B♭ | ais,,, / bes,,, | 10 |  | B    | b,,,     | 11   |
|        | B♯/C | bis,,, / c,,     | 12   |  | D𝄫  | deses,,, | 0    |  | C𝄪/D  | cisis,,, / d,,, | 2 |
|        | E𝄫  | eeses,,, | 2    |  | F𝄫  | feses,,, | 3    |  | E𝄪/F♯ | eisis,,, / fis,,, | 6 |
|        | G𝄫  | geses,,, | 5    |  | F𝄪/G♯ | fisis,,, / gis,,, | 8 |  | A𝄫  | aeses,,, | 7 |
|        | G𝄪/A♯ | gisis,,, / ais,,, | 10 |  | B𝄫  | beses,,, | 9    |  | A𝄪/B♯ | aisis,,, / bis,,, | 12 |
| 0      | C    | c,,      | 12   |  | C♯/D♭ | cis,, / des,, | 13   |  | D    | d,,      | 14   |
|        | D♯/E♭ | dis,, / ees,, | 15   |  | E    | e,,      | 16   |  | F    | f,,      | 17   |
|        | F♯/G♭ | fis,, / ges,, | 18   |  | G    | g,,      | 19   |  | G♯/A♭ | gis,, / aes,, | 20   |
|        | A    | a,,      | 21   |  | A♯/B♭ | ais,, / bes,, | 22   |  | B    | b,,      | 23   |
|        | B♯/C | bis,, / c,     | 24   |  | D𝄫  | deses,, | 12   |  | C𝄪/D  | cisis,, / d,, | 14 |
|        | E𝄫  | eeses,, | 14   |  | F𝄫  | feses,, | 15   |  | E𝄪/F♯ | eisis,, / fis,, | 18 |
|        | G𝄫  | geses,, | 17   |  | F𝄪/G♯ | fisis,, / gis,, | 20 |  | A𝄫  | aeses,, | 19 |
|        | G𝄪/A♯ | gisis,, / ais,, | 22 |  | B𝄫  | beses,, | 21   |  | A𝄪/B♯ | aisis,, / bis,, | 24 |
| 1      | C    | c,       | 24   |  | C♯/D♭ | cis, / des, | 25   |  | D    | d,       | 26   |
|        | D♯/E♭ | dis, / ees, | 27   |  | E    | e,       | 28   |  | F    | f,       | 29   |
|        | F♯/G♭ | fis, / ges, | 30   |  | G    | g,       | 31   |  | G♯/A♭ | gis, / aes, | 32   |
|        | A    | a,       | 33   |  | A♯/B♭ | ais, / bes, | 34   |  | B    | b,       | 35   |
|        | B♯/C | bis, / c      | 36   |  | D𝄫  | deses, | 24   |  | C𝄪/D  | cisis, / d, | 26 |
|        | E𝄫  | eeses, | 26   |  | F𝄫  | feses, | 27   |  | E𝄪/F♯ | eisis, / fis, | 30 |
|        | G𝄫  | geses, | 29   |  | F𝄪/G♯ | fisis, / gis, | 32 |  | A𝄫  | aeses, | 31 |
|        | G𝄪/A♯ | gisis, / ais, | 34 |  | B𝄫  | beses, | 33   |  | A𝄪/B♯ | aisis, / bis, | 36 |
| 2      | C    | c        | 36   |  | C♯/D♭ | cis / des | 37   |  | D    | d        | 38   |
|        | D♯/E♭ | dis / ees | 39   |  | E    | e        | 40   |  | F    | f        | 41   |
|        | F♯/G♭ | fis / ges | 42   |  | G    | g        | 43   |  | G♯/A♭ | gis / aes | 44   |
|        | A    | a        | 45   |  | A♯/B♭ | ais / bes | 46   |  | B    | b        | 47   |
|        | B♯/C | bis / c'      | 48   |  | D𝄫  | deses | 36   |  | C𝄪/D  | cisis / d | 38 |
|        | E𝄫  | eeses | 38   |  | F𝄫  | feses | 39   |  | E𝄪/F♯ | eisis / fis | 42 |
|        | G𝄫  | geses | 41   |  | F𝄪/G♯ | fisis / gis | 44 |  | A𝄫  | aeses | 43 |
|        | G𝄪/A♯ | gisis / ais | 46 |  | B𝄫  | beses | 45   |  | A𝄪/B♯ | aisis / bis | 48 |
| 3      | C    | c'       | 48   |  | C♯/D♭ | cis' / des' | 49   |  | D    | d'       | 50   |
|        | D♯/E♭ | dis' / ees' | 51   |  | E    | e'       | 52   |  | F    | f'       | 53   |
|        | F♯/G♭ | fis' / ges' | 54   |  | G    | g'       | 55   |  | G♯/A♭ | gis' / aes' | 56   |
|        | A    | a'       | 57   |  | A♯/B♭ | ais' / bes' | 58   |  | B    | b'       | 59   |
|        | B♯/C | bis' / c''     | 60   |  | D𝄫  | deses' | 48   |  | C𝄪/D  | cisis' / d' | 50 |
|        | E𝄫  | eeses' | 50   |  | F𝄫  | feses' | 51   |  | E𝄪/F♯ | eisis' / fis' | 54 |
|        | G𝄫  | geses' | 53   |  | F𝄪/G♯ | fisis' / gis' | 56 |  | A𝄫  | aeses' | 55 |
|        | G𝄪/A♯ | gisis' / ais' | 58 |  | B𝄫  | beses' | 57   |  | A𝄪/B♯ | aisis' / bis' | 60 |
| 4      | C    | c''      | 60   |  | C♯/D♭ | cis'' / des'' | 61   |  | D    | d''      | 62   |
|        | D♯/E♭ | dis'' / ees'' | 63   |  | E    | e''      | 64   |  | F    | f''      | 65   |
|        | F♯/G♭ | fis'' / ges'' | 66   |  | G    | g''      | 67   |  | G♯/A♭ | gis'' / aes'' | 68   |
|        | A    | a''      | 69   |  | A♯/B♭ | ais'' / bes'' | 70   |  | B    | b''      | 71   |
|        | B♯/C | bis'' / c'''    | 72   |  | D𝄫  | deses'' | 60   |  | C𝄪/D  | cisis'' / d'' | 62 |
|        | E𝄫  | eeses'' | 62   |  | F𝄫  | feses'' | 63   |  | E𝄪/F♯ | eisis'' / fis'' | 66 |
|        | G𝄫  | geses'' | 65   |  | F𝄪/G♯ | fisis'' / gis'' | 68 |  | A𝄫  | aeses'' | 67 |
|        | G𝄪/A♯ | gisis'' / ais'' | 70 |  | B𝄫  | beses'' | 69   |  | A𝄪/B♯ | aisis'' / bis'' | 72 |
| 5      | C    | c'''     | 72   |  | C♯/D♭ | cis''' / des''' | 73   |  | D    | d'''     | 74   |
|        | D♯/E♭ | dis''' / ees''' | 75   |  | E    | e'''     | 76   |  | F    | f'''     | 77   |
|        | F♯/G♭ | fis''' / ges''' | 78   |  | G    | g'''     | 79   |  | G♯/A♭ | gis''' / aes''' | 80   |
|        | A    | a'''     | 81   |  | A♯/B♭ | ais''' / bes''' | 82   |  | B    | b'''     | 83   |
|        | B♯/C | bis''' / c''''   | 84   |  | D𝄫  | deses''' | 72   |  | C𝄪/D  | cisis''' / d''' | 74 |
|        | E𝄫  | eeses''' | 74   |  | F𝄫  | feses''' | 75   |  | E𝄪/F♯ | eisis''' / fis''' | 78 |
|        | G𝄫  | geses''' | 77   |  | F𝄪/G♯ | fisis''' / gis''' | 80 |  | A𝄫  | aeses''' | 79 |
|        | G𝄪/A♯ | gisis''' / ais''' | 82 |  | B𝄫  | beses''' | 81   |  | A𝄪/B♯ | aisis''' / bis''' | 84 |
| 6      | C    | c''''    | 84   |  | C♯/D♭ | cis'''' / des'''' | 85   |  | D    | d''''    | 86   |
|        | D♯/E♭ | dis'''' / ees'''' | 87   |  | E    | e''''    | 88   |  | F    | f''''    | 89   |
|        | F♯/G♭ | fis'''' / ges'''' | 90   |  | G    | g''''    | 91   |  | G♯/A♭ | gis'''' / aes'''' | 92   |
|        | A    | a''''    | 93   |  | A♯/B♭ | ais'''' / bes'''' | 94   |  | B    | b''''    | 95   |
|        | B♯/C | bis'''' / c'''''  | 96   |  | D𝄫  | deses'''' | 84   |  | C𝄪/D  | cisis'''' / d'''' | 86 |
|        | E𝄫  | eeses'''' | 86   |  | F𝄫  | feses'''' | 87   |  | E𝄪/F♯ | eisis'''' / fis'''' | 90 |
|        | G𝄫  | geses'''' | 89   |  | F𝄪/G♯ | fisis'''' / gis'''' | 92 |  | A𝄫  | aeses'''' | 91 |
|        | G𝄪/A♯ | gisis'''' / ais'''' | 94 |  | B𝄫  | beses'''' | 93   |  | A𝄪/B♯ | aisis'''' / bis'''' | 96 |
| 7      | C    | c'''''   | 96   |  | C♯/D♭ | cis''''' / des''''' | 97   |  | D    | d'''''   | 98   |
|        | D♯/E♭ | dis''''' / ees''''' | 99   |  | E    | e'''''   | 100  |  | F    | f'''''   | 101  |
|        | F♯/G♭ | fis''''' / ges''''' | 102  |  | G    | g'''''   | 103  |  | G♯/A♭ | gis''''' / aes''''' | 104  |
|        | A    | a'''''   | 105  |  | A♯/B♭ | ais''''' / bes''''' | 106  |  | B    | b'''''   | 107  |
|        | B♯/C | bis''''' / c''''''  | 108  |  | D𝄫  | deses''''' | 96   |  | C𝄪/D  | cisis''''' / d''''' | 98 |
|        | E𝄫  | eeses''''' | 98   |  | F𝄫  | feses''''' | 99   |  | E𝄪/F♯ | eisis''''' / fis''''' | 102 |
|        | G𝄫  | geses''''' | 101  |  | F𝄪/G♯ | fisis''''' / gis''''' | 104 |  | A𝄫  | aeses''''' | 103 |
|        | G𝄪/A♯ | gisis''''' / ais''''' | 106 |  | B𝄫  | beses''''' | 105  |  | A𝄪/B♯ | aisis''''' / bis''''' | 108 |
| 8      | C    | c''''''  | 108  |  | C♯/D♭ | cis'''''' / des'''''' | 109  |  | D    | d''''''  | 110  |
|        | D♯/E♭ | dis'''''' / ees'''''' | 111  |  | E    | e''''''  | 112  |  | F    | f''''''  | 113  |
|        | F♯/G♭ | fis'''''' / ges'''''' | 114  |  | G    | g''''''  | 115  |  | G♯/A♭ | gis'''''' / aes'''''' | 116  |
|        | A    | a''''''  | 117  |  | A♯/B♭ | ais'''''' / bes'''''' | 118  |  | B    | b''''''  | 119  |
|        | B♯/C | bis'''''' / c'''''''  | 120  |  | D𝄫  | deses'''''' | 108  |  | C𝄪/D  | cisis'''''' / d'''''' | 110 |
|        | E𝄫  | eeses'''''' | 110  |  | F𝄫  | feses'''''' | 111  |  | E𝄪/F♯ | eisis'''''' / fis'''''' | 114 |
|        | G𝄫  | geses'''''' | 113  |  | F𝄪/G♯ | fisis'''''' / gis'''''' | 116 |  | A𝄫  | aeses'''''' | 115 |
|        | G𝄪/A♯ | gisis'''''' / ais'''''' | 118 |  | B𝄫  | beses'''''' | 117  |  | A𝄪/B♯ | aisis'''''' / bis'''''' | 120 |
| 9      | C    | c''''''' | 120  |  | C♯/D♭ | cis''''''' / des''''''' | 121  |  | D    | d''''''' | 122  |
|        | D♯/E♭ | dis''''''' / ees''''''' | 123  |  | E    | e''''''' | 124  |  | F    | f''''''' | 125  |
|        | F♯/G♭ | fis''''''' / ges''''''' | 126  |  | G    | g''''''' | 127  |  | G♯   | gis''''''' | 128* |
|        | D𝄫  | deses''''''' | 120  |  | C𝄪/D  | cisis''''''' / d''''''' | 122 |  | E𝄫  | eeses''''''' | 122  |
|        | F𝄫  | feses''''''' | 123  |  | E𝄪/F♯ | eisis''''''' / fis''''''' | 126 |  | G𝄫  | geses''''''' | 125  |
|        | F𝄪/G | fisis''''''' / g''''''' | 127 |  |      |          |      |  |      |          |      || 92   |  | A    | a'''     | 93   |  | A♯   | ais'''   | 94   |
|        | B♭   | bes'''   | 94   |  | B    | b'''     | 95   |  |      |          |      |
| 7      | C    | c''''    | 96   |  | C♯   | cis''''  | 97   |  | D♭   | des''''  | 97   |
|        | D    | d''''    | 98   |  | D♯   | dis''''  | 99   |  | E♭   | ees''''  | 99   |
|        | E    | e''''    | 100  |  | F    | f''''    | 101  |  | F♯   | fis''''  | 102  |
|        | G♭   | ges''''  | 102  |  | G    | g''''    | 103  |  | G♯   | gis''''  | 104  |
|        | A♭   | aes''''  | 104  |  | A    | a''''    | 105  |  | A♯   | ais''''  | 106  |
|        | B♭   | bes''''  | 106  |  | B    | b''''    | 107  |  |      |          |      |
| 8      | C    | c'''''   | 108  |  | C♯   | cis''''' | 109  |  | D♭   | des''''' | 109  |
|        | D    | d'''''   | 110  |  | D♯   | dis''''' | 111  |  | E♭   | ees''''' | 111  |
|        | E    | e'''''   | 112  |  | F    | f'''''   | 113  |  | F♯   | fis''''' | 114  |
|        | G♭   | ges''''' | 114  |  | G    | g'''''   | 115  |  | G♯   | gis''''' | 116  |
|        | A♭   | aes''''' | 116  |  | A    | a'''''   | 117  |  | A♯   | ais''''' | 118  |
|        | B♭   | bes''''' | 118  |  | B    | b'''''   | 119  |  |      |          |      |
| 9      | C    | c''''''  | 120  |  | C♯   | cis''''' | 121  |  | D♭   | des''''' | 121  |
|        | D    | d''''''  | 122  |  | D♯   | dis''''' | 123  |  | E♭   | ees''''' | 123  |
|        | E    | e''''''  | 124  |  | F    | f''''''  | 125  |  | F♯   | fis''''' | 126  |
|        | G♭   | ges''''' | 126  |  | G    | g''''''  | 127  |  |      |          |      |

## Notable Reference Points
- MIDI note 0: C-1 (lowest possible MIDI note)
- MIDI note 21: A0 (lowest key on standard 88-key piano)
- MIDI note 60: C4 (middle C)
- MIDI note 108: C8 (highest C on standard 88-key piano)
- MIDI note 127: G9 (highest possible MIDI note)

## Quick Formula
To calculate MIDI note number from scientific pitch notation:
MIDI number = 12 × (octave + 1) + note value

Where note values are:
C = 0, C♯/D♭ = 1, D = 2, D♯/E♭ = 3, E = 4, F = 5, F♯/G♭ = 6, G = 7, G♯/A♭ = 8, A = 9, A♯/B♭ = 10, B = 11
