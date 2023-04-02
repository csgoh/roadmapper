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

from dataclasses import dataclass
import json
import os
import locale

default_timeline_locale_settings = {
    "locale": "en_US",
    "settings": {
        "year": {
            "text": "Year {0}",
            "generic_text": "Year {0}",
        },
        "half_year": {"text": "H{0}"},
        "quarter": {"text": "Q{0}"},
        "month": {
            "text": "{0}",
            "generic_text": "Month {0}",
        },
        "week": {
            "text": "{0} {1}",
            "generic_text": "W{0}",
        },
    },
}

### v1.1.1 Add generic timeline locale settings
generic_timeline_locale_settings = {
    "locale": "",
    "settings": {
        "year": {
            "text": "Year {0}",
            "generic_text": "Year {0}",
        },
        "half_year": {"text": "H{0}"},
        "quarter": {"text": "Q{0}"},
        "month": {
            "text": "{0}",
            "generic_text": "Month {0}",
        },
        "week": {
            "text": "{0} {1}",
            "generic_text": "W{0}",
        },
    },
}


TimelineLocaleSettings = [
    default_timeline_locale_settings,
    ### v1.1.1 Add generic timeline locale settings
    generic_timeline_locale_settings,
    ### Add more themes here
]


@dataclass
class TimelineLocale:
    """Timeline locale for the Roadmapper."""

    def __init__(self, locale_name: str) -> None:
        """Initialise the locale settings."""

        # check if colour_theme_name is a json file
        if locale_name.endswith(".json"):
            if os.path.isfile(locale_name):
                with open(locale_name, "r", encoding="utf8") as f:
                    timeline_locale_json = json.load(f)
                if "locale" in timeline_locale_json:
                    locale_name = timeline_locale_json["locale"]
                    TimelineLocaleSettings.append(timeline_locale_json)
                else:
                    raise ValueError(f"Locale {locale_name} not recognised.")
            else:
                raise ValueError(f"Locale {locale_name} not recognised.")

            self._timeline_locale_name = locale_name
            locale.setlocale(locale.LC_ALL, locale_name)
        else:
            ## v1.1.1 accept all non-json locale names
            self._timeline_locale_name = locale_name
            locale.setlocale(locale.LC_ALL, locale_name)

    def get_timeline_locale_settings(self, timeline_mode: str) -> tuple:
        """ "Get the timeline locale settings for the specified timeline mode.

        Args:
            timeline_mode (str): Timeline mode component to get the corresponding display settings.
                                        Components are: "year", "half-year", "quarter", "month", "week".

        Returns:
            tuple: Tuple of the display settings for the specified timeline mode component.
        """
        locale_settings = None

        for _, value in enumerate(TimelineLocaleSettings):
            if value["locale"] == self._timeline_locale_name:
                locale_settings = value["settings"]
                break

        ### get the colour scheme for the specified roadmap component
        ### values() returns a list of dictionaries, convert it to tuple. e.g. {1, 2} -> (1, 2)
        if len(locale_settings[timeline_mode].values()) > 1:
            return tuple(locale_settings[timeline_mode].values())
        else:
            return tuple(locale_settings[timeline_mode].values())[0]
