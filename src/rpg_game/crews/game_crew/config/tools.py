from crewai.tools import tool
import numpy as np
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import json

@tool("write_novel")
def write_novel(content: str):
    """
    Write the novel to the file.
    """
    with open("game_config/novel.md", "a", encoding="utf-8") as file:
        file.write(content + "\n")
    return print("Novel has been written to the file: game_config/novel.md")

@tool("current_chapter")
def current_chapter(content: str):
    """
    Write the current chapter of the novel.
    """
    with open("game_config/current_chapter.md", "w", encoding="utf-8") as file:
        file.write(content)
    return print("Current chapter has been written to the file: game_config/current_chapter.md")

@tool("options_and_probabilities")
def options_and_probabilities():
    """
    Get the number of options and the probability of success for each option.
    """
    number_of_options = np.random.randint(2, 5)
    # create a dictionary to store the probability of success for each option
    options = {}
    for option in range(number_of_options):
        probability_of_success = np.random.randint(0, 100)
        options[f"option {option+1}"] = {
            "probability_of_success": probability_of_success,
            "probability_of_getting_item": 100 - probability_of_success
        }
    return options

class OptionsAndProbabilities(BaseModel):
    description: str = Field(
        ...,
        description="The question and movement for the player for this option"
    )
    option_number: int = Field(
        ...,
        description="The option number"
    )
    probability_of_success: int = Field(
        ...,
        description="The probability of success for the this option",
        ge=0,
        le=100
    )
    probability_of_getting_item: int = Field(
        ...,
        description="The probability of getting an item for the player for this option",
        ge=0,
        le=100
    )
    item_used: Optional[int] = Field(
        default=None,
        description="The item number used for this option"
    )
    @field_validator("probability_of_getting_item")
    def validate_probability_of_getting_item(cls, v):
        v = 100 - cls.probability_of_success
        if v < 0:
            v = 0
        return v

class Options(BaseModel):
    options: list[OptionsAndProbabilities] = Field(
        ...,
        description="The options for the player to choose"
    )
    @field_validator("options")
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("The number of options must be greater than or equal to 2")
        return v

@tool("read_inventory")
def read_inventory():
    """
    Read the inventory of the player.
    """
    with open("game_config/inventory_info.json", "r") as file:
        return f"The inventory of the player is: \n{json.load(file)}"

@tool("read_character_info")
def read_character_info():
    """
    Read the character information of the player.
    """
    with open("game_config/character_info.json", "r") as file:
        return f"The character information of the player is: \n{json.load(file)}"

@tool("read_theme")
def read_theme():
    """
    Read the theme of the game.
    """
    with open("game_config/theme.md", "r", encoding="utf-8") as file:
        return f"The theme of the game is: \n{file.read()}"

@tool("read_current_chapter")
def read_current_chapter():
    """
    Read the current chapter of the novel.
    if you don't see the file, just ignore it.
    """
    try:
        with open("game_config/current_chapter.md", "r", encoding="utf-8") as file:
            return f"The current chapter of the novel is: \n{file.read()}"
    except FileNotFoundError:
        return None

@tool("read_round_result")
def read_round_result():
    """
    Read the round result of the game.
    if you don't see the file, just ignore it.
    """
    try:
        with open("game_config/round_result.json", "r") as file:
            return f"The round result of the game is: \n{json.load(file)}"
    except FileNotFoundError:
        return None
