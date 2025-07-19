import json
from antchat.antchat import AntChat
from antchat.types

def generate_dataset():
    prompt = (
    "Generate an evaluation dataset for a prompt evaluation. " 
    "The dataset will be used to evaluate prompts that generate Python, JSON, "
    "or Regex specifically for AWS-related tasks. Generate an array of JSON "
    "objects, each representing task that requires Python, JSON, or a Regex "
    "to complete.\n"
    """Example output:
    ```json
    [
    {
        "task": "Description of task",
    },
    ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """
    )
    chat = AntChat()
    chat.add_user_message(prompt)
    chat.add_assistant_message("```json")
    chat.send_messages(stop_sequences=["```"])
    resp_obj = chat.get_last_response() 
    resp = resp_obj if isinstance(resp_obj, str) else str(resp_obj)
    return json.loads(resp )

if __name__ == "__main__":
    dataset = generate_dataset()
    with open('dataset.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    with open("dataset.json", "r") as f:
        dataset = json.load(f)
    if isinstance(dataset, list):
        if all([isinstance(item, dict) for item in dataset]):
