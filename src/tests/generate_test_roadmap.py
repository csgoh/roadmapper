import os
from typing import Type

import pytest
import src.tests.roadmap_generators.roadmap_generator as roadmap_generator

@pytest.mark.genimage
class TestGenerateRoadmaps:
    roadmap_generator.generate_and_save_all_roadmaps_in()
    assert True