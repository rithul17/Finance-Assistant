from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import yaml
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

@CrewBase
class CrewAgent():
    """Multi-agent finance assistant crew"""
    
    def __init__(self):
        # Get the absolute path to the directory containing this file (crew.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Join it with "config/agents.yaml"
        agents_yaml_path = os.path.join(base_dir, "config", "agents.yaml")
        tasks_yaml_path = os.path.join(base_dir, "config", "tasks.yaml")
        
        with open(agents_yaml_path, "r") as f:
            self.agents_config = yaml.safe_load(f)
        with open(tasks_yaml_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)

    @agent
    def query_analysis_agent(self) -> Agent:
        cfg = self.agents_config['query_analysis_agent']
        return Agent(
            role=cfg['role'],
            goal=cfg['goal'],
            backstory=cfg['backstory'],
            verbose=True
        )

    @agent
    def api_agent(self) -> Agent:
        cfg = self.agents_config['api_agent']
        return Agent(
            role=cfg['role'],
            goal=cfg['goal'],
            backstory=cfg['backstory'],
            verbose=True
        )

    @agent
    def scraping_agent(self) -> Agent:
        cfg = self.agents_config['scraping_agent']
        return Agent(
            role=cfg['role'],
            goal=cfg['goal'],
            backstory=cfg['backstory'],
            verbose=True,
            tools=[]  
        )

    @agent
    def retriever_agent(self) -> Agent:
        cfg = self.agents_config['retriever_agent']
        return Agent(
            role=cfg['role'],
            goal=cfg['goal'],
            backstory=cfg['backstory'],
            verbose=True,
            tools=[]  
        )

    @agent
    def analysis_agent(self) -> Agent:
        cfg = self.agents_config['analysis_agent']
        return Agent(
            role=cfg['role'],
            goal=cfg['goal'],
            backstory=cfg['backstory'],
            verbose=True,
            tools=[]  
        )

    @agent
    def language_agent(self) -> Agent:
        cfg = self.agents_config['language_agent']
        return Agent(
            role=cfg['role'],
            goal=cfg['goal'],
            backstory=cfg['backstory'],
            verbose=True,
            tools=[]  
        )

    @task
    def query_analysis_task(self) -> Task:
        cfg = self.tasks_config['query_analysis_task']
        return Task(
            description=cfg['description'],
            expected_output=cfg['expected_output'],
            agent=self.query_analysis_agent()
        )

    @task
    def data_collection_task(self) -> Task:
        cfg = self.tasks_config['data_collection_task']
        return Task(
            description=cfg['description'],
            expected_output=cfg['expected_output'],
            agent=self.api_agent(),
            context=[self.query_analysis_task()]  
        )

    @task
    def document_scraping_task(self) -> Task:
        cfg = self.tasks_config['document_scraping_task']
        return Task(
            description=cfg['description'],
            expected_output=cfg['expected_output'],
            agent=self.scraping_agent()
        )

    @task
    def context_retrieval_task(self) -> Task:
        cfg = self.tasks_config['context_retrieval_task']
        return Task(
            description=cfg['description'],
            expected_output=cfg['expected_output'],
            agent=self.retriever_agent()
        )

    @task
    def quantitative_analysis_task(self) -> Task:
        cfg = self.tasks_config['quantitative_analysis_task']
        return Task(
            description=cfg['description'],
            expected_output=cfg['expected_output'],
            agent=self.analysis_agent(),
            context=[self.context_retrieval_task()] 
        )

    @task
    def narrative_synthesis_task(self) -> Task:
        cfg = self.tasks_config['narrative_synthesis_task']
        return Task(
            description=cfg['description'],
            expected_output=cfg['expected_output'],
            agent=self.language_agent(),
            context=[self.quantitative_analysis_task()]  
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.query_analysis_agent(),
                self.api_agent(),
                self.scraping_agent(), 
                self.retriever_agent(),
                self.analysis_agent(),
                self.language_agent()
            ],
            tasks=[
                self.query_analysis_task(),
                self.data_collection_task(),
                self.document_scraping_task(),
                self.context_retrieval_task(),
                self.quantitative_analysis_task(),
                self.narrative_synthesis_task()
            ],
            process=Process.sequential,
            verbose=True
        )


