import pytest

from src.roadmapper.alignment import Alignment, AlignmentDirection, OffsetType


@pytest.mark.unit
def test_case_insensitivity():
    assert AlignmentDirection["center"] == AlignmentDirection.CENTER
    assert AlignmentDirection["LEFT"] == AlignmentDirection.LEFT
    assert OffsetType["unit"] == OffsetType.UNIT


@pytest.mark.unit
def test_enum_direction_synonyms():
    assert AlignmentDirection.CENTRE == AlignmentDirection.CENTER


@pytest.mark.unit
def test_alignment_from_string():
    alignment = Alignment.from_value("left:50%")
    assert alignment.direction == AlignmentDirection.LEFT
    assert alignment.offset_type == OffsetType.PERCENT
    assert alignment.offset == 0.5


@pytest.mark.unit
def test_from_string():
    alignment = Alignment.from_string("right:30%")
    assert alignment.direction == AlignmentDirection.RIGHT
    assert alignment.offset_type == OffsetType.PERCENT
    assert alignment.offset == 0.3


@pytest.mark.unit
def test_from_alignment():
    alignment = Alignment(direction=AlignmentDirection.LEFT)
    new_alignment = Alignment.from_alignment(alignment)
    assert new_alignment.direction == AlignmentDirection.LEFT


@pytest.mark.unit
def test_parse_offset():
    offset, offset_type = Alignment.parse_offset("50%")
    assert offset == 0.5
    assert offset_type == OffsetType.PERCENT

    offset, offset_type = Alignment.parse_offset("30")
    assert offset == 30
    assert offset_type == OffsetType.UNIT


@pytest.mark.unit
def test_update_from_alignment_string():
    alignment = Alignment()
    alignment.update_from_alignment_string("centre:20%")
    assert alignment.direction == AlignmentDirection.CENTRE
    assert alignment.offset_type == OffsetType.PERCENT
    assert alignment.offset == 0.2


@pytest.mark.unit
def test_alignment_from_alignment_object():
    original_alignment = Alignment(
        direction=AlignmentDirection.RIGHT, offset_type=OffsetType.UNIT, offset=10
    )
    new_alignment = Alignment.from_value(original_alignment)
    assert new_alignment.direction == AlignmentDirection.RIGHT
    assert new_alignment.offset_type == OffsetType.UNIT
    assert new_alignment.offset == 10


@pytest.mark.unit
def test_as_tuple():
    alignment = Alignment(
        direction=AlignmentDirection.RIGHT, offset_type=OffsetType.UNIT, offset=15
    )
    assert alignment.as_tuple() == (AlignmentDirection.RIGHT, OffsetType.UNIT, 15)


@pytest.mark.unit
def test_percent_of():
    alignment = Alignment(offset_type=OffsetType.PERCENT, offset=0.5)
    assert alignment.percent_of(100) == 50

    alignment = Alignment(offset_type=OffsetType.UNIT, offset=30)
    with pytest.raises(ValueError):
        alignment.percent_of(100)


@pytest.mark.unit
def test_invalid_direction():
    with pytest.raises(ValueError):
        Alignment.from_value("widdershins:50")


@pytest.mark.unit
def test_invalid_type():
    with pytest.raises(ValueError):
        Alignment.from_value(1)


@pytest.mark.unit
def test_str_method():
    alignment = Alignment(
        direction=AlignmentDirection.LEFT, offset_type=OffsetType.PERCENT, offset=0.25
    )
    assert str(alignment) == "left:25.0%"

    alignment = Alignment(
        direction=AlignmentDirection.RIGHT, offset_type=OffsetType.UNIT, offset=10
    )
    assert str(alignment) == "right:10"
