#GPT-3 TEST (Lenny)

import os, time, math
from dotenv import load_dotenv
import openai
from pathlib import Path

env_path = Path.cwd() / '.env.env'
load_dotenv(dotenv_path=env_path)

openai.api_key = os.getenv('OPENAI_KEY')
completion = openai.Completion()

# ='''You are an adventurer who has been exploring a gargantuan maze-like dungeon for a long, long time. You have recently stopped at a large room in the dungeon, with merchants and other adventurers bustling about. You notice a man in his thirties, sitting on the cobblestone ground with his back to the black brick walls. He looks scraggly, and softly sips from a glass of whiskey and twirls a dagger in his hand as you approach. He looks up at you, and squints at you.

#You: *Walks up to him*

#Man: *Stares quietly while taking another sip of whiskey* Hey there.'''

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}'
    #print("\nhi\n" + chat_log + "\nhi\n")
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\n\n\n', "\n\n", 'You:', 'Man:'], temperature=0.8,
        top_p=1, frequency_penalty=0.4, presence_penalty=0.6, best_of=1,
        max_tokens=64)
    answer = response.choices[0].text.strip()
    return answer

#print(start_chat_log)
#while True:
#    question = input("Human: ")
#    start_chat_log += "\nHuman: " + question + "\n\nAI:\n"
#    answer = ""
#    while answer == "":
#        answer = ask(start_chat_log, start_chat_log)
#    start_chat_log += answer + "\n"
#    print("\nAI:\n" + answer + "\n")
    
