import os
import time
from openai import OpenAI

def initialize_openai_client(API_KEY):
    return OpenAI(api_key=API_KEY)

def create_assitant(client: OpenAI):
    assitant = client.beta.assistants.create(
        name = "Finance Insight Analyst",
        instructions = "You are a helpful financial analyst expert and, focusing on management discussions and financial results. Help people learn about financial needs and guide them towards fincial literacy.",
        tools = [{"type":"code_interpreter"}, {"type": "retrieval"}],
        model = "gpt-4-1106-preview"
    )
    return assitant

def create_thread(client:OpenAI):
    return client.beta.threads.create()

def submit_message(client:OpenAI, assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    
def wait_on_run(client:OpenAI, run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_response(client:OpenAI, thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")




