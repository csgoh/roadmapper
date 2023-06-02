import os
from typing import Type

import pytest
from PIL import Image, ImageChops

from src.tests.roadmap_generators import roadmap_generator
from src.tests.roadmap_generators.colour_theme import ColourTheme
from src.tests.roadmap_generators.colour_theme_extensive import ColourThemeExtensive
from src.tests.roadmap_generators.roadmap_abc import RoadmapABC

dir_for_examples = "example_roadmaps"
dir_for_generated = "generated_roadmaps"
dir_for_diffs = "diffs_of_generated_roadmaps"

suffix_for_examples = "Example"
file_ending_for_examples = ".png"

suffix_for_diffs = "Diff"
file_ending_for_diffs = file_ending_for_examples


def ensure_presence_of_file_directory(directory):
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def get_diff_file_path_for(roadmap_class: Type[RoadmapABC], operating_system: str) -> str:
    ensure_presence_of_file_directory(dir_for_diffs)
    return dir_for_diffs \
        + "/" \
        + roadmap_generator.get_roadmap_name_for(roadmap_class, operating_system) \
        + suffix_for_diffs \
        + file_ending_for_diffs


def handle_difference(diff, roadmap_class: Type[RoadmapABC], operating_system: str):
    print("The generated roadmap looks different from the example.")
    print("Run the test locally to see the generated difference.")
    diff_file_path = get_diff_file_path_for(roadmap_class, operating_system)
    diff.save(diff_file_path)


def get_generated_roadmap_image_for(roadmap_class: Type[RoadmapABC], operating_system: str) -> Image:
    path_of_generated = roadmap_generator.get_generated_file_path_for(roadmap_class, operating_system)
    return Image.open(path_of_generated).convert("RGB")


def get_example_file_path_for(roadmap_class: Type[RoadmapABC], operating_system: str) -> str:
    return dir_for_examples \
        + "/" \
        + roadmap_generator.get_roadmap_name_for(roadmap_class, operating_system) \
        + suffix_for_examples \
        + file_ending_for_examples


def get_example_roadmap_image_for(roadmap_class: Type[RoadmapABC], operating_system: str) -> Image:
    path_of_example = get_example_file_path_for(roadmap_class, operating_system)
    return Image.open(path_of_example).convert("RGB")


@pytest.mark.ubuntu
class TestCompareGeneratedRoadmaps:

    @pytest.mark.parametrize("roadmap_class_to_test", [ColourThemeExtensive, ColourTheme])
    def test_generate_correct_roadmaps_on_ubuntu(self, roadmap_class_to_test, operating_system_ubuntu):

        roadmap_generator.generate_and_save_roadmap(roadmap_class_to_test, operating_system_ubuntu, dir_for_generated)
        example_roadmap = get_example_roadmap_image_for(roadmap_class_to_test, operating_system_ubuntu)
        generated_roadmap = get_generated_roadmap_image_for(roadmap_class_to_test, operating_system_ubuntu)

        test_diff = ImageChops.difference(example_roadmap, generated_roadmap)

        if test_diff.getbbox():
            handle_difference(test_diff, roadmap_class_to_test, operating_system_ubuntu)
            assert False
        else:
            assert True
