from chordparser import chords_editor
from chordparser import scales_editor
from chordparser import keys_editor
from chordparser import notes_editor
import pytest


NE = notes_editor.NoteEditor()
KE = keys_editor.KeyEditor()
SE = scales_editor.ScaleEditor()
CE = chords_editor.ChordEditor()


@pytest.mark.parametrize(
    "value", [1, len, True, [], ()])
def test_chord_typeerror(value):
    with pytest.raises(TypeError):
        CE.create_chord(value)


@pytest.mark.parametrize(
    "value", ["1", "H", "\u266fG"])
def test_chord_valueerror(value):
    with pytest.raises(ValueError):
        CE.create_chord(value)


@pytest.mark.parametrize(
    "value, root", [
        ('C', NE.create_note('C')),
        ('E\u266f', NE.create_note('E\u266f')),
        ]
    )
def test_chord_root(value, root):
    new_chord = CE.create_chord(value)
    assert new_chord.root == root


@pytest.mark.parametrize(
    "string, quality", [
        ('C', 'major'),
        ('Cm', 'minor'),
        ('Cdim', 'diminished'),
        ('C+', 'augmented'),
        ('C7', 'dominant seventh'),
        ('C5', 'power'),
        ('c7', 'minor seventh'),
        ('Cminmaj9', 'minor-major ninth'),
        ('Caugmaj11', 'augmented-major eleventh'),
        ('Caugb13', 'augmented minor thirteenth'),
        ('Cmaj9', 'major ninth'),
        ('Cdim7', 'diminished seventh'),
        ('C\u00f87', 'half-diminished seventh'),
        ('Cm9', 'minor ninth'),
        ]
    )
def test_quality(string, quality):
    new_chord = CE.create_chord(string)
    assert new_chord.quality == quality


@pytest.mark.parametrize(
    "string, quality", [
        ('Cmb5', 'diminished'),
        ('CM7#5', 'augmented-major seventh'),
        ('Cmin7dim5', 'half-diminished seventh'),
        ]
    )
def test_quality_alt5(string, quality):
    new_chord = CE.create_chord(string)
    assert new_chord.quality == quality


@pytest.mark.parametrize(
    "string, sus", [
        ('Csus2', 2),
        ('Csus', 4),
        ('Csus4', 4),
        ('C', None),
        ]
    )
def test_sus(string, sus):
    c = CE.create_chord(string)
    assert c.sus == sus


@pytest.mark.parametrize(
    "string, add", [
        ('Cadd13', ['13']),
        ('cadd2#6', ['2', '\u266f6']),
        ('cminmaj9b11', ['\u266d11']),
        ('C', None),
        ]
    )
def test_add(string, add):
    c = CE.create_chord(string)
    assert c.add == add


def test_parse_error():
    with pytest.raises(SyntaxError):
        c = CE.create_chord('Cadd21')


@pytest.mark.parametrize(
    "string, bass", [
        ('C', None),
        ('C/G', NE.create_note('G')),
        ('C/G#', NE.create_note('G\u266f')),
        ]
    )
def test_bass(string, bass):
    c = CE.create_chord(string)
    assert c.bass == bass


@pytest.mark.parametrize(
    "degree, quality", [
        (7, 'diminished'),
        (4, 'major'),
        (6, 'minor'),
        ]
    )
def test_diatonic(degree, quality):
    s = SE.create_scale('C', 'major')
    c = CE.create_diatonic(s, degree)
    assert c.quality == quality


@pytest.mark.parametrize(
    "degree, quality", [
        (7, 'diminished'),
        (4, 'major'),
        (6, 'minor'),
        ]
    )
def test_diatonic_2(degree, quality):
    s = KE.create_key('C', 'major')
    c = CE.create_diatonic(s, degree)
    assert c.quality == quality


@pytest.mark.parametrize("degree", [0, len])
def test_diatonic_value_error(degree):
    s = SE.create_scale('C', 'major')
    with pytest.raises(ValueError):
        c = CE.create_diatonic(s, degree)


@pytest.mark.parametrize(
    "input, output", [
        ("hey", "hey"), (None, '')
        ]
    )
def test_xstr(input, output):
    assert CE._xstr(input) == output


def test_change_chord_error():
    with pytest.raises(TypeError):
        CE.change_chord(len)


def test_change_chord_root():
    o = CE.create_chord('C')
    n = CE.create_chord('D')
    assert n == CE.change_chord(o, root='D')


def test_change_chord_q():
    o = CE.create_chord('C')
    n = CE.create_chord('Cminmajb9')
    assert n == CE.change_chord(o, quality="minor-major minor ninth")


@pytest.mark.parametrize(
    "quality", [
        "powr", "power ninth", "major sixth", "augmented major ninth", "augmented minor tenth", "major minor ninth ten",
        ]
    )
def test_change_chord_q_error(quality):
    o = CE.create_chord('C')
    with pytest.raises(ValueError):
        CE.change_chord(o, quality=quality)


def test_change_chord_sus():
    o = CE.create_chord('Csus2')
    n = CE.create_chord('C')
    assert n == CE.change_chord(o, sus=False)


def test_change_chord_sus_error():
    o = CE.create_chord('C')
    with pytest.raises(ValueError):
        CE.change_chord(o, sus=3)


def test_change_chord_add():
    o = CE.create_chord('Cadd9')
    n = CE.create_chord('Caddb2add9')
    assert n == CE.change_chord(o, add=['b2'])


def test_change_chord_add_error():
    o = CE.create_chord('C')
    with pytest.raises(ValueError):
        CE.change_chord(o, add=['b22'])


def test_change_chord_rem():
    o = CE.create_chord('Caddb2')
    n = CE.create_chord('C')
    assert n == CE.change_chord(o, remove=['b2'])


def test_change_chord_rem_error():
    o = CE.create_chord('C')
    with pytest.raises(ValueError):
        CE.change_chord(o, remove=['b2'])


def test_change_chord_rem_error_2():
    o = CE.create_chord('Cb2')
    with pytest.raises(ValueError):
        CE.change_chord(o, remove=['b22'])


def test_change_chord_bass():
    o = CE.create_chord('Cadd9')
    n = CE.create_chord('Cadd9/G')
    assert n == CE.change_chord(o, bass='G')


def test_change_chord_bass_2():
    o = CE.create_chord('Cadd9/G')
    n = CE.create_chord('Cadd9')
    assert n == CE.change_chord(o, bass=False)
