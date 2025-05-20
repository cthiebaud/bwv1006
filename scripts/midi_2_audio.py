from midi2audio import FluidSynth
import os

soundfont_path = "/usr/local/share/soundfonts/Definitive_Guitar_Kit.sf2"

assert os.path.exists(soundfont_path), f"SoundFont not found at: {soundfont_path}"

fs = FluidSynth(sound_font=soundfont_path)
fs.midi_to_audio("bwv1006_ly_one_line.midi", "bwv1006_end.wav")
