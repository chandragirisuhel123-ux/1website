import ast
from functools import lru_cache
from pathlib import Path

from flask import current_app


@lru_cache(maxsize=1)
def _load_legacy_chatbot():
    source_path = Path(current_app.config["LEGACY_LOGIC_PATH"])
    source_code = source_path.read_text(encoding="utf-8")
    parsed = ast.parse(source_code, filename=str(source_path))

    selected_nodes = []
    for node in parsed.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "study_notes":
                    selected_nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == "get_answer":
            selected_nodes.append(node)

    module = ast.Module(body=selected_nodes, type_ignores=[])
    namespace = {}
    exec("import math", namespace)
    exec(compile(module, filename=str(source_path), mode="exec"), namespace)
    return namespace["study_notes"], namespace["get_answer"]


def get_chatbot_answer(user_input):
    _, answer_fn = _load_legacy_chatbot()
    return answer_fn(user_input)


def get_study_notes():
    study_notes, _ = _load_legacy_chatbot()
    return study_notes


def get_response_images(user_input):
    lowered = user_input.lower()

    if "hod" in lowered:
        return ["ramana.jpg"]
    if "faculty" in lowered:
        return ["samuel.jpg", "sujith.jpg", "karthik.jpg", "himaja.jpg"]
    if "principal" in lowered:
        return ["joji.jpg"]
    if "creator" in lowered:
        return ["suhel.jpg"]
    if "vana father" in lowered:
        return ["vana.jpg"]
    if "sujitha" in lowered:
        return ["sujitha.jpg"]
    if "who created you" in lowered:
        return ["suhel.jpg"]
    return []
