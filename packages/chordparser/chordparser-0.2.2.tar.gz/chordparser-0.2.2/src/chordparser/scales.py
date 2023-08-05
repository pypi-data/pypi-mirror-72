from chordparser.notes_editor import NoteEditor
from chordparser.keys import Key


class Scale:
    """
    Scale class that composes of a Key and Notes.

    The Scale class accepts a Key and generates a 2-octave Note tuple in its 'notes' attribute. The Scale can be changed by transposing its key using the 'transpose' method.
    """
    _heptatonic_base = (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)
    _SCALES = {
        "major": 0,
        "ionian": 0,
        "dorian": 1,
        "phrygian": 2,
        "lydian": 3,
        "mixolydian": 4,
        "aeolian": 5,
        "minor": 5,
        "locrian": 6,
        }
    _SCALE_DEGREE = {
        0: "ionian",
        1: "dorian",
        2: "phrygian",
        3: "lydian",
        4: "mixolydian",
        5: "aeolian",
        6: "locrian",
    }
    _submodes = {
        None: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "natural": (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "melodic": (0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 0, -1),
        "harmonic": (0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 1, -1),
    }
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B')
    NE = NoteEditor()

    def __init__(self, key: Key):
        self.key = key
        self.build()

    def build(self):
        """Build the scale from its key."""
        self.notes = self._get_notes()

    def _get_notes(self):
        """Get notes in the scale."""
        self.scale_intervals = self._get_scale_intervals()
        note_no_symbol = self.NE.create_note(self.key.letter())
        self._idx = Scale._notes_tuple.index(note_no_symbol)
        self._note_order = self._get_note_order()
        notes = self._shift_notes()
        return notes

    def _get_scale_intervals(self):
        """Get note-by-note intervals in the scale."""
        intervals = self._get_intervals(self.key.mode)
        # Account for submode
        submode_intervals = Scale._submodes.get(self.key.submode)
        scale_intervals = []
        for scale, subm in zip(intervals, submode_intervals):
            scale_intervals.append(scale + subm)
        return tuple(scale_intervals)

    def _get_intervals(self, mode):
        """Get intervals based on mode."""
        shift = Scale._SCALES[mode]
        intervals = (
            Scale._heptatonic_base[shift:]
            + Scale._heptatonic_base[:shift]
            )
        return intervals

    def _get_note_order(self):
        """Re-arrange note order based on key."""
        note_order = (
            Scale._notes_tuple[self._idx:]
            + Scale._notes_tuple[:self._idx]
            )
        return note_order

    def _shift_notes(self):
        """Shift notes with reference to original mode intervals."""
        base_intervals = self._get_intervals(
                Scale._SCALE_DEGREE[self._idx]
                )
        symbol_increment = self.key.symbolvalue()
        note_list = []
        for num, note in enumerate(self._note_order):
            new_note = self.NE.create_note(note)
            total_increment = (
                symbol_increment
                + sum(self.scale_intervals[:num])
                - sum(base_intervals[:num])
                )
            new_note.shift_s(total_increment)
            note_list.append(new_note)
        return tuple(note_list)

    def transpose(self, semitones: int, letter: int):
        """Transpose the key of the scale."""
        self.key.transpose(semitones, letter)
        self.build()
        return self

    def __repr__(self):
        return f'{self.key} scale'

    def __eq__(self, other):
        # Allow comparison between Keys by checking their basic attributes
        if not isinstance(other, Scale):
            return NotImplemented
        return self.key == other.key
