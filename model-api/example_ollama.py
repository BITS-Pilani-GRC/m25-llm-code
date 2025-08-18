from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'Who won the world cup in 2011?',
  },
]

response = chat('llama3.2', messages=messages)
print(response['message']['content'])