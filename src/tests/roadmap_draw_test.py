import os.path
import time
import calendar

import pytest

from src.roadmapper.roadmap import Roadmap


@pytest.mark.unit
class TestRoadmapDraw:
    def test_draw_roadmap_with_minimal_required_features(self):
        roadmap: Roadmap = Roadmap()
        roadmap.set_timeline(start="2023-01-01")
        roadmap.set_title("Test Title")

        roadmap.draw()

        filename_with_ts = str(calendar.timegm(time.gmtime())) + ".png"
        roadmap.save(filename_with_ts)

        assert os.path.exists(filename_with_ts)
        os.remove(filename_with_ts)

    def test_draw_roadmap_requires_timeline(self):
        roadmap: Roadmap = Roadmap()
        roadmap.set_title("Test Title")

        with pytest.raises(ValueError) as e:
            roadmap.draw()

        assert "timeline" in str(e.value).lower()

    def test_draw_roadmap_requires_title(self):
        roadmap: Roadmap = Roadmap()

        with pytest.raises(ValueError) as e:
            roadmap.draw()

        assert "title" in str(e.value).lower()
