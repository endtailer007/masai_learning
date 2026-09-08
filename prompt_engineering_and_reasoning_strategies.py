system_persona = "You are an expert career coach."

turns = [
    "What is the roadmap to become an FDE in 6 months?",
    "Summarize your previous answer in one sentence."
]

def mock_call_model(messages):
    reply_number = sum(1 for m in messages if m["role"] == "assistant") + 1
    return f"Mock reply #{reply_number} based on {len(messages)} messages so far."


def run_conversation(system_persona, turns, call_model):
    # TODO: start the messages list with a single system-role entry using system_persona
    messages = [{"role": "system", "content": system_persona}]

    # TODO: for each turn in `turns':
    for turn in turns:
    #   - append a user-role entry with that turn's text
        messages.append({"role": "user", "content": turn})
    #   - call `call_model(messages)` to get the assistant's reply
        reply = call_model(messages)
    #   - append an assistant-role entry with that reply
        messages.append({'role': "assistant", 'content': reply})
        

    return messages

if __name__ == "__main__":
    result = run_conversation(system_persona, turns, mock_call_model)
    print(result)
