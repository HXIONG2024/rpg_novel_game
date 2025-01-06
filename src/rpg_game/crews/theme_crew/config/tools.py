from crewai.tools import tool
import json
from pydantic import BaseModel, Field, field_validator, ValidationError
from pathlib import Path
from typing import Optional, List


class CharacterInfo(BaseModel):
    description: str = Field(
        default="",
        description="The description of the character"
    )
    name: str = Field(
        ...,
        description="The name of the character",
        min_length=1,
    )
    health_point: int = Field(
        default=5,
        description="The health point of the character(0-5)",
        ge=0,
        le=5,
    )

@tool("read_character_info")
def read_character_info(file_path = "game_config/character_info.json") -> CharacterInfo:
    """
    Read character information from a JSON file.
    The default file path is "game_config/character_info.json"
    
    Args:
        file_path (str): Path to the character info JSON file
        
    Returns:
        CharacterInfo: The character information loaded from the file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Character info file not found: {file_path}")
        
    with path.open('r') as f:
        data = json.load(f)
    return CharacterInfo(**data)

@tool("save_character_info")
def save_character_info(character_info: CharacterInfo, file_path = "game_config/character_info.json") -> str:
    """
    Save character information to a JSON file.
    The default file path is "game_config/character_info.json"
    
    Args:
        character_info (CharacterInfo): The character information to save
        file_path (str): Path where to save the JSON file
        
    Returns:
        str: Success message with file path
    """
    # Convert the dictionary to a pydantic model if necessary
    if isinstance(character_info, dict):
        character_info = CharacterInfo(**character_info)
    
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open('w') as f:
        json.dump(character_info.model_dump(), f, indent=4)
    
    return f"Character info saved to {file_path}"

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

class InventoryInfo(BaseModel):
    description: str = Field(
        default="",
        description="The description of the inventory",
    )
    items: List[ItemInfo] = Field(
        default=[],
        description="The items in the inventory",
    )

@tool("read_inventory_info")
def read_inventory_info(file_path = "game_config/inventory_info.json") -> InventoryInfo:
    """
    Read inventory information from a JSON file.
    The default file path is "game_config/inventory_info.json"

    Args:
        file_path (str): Path to the inventory info JSON file
        
    Returns:
        InventoryInfo: The inventory information loaded from the file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Inventory info file not found: {file_path}")
       
    with path.open('r') as f:
        data = json.load(f)
    return InventoryInfo(**data)

@tool("save_inventory_info")
def save_inventory_info(inventory_info: InventoryInfo, file_path = "game_config/inventory_info.json") -> str:
    """
    Save inventory information to a JSON file.
    The default file path is "game_config/inventory_info.json"
    
    Args:
        inventory_info (InventoryInfo): The inventory information to save
        file_path (str): Path where to save the JSON file
        
    Returns:
        str: Success message with file path
    """
    try:
        # Handle case where input is a JSON string
        if isinstance(inventory_info, str):
            data = json.loads(inventory_info)
            if "inventory_info" in data:  # Handle nested structure
                data = data["inventory_info"]
            inventory_info = InventoryInfo(**data)
        # Handle dictionary case
        elif isinstance(inventory_info, dict):
            inventory_info = InventoryInfo(**inventory_info)
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with path.open('w') as f:
            json.dump(inventory_info.model_dump(), f, indent=4)
        
        return f"Character info saved to {file_path}"
        
    except ValidationError as e:
        return f"Validation error: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Invalid JSON format: {str(e)}"
    except Exception as e:
        return f"Error saving inventory info: {str(e)}"
    
@tool("save_theme")
def save_theme(theme: str, file_path = "game_config/theme.md") -> str:
    """
    Save the theme to a file.
    The default file path is "game_config/theme.md"
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(theme)
    return f"Theme saved to {file_path}"

