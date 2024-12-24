import os
from key import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def example():
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run("colorful socks")
    print(output)


DEBUG = True

def chat_only(user_input):
    llm = OpenAI(temperature=0.9)
    output = llm(user_input)
    if DEBUG:
        print(f"LLM: {output}")
    return output

def get_prompt(user_input):
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    output = prompt.format(product=user_input)
    if DEBUG:
        print(f"PROMPT: {output}")
    return output
    
example()