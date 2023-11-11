import pytest
from datetime import datetime
from src.roadmapper.milestone import Milestone


class MockPainter:
    def __init__(self):
        self.drawn_diamond = []
        self.drawn_text = []

    def draw_diamond(self, x, y, width, height, colour):
        self.drawn_diamond.append(("diamond", x, y, width, height, colour))

    @property
    def diamond_count(self):
        return len(self.drawn_diamond)

    @property
    def last_diamond(self):
        return self.drawn_diamond[-1]

    def draw_text(self, x, y, text, font, font_size, font_colour):
        self.drawn_text.append(("text", x, y, text, font, font_size, font_colour))

    @property
    def text_count(self):
        return len(self.drawn_text)

    @property
    def last_text(self):
        return self.drawn_text[-1]

    def get_text_dimension(self, text, font, font_size):
        # Return a mock dimension.
        return (100, 100)


@pytest.mark.unit
@pytest.fixture(scope="function")
def milestone():
    milestone = Milestone(
        text="Test",
        date=datetime.now(),
        font="Arial",
        font_size=12,
        font_colour="black",
        fill_colour="white",
        text_alignment="centre",
    )
    milestone.diamond_x = 200
    milestone.diamond_y = 200
    milestone.text_x = 200
    milestone.text_y = 200
    return milestone


@pytest.mark.unit
@pytest.fixture(scope="function")
def painter():
    return MockPainter()


# Text test cases
@pytest.mark.parametrize("text_alignment", [None, "centre"])
def test_draw_milestone_centre_alignment(milestone, painter, text_alignment):
    milestone.text_alignment = text_alignment
    milestone.draw(painter)
    assert painter.text_count > 0
    assert painter.last_text == ("text", 200, 200, "Test", "Arial", 12, "black")


@pytest.mark.unit
@pytest.mark.parametrize(
    "text_alignment, expected_x",
    [("left", 150), ("Left:199", 1), ("left:90%", 110)],
)
def test_draw_milestone_left_alignment(milestone, painter, text_alignment, expected_x):
    milestone.text_alignment = text_alignment
    milestone.draw(painter)
    assert painter.text_count > 0
    assert painter.last_text == ("text", expected_x, 200, "Test", "Arial", 12, "black")


@pytest.mark.unit
@pytest.mark.parametrize(
    "text_alignment, expected_x",
    [("right", 250), ("Right:1", 201), ("right:90%", 290)],
)
def test_draw_milestone_right_alignment(milestone, painter, text_alignment, expected_x):
    milestone.text_alignment = text_alignment
    milestone.draw(painter)
    assert painter.text_count > 0
    assert painter.last_text == ("text", expected_x, 200, "Test", "Arial", 12, "black")


@pytest.mark.unit
@pytest.mark.parametrize("invalid_alignment", ["top", "bottom", "diagonal"])
def test_invalid_text_alignment(milestone, invalid_alignment):
    milestone.text_alignment = invalid_alignment
    with pytest.raises(ValueError):
        milestone.draw(MockPainter())
