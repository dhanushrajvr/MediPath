from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from langchain.agents import create_agent
from tools.symptom_checker import symptom_checker
from tools.department_lookup import department_lookup
from tools.emergency_checker import check_emergency
from tools.slot_checker import check_slot_availability

load_dotenv()
llm_provider = os.getenv("LLM_PROVIDER")

class Agent:
    def __init__(self):
        self.llm_provider = llm_provider  # Global variable
        self.llm = None
        self.agent = None

    def setup_llm(self):
        if self.llm_provider == "ollama":
            self.llm = ChatOllama(
                model="llama2",
                temperature=0
            )
        elif self.llm_provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-3.5-flash-lite",
                temperature=0
            )

    def create_agent(self):
        if self.llm is not None:
            self.agent = create_agent(
                model=self.llm,
                tools=[symptom_checker, department_lookup, check_emergency, check_slot_availability],
                system_prompt="""
                    You are a medical assistant. Doctor lose time in manual intake forms and mis-routed patients. 
                    Your task is to help patients by asking them questions about their symptoms, check possible diseases, determine the appropriate department, check for emergency symptoms, and check slot availability for appointments.

                    Input Structure:
                    - Name of the patient
                    - Age of the patient
                    - Gender of the patient
                    - List of symptoms
                    - Start date of symptoms
                    - Other relevant information

                    Output Structure:
                    - Client Data (like name, age, gender,...)
                    - List of possible diseases
                    - Appropriate department for the patient
                    - Whether the symptoms indicate an emergency
                    - Slot for application availability for the department based on the symptoms, possible diseases, emergency check, and available slots for the department.

                    You have access to the following tools:
                    1. symptom_checker: This tool takes a list of symptoms and returns a list of possible diseases.
                    2. department_lookup: This tool takes a list of symptoms and a list of possible diseases and returns the appropriate department.
                    3. check_emergency: This tool takes a list of symptoms and returns True if the symptoms indicate an emergency, False otherwise.
                    4. check_slot_availability: This tool takes a department and a date and returns True if there are available slots, False otherwise.

                    You should use these tools to help patients with their medical concerns.
                """
            )

    def send_query(self, query: str) -> str:
        
        result = self.agent.invoke({
            "messages": [
                {"role": "user", "content": query},
            ]
        })
    
        # Get final answer
        answer = result["messages"][-1].content
    
        # If Gemini returns a list, extract the text
        if isinstance(answer, list):
            answer = "\n".join(
                item["text"]
                for item in answer
                if isinstance(item, dict) and item.get("type") == "text"
            )
    
        return answer

def has_llmProvider() -> bool:
    return llm_provider is not None

if __name__ == "__main__":
    if not has_llmProvider():
        raise ValueError("LLM_PROVIDER environment variable is not set.")
    agent_instance = Agent()
    agent_instance.setup_llm()
    agent_instance.create_agent()
    result = agent_instance.send_query("Patient Name: John Doe\nAge: 30\nGender: Male\nSymptoms: fever, cough, fatigue\nStart Date of Symptoms: 2024-06-01\nOther Relevant Information: None")
    
    print('-' * 15)
    print(result)
    print('-' * 15)