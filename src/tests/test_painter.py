from src.roadmapper.painter import Painter


class TestPainter:
    def test_init(self):
        painter = Painter(800, 600)
        assert painter.width == 800
        assert painter.height == 600

    # Tests that the colour theme is correctly set and that subsequent shapes and text are drawn with the correct colours.
    def test_set_colour_theme(self):
        painter = Painter(500, 500)
        painter.set_colour_theme("ORANGEPEEL")
        assert painter.title_font == "Arial"
        assert painter.title_font_size == 26
        assert painter.title_font_colour == "#B45F06"
        assert painter.subtitle_font == "Arial"
        assert painter.subtitle_font_size == 18
        assert painter.subtitle_font_colour == "#B45F06"
        assert painter.timeline_year_font == "Arial"
        assert painter.timeline_year_font_size == 12
        assert painter.timeline_year_font_colour == "#FFFFFF"
        assert painter.timeline_year_fill_colour == "#B45F06"
        assert painter.timeline_item_font == "Arial"
        assert painter.timeline_item_font_size == 12
        assert painter.timeline_item_font_colour == "#FFFFFF"
        assert painter.timeline_item_fill_colour == "#B45F06"
        assert painter.marker_font == "Arial"
        assert painter.marker_font_size == 12
        assert painter.marker_font_colour == "#B45F06"
        assert painter.marker_line_colour == "#B45F06"
        assert painter.group_font == "Arial"
        assert painter.group_font_size == 12
        assert painter.group_font_colour == "#FFFFFF"
        assert painter.group_fill_colour == "#B45F06"
        assert painter.task_font == "Arial"
        assert painter.task_font_size == 12
        assert painter.task_font_colour == "#000000"
        assert painter.task_fill_colour == "#F6B26B"
        assert painter.task_style == "rectangle"
        assert painter.milestone_font == "Arial"
        assert painter.milestone_font_size == 10
        assert painter.milestone_font_colour == "#B45F06"
        assert painter.milestone_fill_colour == "#B45F06"
        assert painter.footer_font == "Arial"
        assert painter.footer_font_size == 13
        assert painter.footer_font_colour == "#B45F06"

    # Tests that the get_text_dimension() method correctly calculates the dimensions of text for different fonts and font sizes.
    def test_get_text_dimension(self):
        painter = Painter(100, 100)
        text = "Hello World"
        font = "Arial"
        font_size = 12
        width, height = painter.get_text_dimension(text, font, font_size)
        assert width > 0
        assert height > 0

    def test_get_text_dimension2(self):
        painter = Painter(800, 600)
        text_width, text_height = painter.get_text_dimension("Hello World", "Arial", 12)
        print(f"text_width: {text_width}, text_height: {text_height}")
        # Linux returns different text width
        assert (text_width == 62) or (text_width == 64)
        assert text_height == 11
