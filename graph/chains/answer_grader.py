from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field

class GradeAnswer(BaseModel):
    binary_score: bool = Field(description="Answer addresses the question, 'yes' or 'no'")

parser = JsonOutputParser(pydantic_object=GradeAnswer)

llm = Ollama(model="llama3.2")

system = """You are a grader assessing whether an answer addresses / resolves a question.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question.
You must respond in the following JSON format:
{{"binary_score": true}} for yes
{{"binary_score": false}} for no"""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader = answer_prompt | llm | parser
