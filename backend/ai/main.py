from speech import Speech
from engine import generate_response


chat_history = []


while True:
    user_message= Speech.stt()
    if user_message.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break


    result = generate_response(user_message, chat_history=chat_history)
    Speech.speak_text(result['response'])
    # print(f"User: {result['input']}")
    # print(f"Intent: {result['intent']}")
    print(f"Assistant: {result['response']}\n")