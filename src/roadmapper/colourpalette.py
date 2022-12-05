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

DEFAULT_FONT = "Arial"
DEFAULT_TITLE_FONT_SIZE = 18
DEFAULT_TIMELINE_FONT_SIZE = 12
DEFAULT_MARKER_FONT_SIZE = 10
DEFAULT_GROUP_FONT_SIZE = 12
DEFAULT_TASK_FONT_SIZE = 12
DEFAULT_MILESTONE_FONT_SIZE = 12
DEFAULT_FOOTER_FONT_SIZE = 12


def get_default_scheme(roadmap_component: str):
    """Get default colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font (str): If roadmap_component is "title"
        title_font_size (int): If roadmap_component is "title"
        title_font_colour (str): If roadmap_component is "title"

        timeline_font (str): If roadmap_component is "timeline"
        timeline_font_size (int): If roadmap_component is "timeline"
        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font (str): If roadmap_component is "marker"
        marker_font_size (int): If roadmap_component is "marker"
        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font (str): If roadmap_component is "group"
        group_font_size (int): If roadmap_component is "group"
        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font (str): If roadmap_component is "task"
        task_font_size (int): If roadmap_component is "task"
        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font (str): If roadmap_component is "milestone"
        milestone_font_size (int): If roadmap_component is "milestone"
        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font (str): If roadmap_component is "footer"
        footer_font_size (int): If roadmap_component is "footer"
        footer_font_colour (str): If roadmap_component is "footer"
    """
    background_colour = "#FFFFFF"

    title_font = DEFAULT_FONT
    title_font_size = DEFAULT_TITLE_FONT_SIZE
    title_font_colour = "#000000"

    timeline_font = DEFAULT_FONT
    timeline_font_size = DEFAULT_TIMELINE_FONT_SIZE
    timeline_font_colour = "#FFFFFF"
    timeline_fill_colour = "#000000"

    marker_font = DEFAULT_FONT
    marker_font_size = DEFAULT_MARKER_FONT_SIZE
    marker_font_colour = "#000000"
    marker_line_colour = "#000000"

    group_font = DEFAULT_FONT
    group_font_size = DEFAULT_GROUP_FONT_SIZE
    group_font_colour = "#FFFFFF"
    group_fill_colour = "#000000"

    task_font = DEFAULT_FONT
    task_font_size = DEFAULT_TASK_FONT_SIZE
    task_font_colour = "#000000"
    task_fill_colour = "#D9D9D9"

    milestone_font = DEFAULT_FONT
    milestone_font_size = DEFAULT_MILESTONE_FONT_SIZE
    milestone_font_colour = "#FFFFFF"
    milestone_fill_colour = "#000000"

    footer_font = DEFAULT_FONT
    footer_font_size = DEFAULT_FOOTER_FONT_SIZE
    footer_font_colour = "#FFFFFF"

    match roadmap_component:
        case "background":
            return background_colour
        case "title":
            return title_font, title_font_size, title_font_colour
        case "timeline":
            return (
                timeline_font,
                timeline_font_size,
                timeline_font_colour,
                timeline_fill_colour,
            )
        case "marker":
            return marker_font, marker_font_size, marker_font_colour, marker_line_colour
        case "group":
            return group_font, group_font_size, group_font_colour, group_fill_colour
        case "task":
            return task_font, task_font_size, task_font_colour, task_fill_colour
        case "milestone":
            return (
                milestone_font,
                milestone_font_size,
                milestone_font_colour,
                milestone_fill_colour,
            )
        case "footer":
            return footer_font, footer_font_size, footer_font_colour
        case _:
            return None


def get_greywoof_scheme(roadmap_component: str):
    """Get "GREYWOOF" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font (str): If roadmap_component is "title"
        title_font_size (int): If roadmap_component is "title"
        title_font_colour (str): If roadmap_component is "title"

        timeline_font (str): If roadmap_component is "timeline"
        timeline_font_size (int): If roadmap_component is "timeline"
        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font (str): If roadmap_component is "marker"
        marker_font_size (int): If roadmap_component is "marker"
        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font (str): If roadmap_component is "group"
        group_font_size (int): If roadmap_component is "group"
        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font (str): If roadmap_component is "task"
        task_font_size (int): If roadmap_component is "task"
        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font (str): If roadmap_component is "milestone"
        milestone_font_size (int): If roadmap_component is "milestone"
        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font (str): If roadmap_component is "footer"
        footer_font_size (int): If roadmap_component is "footer"
        footer_font_colour (str): If roadmap_component is "footer"
    """
    background_colour = "#FFFFFF"
    title_font = DEFAULT_FONT
    title_font_size = DEFAULT_TITLE_FONT_SIZE
    title_font_colour = "#000000"

    timeline_font = DEFAULT_FONT
    timeline_font_size = DEFAULT_TIMELINE_FONT_SIZE
    timeline_font_colour = "#FFFFFF"
    timeline_fill_colour = "#666666"

    marker_font = DEFAULT_FONT
    marker_font_size = DEFAULT_MARKER_FONT_SIZE
    marker_font_colour = "#666666"
    marker_line_colour = "#666666"

    group_font = DEFAULT_FONT
    group_font_size = DEFAULT_GROUP_FONT_SIZE
    group_font_colour = "#FFFFFF"
    group_fill_colour = "#666666"

    task_font = DEFAULT_FONT
    task_font_size = DEFAULT_TASK_FONT_SIZE
    task_font_colour = "#000000"
    task_fill_colour = "#D9D9D9"

    milestone_font = DEFAULT_FONT
    milestone_font_size = DEFAULT_MILESTONE_FONT_SIZE
    milestone_font_colour = "#000000"
    milestone_fill_colour = "#B7B7B7"

    footer_font = DEFAULT_FONT
    footer_font_size = DEFAULT_FOOTER_FONT_SIZE
    footer_font_colour = "#000000"

    match roadmap_component:
        case "background":
            return background_colour
        case "title":
            return title_font, title_font_size, title_font_colour
        case "timeline":
            return (
                timeline_font,
                timeline_font_size,
                timeline_font_colour,
                timeline_fill_colour,
            )
        case "marker":
            return (
                marker_font,
                marker_font_size,
                marker_font_colour,
                marker_line_colour,
            )
        case "group":
            return group_font, group_font_size, group_font_colour, group_fill_colour
        case "task":
            return task_font, task_font_size, task_font_colour, task_fill_colour
        case "milestone":
            return (
                milestone_font,
                milestone_font_size,
                milestone_font_colour,
                milestone_fill_colour,
            )
        case "footer":
            return footer_font, footer_font_size, footer_font_colour
        case _:
            return None


def get_bluemountain_scheme(roadmap_component: str):
    """Get "BLUEMOUNTAIN" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font (str): If roadmap_component is "title"
        title_font_size (int): If roadmap_component is "title"
        title_font_colour (str): If roadmap_component is "title"

        timeline_font (str): If roadmap_component is "timeline"
        timeline_font_size (int): If roadmap_component is "timeline"
        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font (str): If roadmap_component is "marker"
        marker_font_size (int): If roadmap_component is "marker"
        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font (str): If roadmap_component is "group"
        group_font_size (int): If roadmap_component is "group"
        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font (str): If roadmap_component is "task"
        task_font_size (int): If roadmap_component is "task"
        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font (str): If roadmap_component is "milestone"
        milestone_font_size (int): If roadmap_component is "milestone"
        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font (str): If roadmap_component is "footer"
        footer_font_size (int): If roadmap_component is "footer"
        footer_font_colour (str): If roadmap_component is "footer"
    """
    background_colour = "#FFFFFF"
    title_font = DEFAULT_FONT
    title_font_size = DEFAULT_TITLE_FONT_SIZE
    title_font_colour = "#0B5394"

    timeline_font = DEFAULT_FONT
    timeline_font_size = DEFAULT_TIMELINE_FONT_SIZE
    timeline_font_colour = "#FFFFFF"
    timeline_fill_colour = "#0B5394"

    marker_font = DEFAULT_FONT
    marker_font_size = DEFAULT_MARKER_FONT_SIZE
    marker_font_colour = "#0B5394"
    marker_line_colour = "#0B5394"

    group_font = DEFAULT_FONT
    group_font_size = DEFAULT_GROUP_FONT_SIZE
    group_font_colour = "#FFFFFF"
    group_fill_colour = "#0B5394"

    task_font = DEFAULT_FONT
    task_font_size = DEFAULT_TASK_FONT_SIZE
    task_font_colour = "#000000"
    task_fill_colour = "#9FC5E8"

    milestone_font = DEFAULT_FONT
    milestone_font_size = DEFAULT_MILESTONE_FONT_SIZE
    milestone_font_colour = "#0B5394"
    milestone_fill_colour = "#3D85C6"

    footer_font = DEFAULT_FONT
    footer_font_size = DEFAULT_FOOTER_FONT_SIZE
    footer_font_colour = "#0B5394"

    match roadmap_component:
        case "background":
            return background_colour
        case "title":
            return title_font, title_font_size, title_font_colour
        case "timeline":
            return (
                timeline_font,
                timeline_font_size,
                timeline_font_colour,
                timeline_fill_colour,
            )
        case "marker":
            return (
                marker_font,
                marker_font_size,
                marker_font_colour,
                marker_line_colour,
            )
        case "group":
            return group_font, group_font_size, group_font_colour, group_fill_colour
        case "task":
            return task_font, task_font_size, task_font_colour, task_fill_colour
        case "milestone":
            return (
                milestone_font,
                milestone_font_size,
                milestone_font_colour,
                milestone_fill_colour,
            )
        case "footer":
            return footer_font, footer_font_size, footer_font_colour
        case _:
            return None


def get_orangepeel_scheme(roadmap_component: str):
    """Get "ORANGEPEEL" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font (str): If roadmap_component is "title"
        title_font_size (int): If roadmap_component is "title"
        title_font_colour (str): If roadmap_component is "title"

        timeline_font (str): If roadmap_component is "timeline"
        timeline_font_size (int): If roadmap_component is "timeline"
        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font (str): If roadmap_component is "marker"
        marker_font_size (int): If roadmap_component is "marker"
        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font (str): If roadmap_component is "group"
        group_font_size (int): If roadmap_component is "group"
        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font (str): If roadmap_component is "task"
        task_font_size (int): If roadmap_component is "task"
        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font (str): If roadmap_component is "milestone"
        milestone_font_size (int): If roadmap_component is "milestone"
        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font (str): If roadmap_component is "footer"
        footer_font_size (int): If roadmap_component is "footer"
        footer_font_colour (str): If roadmap_component is "footer"
    """
    background_colour = "#FFFFFF"
    title_font = DEFAULT_FONT
    title_font_size = DEFAULT_TITLE_FONT_SIZE
    title_font_colour = "#B45F06"

    timeline_font = DEFAULT_FONT
    timeline_font_size = DEFAULT_TIMELINE_FONT_SIZE
    timeline_font_colour = "#FFFFFF"
    timeline_fill_colour = "#B45F06"

    marker_font = DEFAULT_FONT
    marker_font_size = DEFAULT_MARKER_FONT_SIZE
    marker_font_colour = "#B45F06"
    marker_line_colour = "#B45F06"

    group_font = DEFAULT_FONT
    group_font_size = DEFAULT_GROUP_FONT_SIZE
    group_font_colour = "#FFFFFF"
    group_fill_colour = "#B45F06"

    task_font = DEFAULT_FONT
    task_font_size = DEFAULT_TASK_FONT_SIZE
    task_font_colour = "#000000"
    task_fill_colour = "#F6B26B"

    milestone_font = DEFAULT_FONT
    milestone_font_size = DEFAULT_MILESTONE_FONT_SIZE
    milestone_font_colour = "#B45F06"
    milestone_fill_colour = "#B45F06"

    footer_font = DEFAULT_FONT
    footer_font_size = DEFAULT_FOOTER_FONT_SIZE
    footer_font_colour = "#B45F06"

    match roadmap_component:
        case "background":
            return background_colour
        case "title":
            return title_font, title_font_size, title_font_colour
        case "timeline":
            return (
                timeline_font,
                timeline_font_size,
                timeline_font_colour,
                timeline_fill_colour,
            )
        case "marker":
            return (
                marker_font,
                marker_font_size,
                marker_font_colour,
                marker_line_colour,
            )
        case "group":
            return group_font, group_font_size, group_font_colour, group_fill_colour
        case "task":
            return task_font, task_font_size, task_font_colour, task_fill_colour
        case "milestone":
            return (
                milestone_font,
                milestone_font_size,
                milestone_font_colour,
                milestone_fill_colour,
            )
        case "footer":
            return footer_font, footer_font_size, footer_font_colour
        case _:
            return None


def get_greenturtle_scheme(roadmap_component: str):
    """Get "GREENTURTLE" colour scheme

    Args:
        roadmap_component (str): The component of the roadmap to get the colour scheme for

    Returns:
        background_colour (str): If roadmap_component is "background"

        title_font (str): If roadmap_component is "title"
        title_font_size (int): If roadmap_component is "title"
        title_font_colour (str): If roadmap_component is "title"

        timeline_font (str): If roadmap_component is "timeline"
        timeline_font_size (int): If roadmap_component is "timeline"
        timeline_font_colour (str): If roadmap_component is "timeline"
        timeline_fill_colour (str): If roadmap_component is "timeline"

        marker_font (str): If roadmap_component is "marker"
        marker_font_size (int): If roadmap_component is "marker"
        marker_font_colour (str): If roadmap_component is "marker"
        marker_line_colour (str): If roadmap_component is "marker"

        group_font (str): If roadmap_component is "group"
        group_font_size (int): If roadmap_component is "group"
        group_font_colour (str): If roadmap_component is "group"
        group_fill_colour (str): If roadmap_component is "group"

        task_font (str): If roadmap_component is "task"
        task_font_size (int): If roadmap_component is "task"
        task_font_colour (str): If roadmap_component is "task"
        task_fill_colour (str): If roadmap_component is "task"

        milestone_font (str): If roadmap_component is "milestone"
        milestone_font_size (int): If roadmap_component is "milestone"
        milestone_font_colour (str): If roadmap_component is "milestone"
        milestone_fill_colour (str): If roadmap_component is "milestone"

        footer_font (str): If roadmap_component is "footer"
        footer_font_size (int): If roadmap_component is "footer"
        footer_font_colour (str): If roadmap_component is "footer"
    """
    background_colour = "#FFFFFF"
    title_font = DEFAULT_FONT
    title_font_size = DEFAULT_TITLE_FONT_SIZE
    title_font_colour = "#38761D"

    timeline_font = DEFAULT_FONT
    timeline_font_size = DEFAULT_TIMELINE_FONT_SIZE
    timeline_font_colour = "#FFFFFF"
    timeline_fill_colour = "#38761D"

    marker_font = DEFAULT_FONT
    marker_font_size = DEFAULT_MARKER_FONT_SIZE
    marker_font_colour = "#38761D"
    marker_line_colour = "#38761D"

    group_font = DEFAULT_FONT
    group_font_size = DEFAULT_GROUP_FONT_SIZE
    group_font_colour = "#FFFFFF"
    group_fill_colour = "#38761D"

    task_font = DEFAULT_FONT
    task_font_size = DEFAULT_TASK_FONT_SIZE
    task_font_colour = "#000000"
    task_fill_colour = "#93C47D"

    milestone_font = DEFAULT_FONT
    milestone_font_size = DEFAULT_MILESTONE_FONT_SIZE
    milestone_font_colour = "#38761D"
    milestone_fill_colour = "#38761D"

    footer_font = DEFAULT_FONT
    footer_font_size = DEFAULT_FOOTER_FONT_SIZE
    footer_font_colour = "#38761D"

    match roadmap_component:
        case "background":
            return background_colour
        case "title":
            return title_font, title_font_size, title_font_colour
        case "timeline":
            return (
                timeline_font,
                timeline_font_size,
                timeline_font_colour,
                timeline_fill_colour,
            )
        case "marker":
            return (
                marker_font,
                marker_font_size,
                marker_font_colour,
                marker_line_colour,
            )
        case "group":
            return group_font, group_font_size, group_font_colour, group_fill_colour
        case "task":
            return task_font, task_font_size, task_font_colour, task_fill_colour
        case "milestone":
            return (
                milestone_font,
                milestone_font_size,
                milestone_font_colour,
                milestone_fill_colour,
            )
        case "footer":
            return footer_font, footer_font_size, footer_font_colour
        case _:
            return None


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

            title_font (str): If roadmap_component is "title"
            title_font_size (int): If roadmap_component is "title"
            title_font_colour (str): If roadmap_component is "title"

            timeline_font (str): If roadmap_component is "timeline"
            timeline_font_size (int): If roadmap_component is "timeline"
            timeline_font_colour (str): If roadmap_component is "timeline"
            timeline_fill_colour (str): If roadmap_component is "timeline"

            marker_font (str): If roadmap_component is "marker"
            marker_font_size (int): If roadmap_component is "marker"
            marker_font_colour (str): If roadmap_component is "marker"
            marker_line_colour (str): If roadmap_component is "marker"

            group_font (str): If roadmap_component is "group"
            group_font_size (int): If roadmap_component is "group"
            group_font_colour (str): If roadmap_component is "group"
            group_fill_colour (str): If roadmap_component is "group"

            task_font (str): If roadmap_component is "task"
            task_font_size (int): If roadmap_component is "task"
            task_font_colour (str): If roadmap_component is "task"
            task_fill_colour (str): If roadmap_component is "task"

            milestone_font (str): If roadmap_component is "milestone"
            milestone_font_size (int): If roadmap_component is "milestone"
            milestone_font_colour (str): If roadmap_component is "milestone"
            milestone_fill_colour (str): If roadmap_component is "milestone"

            footer_font (str): If roadmap_component is "footer"
            footer_font_size (int): If roadmap_component is "footer"
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
