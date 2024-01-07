import ast
from pathlib import Path
from typing import Callable

from doclint.core.rating import Difficulty, rate_text


def process(
    path: Path,
    error_callback: Callable[[str], None],
    warning_callback: Callable[[str], None],
) -> bool:
    with open(path, mode="r") as f:
        file = f.read()

    try:
        tree = ast.parse(file)
    except SyntaxError:
        error_callback(f"Anaylsis failed: '{path}' contains invalid Python syntax.")
        exit(1)

    has_errors = False

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if docstring := ast.get_docstring(node):
                difficulty = rate_text(docstring)
                if difficulty == Difficulty.VERY_HARD:
                    has_errors = True
                    error_callback(f"Docstring too complicated. Line: {node.lineno}")
                elif difficulty == Difficulty.HARD:
                    has_errors = True
                    warning_callback(f"Docstring complicated. Line: {node.lineno}")
        elif isinstance(node, ast.Module):
            if docstring := ast.get_docstring(node):
                difficulty = rate_text(docstring)
                if difficulty == Difficulty.VERY_HARD:
                    has_errors = True
                    error_callback(
                        f"Module docstring too complicated. File: {path.name}"
                    )
                elif difficulty == Difficulty.HARD:
                    has_errors = True
                    warning_callback(f"Module docstring complicated. File: {path.name}")

    return has_errors
