import argparse
import os.path
from typing import Type

from src.tests.roadmap_generators.colour_theme import ColourTheme
from src.tests.roadmap_generators.colour_theme_extensive import ColourThemeExtensive
from src.tests.roadmap_generators.milestone_text_alignment import MilestoneTextAlignment
from src.tests.roadmap_generators.roadmap_abc import RoadmapABC

file_ending = ".png"
file_directory = ""
all_roadmaps_to_generate: [RoadmapABC] = [ColourThemeExtensive, ColourTheme, MilestoneTextAlignment]


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


def get_roadmap_name_for(roadmap_class: Type[RoadmapABC], operating_system: str) -> str:
    return roadmap_class.__name__ + operating_system


def get_generated_file_path_for(roadmap_class: Type[RoadmapABC], operating_system: str) -> str:
    ensure_presence_of_file_directory(file_directory)
    return file_directory + get_roadmap_name_for(roadmap_class, operating_system) + file_ending


def generate_and_save_roadmap(roadmap_class: Type[RoadmapABC], operating_system: str, target_directory: str = ""):
    set_file_directory(target_directory)
    file_path = get_generated_file_path_for(roadmap_class, operating_system)
    generating_object = roadmap_class()
    generating_object.generate_and_save_as(file_path)


def generate_and_save_all_roadmaps(target_directory: str = "", operating_system: str = "Ubuntu"):
    set_file_directory(target_directory)
    for generating_class in all_roadmaps_to_generate:
        generate_and_save_roadmap(generating_class, operating_system, target_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate roadmaps")
    parser.add_argument("--target-directory", "-td", help="Directory in which the generated roadmaps should be saved",
                        type=str, default="")
    parser.add_argument("--operating-system", "-os", help="Operating system for which the roadmaps are generated",
                        type=str, default="")

    args = parser.parse_args()

    generate_and_save_all_roadmaps(target_directory=args.target_directory, operating_system=args.operating_system)
