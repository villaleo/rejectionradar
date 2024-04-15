from openai import OpenAI

MODEL = "gpt-3.5-turbo"
client = OpenAI()


def is_rejection(msg):
    content = ""
    if not msg.get("text"):
        content = msg["snippet"]
    else:
        content = msg["text"]

    messages = [
        {
            "role": "system",
            "content": "You are an expert on determining if an email received was a job "
            + "rejection. A user will send you parts of an email they received "
            + "and you will respond with 'true' if it's a rejection, or "
            + "'false' otherwise.",
        },
        {"role": "user", "content": content},
    ]
    completion = client.chat.completions.create(model=MODEL, messages=messages)
    content = completion.choices[0].message.content
    return "true" in str(content).lower()
