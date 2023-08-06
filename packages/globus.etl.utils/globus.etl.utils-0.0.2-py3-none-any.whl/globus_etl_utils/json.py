import json

def list_to_json_line(l: list) -> str:
    return '\n'.join([json.dumps(item) for item in l])


def json_line_to_list(jsl: str) -> str:
    return [json.loads(line) for line in jsl.split('\n') if line]