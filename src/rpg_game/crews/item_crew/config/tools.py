from pydantic import BaseModel, Field
from crewai.tools import tool
import json

class ItemInfo(BaseModel):

    item_number: int = Field(
        ...,
        description="The number of the item",
        ge=1,
    )
    item_name: str = Field(
        ...,
        description="The name of the item",
        min_length=1,
    )
    ability: str = Field(
        ...,
        description="The ability of the item, cannot have more than 1 ability",
        min_length=1,
    )

@tool("read_theme")
def read_theme(file_path = "game_config/theme.md") -> str:
    """
    Read the theme from a markdown file.
    The default file path is "game_config/theme.md"
    """
    with open(file_path, "r", encoding="utf-8") as file:
        theme = file.read()
    return theme

@tool("read_option_description")
def read_option_description(file_path = "game_config/round_result.json") -> str:
    """
    Read the option description from a json file.
    The default file path is "game_config/round_result.json"
    """
    with open(file_path, "r") as file:
        option_description = json.load(file)["option_description"]
    return option_description

@tool("check_item")
def check_item(file_path = "game_config/inventory_info.json") -> str:
    """
    Check if the item is already in the inventory.
    The default file path is "game_config/inventory_info.json"
    """
    with open(file_path, "r") as file:
        inventory_info = json.load(file)["items"]
    return inventory_info

@tool("save_item")
def save_item(item: ItemInfo, file_path = "game_config/inventory_info.json") -> str:
    """
    Save the item to the inventory_info.json file.
    The default file path is "game_config/inventory_info.json"
    """
    # if item is dictionary, convert it to ItemInfo
    if isinstance(item, dict):
        item = ItemInfo(**item)
    # append the item to the items list
    with open(file_path, "r") as file:
        inventory_info = json.load(file)
    inventory_info["items"].append(item.model_dump())
    with open(file_path, "w") as file:
        json.dump(inventory_info, file, indent=4)
    return "Item saved successfully"