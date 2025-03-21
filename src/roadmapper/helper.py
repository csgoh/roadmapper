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
import inspect
import logging
import uuid
from rich.console import Console
from rich.panel import Panel


class Helper:
    show_timeline = True
    show_group = False
    show_task = True
    show_parallel_task = False
    show_milestone = True
    show_marker = False
    show_title = False
    show_header = False
    show_footer = False
    show_logo = False

    @staticmethod
    def should_show_message(show_level: str) -> bool:
        return (
            (show_level == "group" and Helper.show_group)
            or (show_level == "task" and Helper.show_task)
            or (show_level == "parallel_task" and Helper.show_parallel_task)
            or (show_level == "milestone" and Helper.show_milestone)
            or (show_level == "marker" and Helper.show_marker)
            or (show_level == "title" and Helper.show_title)
            or (show_level == "header" and Helper.show_header)
            or (show_level == "footer" and Helper.show_footer)
            or (show_level == "logo" and Helper.show_logo)
            or (show_level == "timeline" and Helper.show_timeline)
        )

    @staticmethod
    def printc(
        message: str,
        color: str = "30",
        reverse: bool = False,
        end: str = "\n",
        rich_type: str = "text",
        show_level: str = "general",
        true_condition: bool = True,
    ):
        """Print text in color"""

        root_logger = logging.getLogger()

        call_depth = len(inspect.stack())

        if call_depth < 5:
            call_depth = 0
        else:
            call_depth -= 5

        caller = inspect.stack()[1].function

        # determine the caller class name
        if "self" in inspect.stack()[1].frame.f_locals:
            caller_class = inspect.stack()[1].frame.f_locals["self"].__class__.__name__

        # add \t tab to the print message if for each level of call depth
        message = "\t" * call_depth + message

        if (
            root_logger.getEffectiveLevel() == logging.DEBUG
            and Helper.should_show_message(show_level)
            and true_condition
        ):
            console = Console()
            if rich_type == "text":
                style_attribute = "reverse" if reverse else ""
                console.print(
                    f"{caller_class}.{caller}(): {message}",
                    end=end,
                    style=style_attribute,
                )
            elif rich_type == "panel":
                console.print(Panel(message), style="blue")

    @staticmethod
    def print_info(message: str, color: str = "30", end: str = "\n"):
        """Print text in color"""

        root_logger = logging.getLogger()

        if root_logger.getEffectiveLevel() == logging.INFO:
            console = Console()
            console.print(f"\033[{message}\033", end=end)

    @staticmethod
    def debug_log(message: str):
        """Log debug message"""
        logging.debug(message)

    @staticmethod
    def info_log(message: str):
        """Log info message"""
        logging.info(message)

    @staticmethod
    def get_uuid(prefix: str = "PIPER"):
        # replace uuid '-' with '_'
        uuid_str = str(uuid.uuid4()).replace("-", "_")
        # shorten to 8 chars
        uuid_str = uuid_str[:8]
        prefix = "".join(e for e in prefix if e.isalnum() or e == "_")
        return f"{prefix.upper()}_{uuid_str}"
