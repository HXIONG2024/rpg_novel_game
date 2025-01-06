from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from .config.tools import CharacterInfo, InventoryInfo, save_theme
from .config.tools import save_character_info, save_inventory_info
from llm_config import novel_llm, mistral_llm, gemini_llm_15
load_dotenv()


@CrewBase
class ThemeCrew:
    """Theme Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def tool_executor(self) -> Agent:
        return Agent(
            config=self.agents_config["tool_executor"],
            llm=gemini_llm_15
        )
    
    @agent
    def rpg_game_theme_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["rpg_game_theme_writer"],
            llm=novel_llm
        )

    @agent
    def rpg_initial_configuration_provider(self) -> Agent:
        return Agent(
            config=self.agents_config["rpg_initial_configuration_provider"],
            llm=mistral_llm
        )

    @agent
    def rpg_initial_configuration_modifier(self) -> Agent:
        return Agent(
            config=self.agents_config["rpg_initial_configuration_modifier"],
            llm=novel_llm
        )

    @task
    def write_theme(self) -> Task:
        return Task(
            config=self.tasks_config["write_theme"]
        )
    
    @task
    def save_theme(self) -> Task:
        return Task(
            config=self.tasks_config["save_theme"],
            tools=[save_theme]
        )

    @task
    def generate_initial_character_configuration(self) -> Task:
        return Task(
            config=self.tasks_config["generate_initial_character_info"],
            output_pydantic=CharacterInfo
        )
    
    @task
    def modify_initial_character_configuration(self) -> Task:
        return Task(
            config=self.tasks_config["modify_initial_character_info"],
            tools=[save_character_info]
        )

    @task
    def generate_initial_inventory_configuration(self) -> Task:
        return Task(
            config=self.tasks_config["generate_initial_inventory_info"],
            output_pydantic=InventoryInfo
        )

    @task
    def modify_initial_inventory_configuration(self) -> Task:
        return Task(
            config=self.tasks_config["modify_initial_inventory_info"],
            tools=[save_inventory_info]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Theme Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

#test
"""
input = {
    'player_preferences': 'cats',
    'player_character_name': 'Harry'
}
test = ThemeCrew()
result = test.crew().kickoff(inputs=input)
"""