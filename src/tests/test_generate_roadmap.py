import os
from typing import Type

import pytest
import src.tests.roadmap_generators.roadmap_generator as roadmap_generator

@pytest.mark.genimage
class TestGenerateRoadmaps:
    def test_generate_and_save_all_roadmaps_in(self):
        roadmap_generator.generate_and_save_all_roadmaps_in()
        assert True