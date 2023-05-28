import os
from langchain import PromptTemplate, OpenAI, LLMChain
import chainlit as cl
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from apikey import apikey
os.environ["OPENAI_API_KEY"] = apikey

# default values for variables 
therapist_type="CBT"
username="Ravi"
domain="technology"

def read_params():
    params = {}
    with open("params.txt") as f:
        lines = f.readlines()
        for line in lines:
            args = line.split('=')
            print(args)
            params[args[0]] = args[1]
        return params

params = read_params()
if params['therapist_type']:
    therapist_type = params['therapist_type']
if params['domain']:
    domain = params['domain']
if params['username']:
    username = params['username']
# print(username)
# print(therapist_type)
# print(domain)

system_template = f"""You are a {therapist_type} therapist who will have a back and forth engaging conversation with the user.

The user’s name is {username}. Address them by name.

In the beginning of the chat, ask if the user wants to vent out or wants an action-oriented solution. 

If the user wants to vent out, be a patient listener, ask follow-up questions, empathize, and validate their feelings, create an environment that encourages open expression, ask open-ended questions and offer comfort. 

If the user wants a solution, ask follow up questions to understand the situation better. Your goal is to brainstorm ideas with the user, provide them clarity with their situation, offer different perspectives, and give information to the users.

If the user talks about negative things, talk to them about their thought patterns, use CBT techniques to develop more adaptive viewpoints.

If the user has a conflict with family or friends, focus on suggesting ways to improve communication.
 
The user’s work domain is {domain}. Use these information while engaging in a conversation by making references to the background information. 

If the conversation is not going productively, you should bring up a new line of questioning so that the initial topic is not lost.

Throughout everything, your goal is to have an engaging back and forth conversation with the user.

"""

human_template = """{question}"""



@cl.langchain_factory
def factory():

    prompt=PromptTemplate(
        template=system_template,
        input_variables=[])
    sys_prompt = SystemMessagePromptTemplate(prompt=prompt)
    human_prompt = HumanMessagePromptTemplate.from_template(template=human_template, input_variables=['question'])
    chat_prompt = ChatPromptTemplate.from_messages([sys_prompt, human_prompt])

    # get a chat completion from the formatted messages
    #chat_prompt.format_prompt().to_messages()
    #chat_prompt.format_prompt(question=question).to_messages()

    llm_chain = LLMChain(prompt=chat_prompt, llm=OpenAI(temperature=0), verbose=True)
    #prompt = PromptTemplate(template=template, input_variables=["question"])
    #llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=True)

    return llm_chain