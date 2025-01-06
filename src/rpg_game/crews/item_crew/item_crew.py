from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from .config.tools import read_theme, read_option_description, check_item, save_item
from llm_config import novel_llm, mistral_llm, gemini_llm_15
load_dotenv()


@CrewBase
class ItemCrew:
    """Item Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def tool_executor(self) -> Agent:
        return Agent(
            config=self.agents_config["tool_executor"],
            llm=novel_llm
        )
    
    @agent
    def item_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["item_creator"],
            llm=mistral_llm
        )
    
    @task
    def provide_info(self) -> Task:
        return Task(
            config=self.tasks_config["provide_info"],
            tools=[read_theme, read_option_description, check_item]
        )
    
    @task
    def create_item(self) -> Task:
        return Task(
            config=self.tasks_config["create_item"]
        )
    
    @task
    def save_item(self) -> Task:
        return Task(
            config=self.tasks_config["save_item"],
            tools=[save_item]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Item Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

#test
"""
test = ItemCrew()
result = test.crew().kickoff()
"""