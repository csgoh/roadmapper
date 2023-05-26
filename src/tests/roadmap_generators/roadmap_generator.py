import os.path
from typing import Type

from src.tests.roadmap_generators.colour_theme_extensive import ColourThemeExtensive
from src.tests.roadmap_generators.roadmap_abc import RoadmapABC
import pytest

file_ending = ".png"
file_directory = ""
all_roadmaps_to_generate: [RoadmapABC] = [ColourThemeExtensive]


def get_all_roadmap_names_to_generate() -> [str]:
    return [get_roadmap_name_for(cls) for cls in all_roadmaps_to_generate]


def append_trailing_slash_if_necessary(directory) -> str:
    if directory and not directory.endswith(os.path.sep):
        return directory + os.path.sep
    return directory


def set_file_directory(directory):
    global file_directory
    file_directory = append_trailing_slash_if_necessary(directory)


def ensure_presence_of_file_directory(directory):
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def get_roadmap_name_for(roadmap_class: Type[RoadmapABC]) -> str:
    print(roadmap_class.__name__ + "Ubuntu")
    return roadmap_class.__name__ + "Ubuntu"  # TODO: Make OS agnostic


def get_generated_file_path_for(roadmap_class: Type[RoadmapABC]) -> str:
    ensure_presence_of_file_directory(file_directory)
    return file_directory + get_roadmap_name_for(roadmap_class) + file_ending


def generate_and_save_roadmap_in(
    roadmap_class: Type[RoadmapABC], target_directory: str = ""
):
    set_file_directory(target_directory)
    file_path = get_generated_file_path_for(roadmap_class)
    generating_object = roadmap_class()
    generating_object.generate_and_save_as(file_path)


def generate_and_save_all_roadmaps_in(target_directory: str = ""):
    set_file_directory(target_directory)
    for generating_class in all_roadmaps_to_generate:
        file_path = get_generated_file_path_for(generating_class)
        generating_object = generating_class()
        generating_object.generate_and_save_as(file_path)


if __name__ == "__main__":
    generate_and_save_all_roadmaps_in()


