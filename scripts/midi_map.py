from mido import MidiFile, tick2second
import pandas as pd

def extract_note_intervals(midi_path):
    mid = MidiFile(midi_path)
    ticks_per_beat = mid.ticks_per_beat
    note_stack = {}
    note_events = []
    current_tick = 0
    max_tick = 0

    for msg in mid:
        current_tick += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            note_stack.setdefault(msg.note, []).append((current_tick, msg.channel))
        elif msg.type in ('note_off', 'note_on') and msg.velocity == 0:
            if note_stack.get(msg.note):
                start_tick, channel = note_stack[msg.note].pop(0)
                note_events.append({
                    "pitch": msg.note,
                    "on_tick": start_tick,
                    "off_tick": current_tick,
                    "channel": channel
                })
        max_tick = max(max_tick, current_tick)

    # ===>>> Use actual audio duration
    audio_duration_seconds = 207

    # Compute tempo so that max_tick maps to audio_duration
    tempo = int(audio_duration_seconds * 1_000_000 * ticks_per_beat / max_tick)
    ## print(f"Computed tempo to match audio: {tempo} μs per beat")

    # Convert tick values to seconds using computed tempo
    for note in note_events:
        note["on"] = tick2second(note["on_tick"], ticks_per_beat, tempo)
        note["off"] = tick2second(note["off_tick"], ticks_per_beat, tempo)
        del note["on_tick"]
        del note["off_tick"]

    note_events_df = pd.DataFrame(note_events)
    note_events_df = note_events_df.sort_values(by=["on", "channel", "pitch"], ascending=[True, False, True])

    return note_events_df

if __name__ == "__main__":
    midi_file_path = "bwv1006_ly_one_line.midi"
    df = extract_note_intervals(midi_file_path)
    output_file = "bwv1006_csv_midi_note_events.csv"
    df.to_csv(output_file, index=False)
    details = f"[ exported {len(df)} note events ]"
    print(f"💾 Saved: {output_file} {details}")

