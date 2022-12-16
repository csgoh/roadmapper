# MIT License

# Copyright (c) 2022 CS Goh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from dataclasses import dataclass, field

### Font :
# "Microsoft YaHei UI"
# "DengXian"
# "Segoe UI"
# "Tahoma"
# "Microsoft Jhenghei"

DEFAULT_FONT = "arial.ttf"
DEFAULT_TITLE_FONT_SIZE = 26
DEFAULT_SUBTITLE_FONT_SIZE = 18
DEFAULT_TIMELINE_FONT_SIZE = 12
DEFAULT_MARKER_FONT_SIZE = 12
DEFAULT_GROUP_FONT_SIZE = 12
DEFAULT_TASK_FONT_SIZE = 10
DEFAULT_MILESTONE_FONT_SIZE = 10
DEFAULT_FOOTER_FONT_SIZE = 13


class ColourSettings:
    background_colour: str = "#FFFFFF"

    title_font: str = DEFAULT_FONT
    title_font_size: int = DEFAULT_TITLE_FONT_SIZE
    title_font_colour: str = "#000000"

    subtitle_font: str = DEFAULT_FONT
    subtitle_font_size: int = DEFAULT_SUBTITLE_FONT_SIZE
    subtitle_font_colour: str = "#000000"

    timeline_font: str = DEFAULT_FONT
    timeline_font_size: int = DEFAULT_TIMELINE_FONT_SIZE
    timeline_font_colour: str = "#FFFFFF"
    timeline_fill_colour: str = "#000000"

    marker_font: str = DEFAULT_FONT
    marker_font_size: int = DEFAULT_MARKER_FONT_SIZE
    marker_font_colour: str = "#000000"
    marker_line_colour: str = "#000000"

    group_font: str = DEFAULT_FONT
    group_font_size: int = DEFAULT_GROUP_FONT_SIZE
    group_font_colour: str = "#FFFFFF"
    group_fill_colour: str = "#000000"

    task_font: str = DEFAULT_FONT
    task_font_size: int = DEFAULT_TASK_FONT_SIZE
    task_font_colour: str = "#000000"
    task_fill_colour: str = "#D9D9D9"

    milestone_font: str = DEFAULT_FONT
    milestone_font_size: int = DEFAULT_MILESTONE_FONT_SIZE
    milestone_font_colour: str = "#FFFFFF"
    milestone_fill_colour: str = "#000000"

    footer_font: str = DEFAULT_FONT
    footer_font_size: int = DEFAULT_FOOTER_FONT_SIZE
    footer_font_colour: str = "#000000"

    def get_colour_settings(self, roadmap_component: str):
        match roadmap_component:
            case "background":
                return self.background_colour
            case "title":
                return (
                    self.title_font,
                    self.title_font_size,
                    self.title_font_colour,
                    self.subtitle_font,
                    self.subtitle_font_size,
                    self.subtitle_font_colour,
                )
            case "timeline":
                return (
                    self.timeline_font,
                    self.timeline_font_size,
                    self.timeline_font_colour,
                    self.timeline_fill_colour,
                )
            case "marker":
                return (
                    self.marker_font,
                    self.marker_font_size,
                    self.marker_font_colour,
                    self.marker_line_colour,
                )
            case "group":
                return (
                    self.group_font,
                    self.group_font_size,
                    self.group_font_colour,
                    self.group_fill_colour,
                )
            case "task":
                return (
                    self.task_font,
                    self.task_font_size,
                    self.task_font_colour,
                    self.task_fill_colour,
                )
            case "milestone":
                return (
                    self.milestone_font,
                    self.milestone_font_size,
                    self.milestone_font_colour,
                    self.milestone_fill_colour,
                )
            case "footer":
                return self.footer_font, self.footer_font_size, self.footer_font_colour
            case _:
                return None


def get_default_scheme(roadmap_component: str):
    """Get default colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font_colour (str): If roadmap_component is "title"
        subtitle_font_colour (str): If roadmap_component is "title"

        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font_colour (str): If roadmap_component is "footer"
    """
    settings = ColourSettings()
    return settings.get_colour_settings(roadmap_component)


def get_greywoof_scheme(roadmap_component: str):
    """Get "GREYWOOF" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font_colour (str): If roadmap_component is "title"
        subtitle_font_colour (str): If roadmap_component is "title"

        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font_colour (str): If roadmap_component is "footer"
    """
    settings = ColourSettings()
    settings.background_colour = "#FFFFFF"

    settings.title_font_colour = "#000000"
    settings.subtitle_font_colour = "#000000"

    settings.timeline_font_colour = "#FFFFFF"
    settings.timeline_fill_colour = "#666666"

    settings.marker_font_colour = "#666666"
    settings.marker_line_colour = "#666666"

    settings.group_font_colour = "#FFFFFF"
    settings.group_fill_colour = "#666666"

    settings.task_font_colour = "#000000"
    settings.task_fill_colour = "#D9D9D9"

    settings.milestone_font_colour = "#000000"
    settings.milestone_fill_colour = "#B7B7B7"

    settings.footer_font_colour = "#000000"

    return settings.get_colour_settings(roadmap_component)


def get_bluemountain_scheme(roadmap_component: str):
    """Get "BLUEMOUNTAIN" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font_colour (str): If roadmap_component is "title"
        subtitle_font_colour (str): If roadmap_component is "title"

        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font_colour (str): If roadmap_component is "footer"
    """
    settings = ColourSettings()
    settings.background_colour = "#FFFFFF"

    settings.title_font_colour = "#0B5394"
    settings.subtitle_font_colour = "#0B5394"

    settings.timeline_font_colour = "#FFFFFF"
    settings.timeline_fill_colour = "#0B5394"

    settings.marker_font_colour = "#0B5394"
    settings.marker_line_colour = "#0B5394"

    settings.group_font_colour = "#FFFFFF"
    settings.group_fill_colour = "#0B5394"

    settings.task_font_colour = "#000000"
    settings.task_fill_colour = "#9FC5E8"

    settings.milestone_font_colour = "#0B5394"
    settings.milestone_fill_colour = "#3D85C6"

    settings.footer_font_colour = "#0B5394"

    return settings.get_colour_settings(roadmap_component)


def get_orangepeel_scheme(roadmap_component: str):
    """Get "ORANGEPEEL" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font_colour (str): If roadmap_component is "title"
        subtitle_font_colour (str): If roadmap_component is "title"

        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font_colour (str): If roadmap_component is "footer"
    """
    settings = ColourSettings()
    settings.background_colour = "#FFFFFF"

    settings.title_font_colour = "#B45F06"
    settings.subtitle_font_colour = "#B45F06"

    settings.timeline_font_colour = "#FFFFFF"
    settings.timeline_fill_colour = "#B45F06"

    settings.marker_font_colour = "#B45F06"
    settings.marker_line_colour = "#B45F06"

    settings.group_font_colour = "#FFFFFF"
    settings.group_fill_colour = "#B45F06"

    settings.task_font_colour = "#000000"
    settings.task_fill_colour = "#F6B26B"

    settings.milestone_font_colour = "#B45F06"
    settings.milestone_fill_colour = "#B45F06"

    settings.footer_font_colour = "#B45F06"

    return settings.get_colour_settings(roadmap_component)


def get_greenturtle_scheme(roadmap_component: str):
    """Get "GREENTURTLE" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font_colour (str): If roadmap_component is "title"
        subtitle_font_colour (str): If roadmap_component is "title"

        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font_colour (str): If roadmap_component is "footer"
    """
    settings = ColourSettings()
    settings.background_colour = "#FFFFFF"

    settings.title_font_colour = "#38761D"
    settings.subtitle_font_colour = "#38761D"

    settings.timeline_font_colour = "#FFFFFF"
    settings.timeline_fill_colour = "#38761D"

    settings.marker_font_colour = "#38761D"
    settings.marker_line_colour = "#38761D"

    settings.group_font_colour = "#FFFFFF"
    settings.group_fill_colour = "#38761D"

    settings.task_font_colour = "#000000"
    settings.task_fill_colour = "#93C47D"

    settings.milestone_font_colour = "#38761D"
    settings.milestone_fill_colour = "#38761D"

    settings.footer_font_colour = "#38761D"

    return settings.get_colour_settings(roadmap_component)


@dataclass
class ColourTheme:
    """Colour theme for the Roadmapper."""

    def __init__(self, colour_theme_name: str) -> None:
        """Initialise the colour theme."""
        if colour_theme_name not in [
            "DEFAULT",
            "GREYWOOF",
            "BLUEMOUNTAIN",
            "ORANGEPEEL",
            "GREENTURTLE",
        ]:
            ValueError(f"Colour theme {colour_theme_name} not recognised.")
        self._colour_theme_name = colour_theme_name

    def get_colour_theme_settings(self, roadmap_component: str):
        """Get the colour theme settings for the specified roadmap component.

        Args:
            roadmap_component (str): Roadmap component to get the colour theme settings for.
                                        Components are: "background", "title", "timeline", "marker", "group", "task", "milestone", "footer"

        Returns:
            background_colour (str): If roadmap_component is "background"

        title_font_colour (str): If roadmap_component is "title"
        subtitle_font_colour (str): If roadmap_component is "title"

        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font_colour (str): If roadmap_component is "footer"
        """
        if self._colour_theme_name == "DEFAULT":
            return get_default_scheme(roadmap_component)
        elif self._colour_theme_name == "GREYWOOF":
            return get_greywoof_scheme(roadmap_component)
        elif self._colour_theme_name == "BLUEMOUNTAIN":
            return get_bluemountain_scheme(roadmap_component)
        elif self._colour_theme_name == "ORANGEPEEL":
            return get_orangepeel_scheme(roadmap_component)
        elif self._colour_theme_name == "GREENTURTLE":
            return get_greenturtle_scheme(roadmap_component)
        else:
            return None
