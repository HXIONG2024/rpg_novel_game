#!/usr/bin/env python
from crewai.flow.flow import Flow, listen, start
from crews.theme_crew.theme_crew import ThemeCrew
from crews.game_crew.game_crew import GameCrew
from crews.item_crew.item_crew import ItemCrew
import os
import shutil
import json
import random

class GameFlow(Flow):
    @start()
    def clear_game_config(self):
        print("Clearing game_config folder...")
        shutil.rmtree("game_config")
        os.makedirs("game_config")
        print("Game_config folder cleared.")

    @listen(clear_game_config)
    def generate_game_theme(self):
        print("Welcome to the RPG Novel Game!")
        print(
            """
            This game will be generated by AI, and please use
            your imagination to play the game!\n
            """
        )
        print("Here are some questions to help you generate the game theme:")
        name = input("\nWhat is your name?: ")
        theme = input("\nWhat kind of game do you like?: ")
        game_input = {
            "player_preferences": theme,
            "player_character_name": name
        }
        return ThemeCrew().crew().kickoff(inputs=game_input)
    
    @listen(generate_game_theme)
    def game_start(self):
        print("Game is starting...")
        self.progress_number = 0
        self.max_progress_number = 10
        self.game_status = True

        while self.game_status:
            self.progress_number += 1
            self.chapter = self.progress_number
            game_input = {
                "progress_number": self.progress_number,
                "max_progress_number": self.max_progress_number
            }
            self.game_crew = GameCrew().crew().kickoff(inputs=game_input)
            
            # here is the next step
            is_player_alive = True
            # player choose the option
            with open("game_config/current_options.json", "r") as file:
                current_options = json.load(file)
            for option in current_options["options"]:
                print(option["option_number"])
                print(option["description"])
                print("\n")
            player_input = int(input("Please choose the option: "))
            
            # check whether the player success or not
            if random.randint(0, 100) <= current_options["options"][player_input-1]["probability_of_success"]:
                is_player_success = True
            else:
                is_player_success = False
                # player - 1 health point
                with open("game_config/character_info.json", "r") as file:
                    character_info = json.load(file)
                character_info["health_point"] -= 1
                with open("game_config/character_info.json", "w") as file:
                    json.dump(character_info, file, indent=2)
                # check whether the player is alive or not
                if character_info["health_point"] <= 0:
                    is_player_alive = False
            
            # check whether the player used the item or not
            if current_options["options"][player_input-1]["item_used"] is None:
                is_item_used = False
            else:
                is_item_used = True
                # delete the item from the player's inventory
                item_number = current_options["options"][player_input-1]["item_used"]
                with open("game_config/inventory_info.json", "r") as file:
                    inventory_info = json.load(file)
                for item in inventory_info["items"]:
                    if item["item_number"] == item_number:
                        inventory_info["items"].remove(item)
                        break
                with open("game_config/inventory_info.json", "w") as file:
                    json.dump(inventory_info, file, indent=2)
            
            # check whether the player get the item or not
            if random.randint(0, 100) > current_options["options"][player_input-1]["probability_of_getting_item"]:
                is_player_get_item = False
            else:
                is_player_get_item = True
            
            # create the new item
            if is_player_get_item:
                ItemCrew().crew().kickoff()
            
                # write the new item back to the round result
                with open("game_config/inventory_info.json", "r") as file:
                    inventory_info = json.load(file)
                self.new_item_name = inventory_info["items"][-1]["item_name"]
                self.new_item_ability = inventory_info["items"][-1]["ability"]
            else:
                self.new_item_name = None
                self.new_item_ability = None
            
            round_result = {
                "option_description": current_options["options"][player_input-1]["description"],
                "is_player_alive": is_player_alive,
                "is_player_success": is_player_success,
                "is_item_used": is_item_used,
                "is_player_get_item": is_player_get_item,
                "new_item_name": self.new_item_name,
                "new_item_ability": self.new_item_ability
            }
            with open("game_config/round_result.json", "w") as file:
                json.dump(round_result, file, indent=4)
            
            if self.progress_number == self.max_progress_number:
                self.game_status = False
            print("current round result has been saved in game_config/round_result.json")
            player_response = input("Do you want to continue the game? (yes/no): ")
            if player_response == "no":
                self.game_status = False
            else:
                self.game_status = True
        return print("Game is over!")



def kickoff():
    game_flow = GameFlow()
    game_flow.kickoff()

if __name__ == "__main__":
    kickoff()
