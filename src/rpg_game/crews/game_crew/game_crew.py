from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from .config.tools import read_character_info, read_theme, read_current_chapter, read_round_result
from .config.tools import write_novel, current_chapter
from .config.tools import options_and_probabilities, Options, read_inventory
from llm_config import novel_llm, mistral_llm, gemini_llm_15
load_dotenv()

tool_executor_llm = gemini_llm_15


@CrewBase
class GameCrew:
    """Game Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def tool_executor(self) -> Agent:
        return Agent(
            config=self.agents_config["tool_executor"],
            llm=tool_executor_llm
        )

    @agent
    def condition_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["condition_checker"],
            llm=novel_llm,
        )
    
    @agent
    def rpg_novel_game_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["rpg_novel_game_writer"],
            llm=novel_llm
        )
    
    @agent
    def rpg_option_maker(self) -> Agent:
        return Agent(
            config=self.agents_config["rpg_option_maker"],
            llm=mistral_llm
        )

    @task
    def information_providing(self) -> Task:
        return Task(
            config=self.tasks_config["information_providing"],
            tools=[read_character_info, read_theme, read_current_chapter, read_round_result, read_inventory]
        )

    @task
    def check_game_condition(self) -> Task:
        return Task(
            config=self.tasks_config["check_game_condition"],
            output_file="game_config/summary.md",
        )
    
    @task
    def write_novel(self) -> Task:
        return Task(
            config=self.tasks_config["write_novel"]
        )
    
    @task
    def store_novel(self) -> Task:
        return Task(
            config=self.tasks_config["store_novel"],
            tools=[write_novel, current_chapter]
        )
    
    @task
    def excute_probability(self) -> Task:
        return Task(
            config=self.tasks_config["excute_probability"],
            tools=[options_and_probabilities, read_inventory]
        )

    @task
    def make_options(self) -> Task:
        return Task(
            config=self.tasks_config["make_options"]
        )
    
    @task
    def store_options(self) -> Task:
        return Task(
            config=self.tasks_config["store_options"],
            output_pydantic=Options,
            output_file="game_config/current_options.json"
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Game Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

#test
"""
input = {
    'progress_number': 2,
    'max_progress_number': 10
}
test = GameCrew()
result = test.crew().kickoff(inputs=input)
"""