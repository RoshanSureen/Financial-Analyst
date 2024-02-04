import os
import time
import json
import time


def pretty_print(messages):
    responses = []
    for m in messages:
        if m.role == "assistant":
            responses.append(m.content[0].text.value)
    return "\n".join(responses)

def extract_assitant_desc(obj):
    return json.loads(obj.model_dump_json())


