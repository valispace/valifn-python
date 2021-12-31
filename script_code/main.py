from typing import Any, Dict


def main(*args, **kwargs) -> Dict[str, Any]:
    """
    This file and folder will be replaced when container is built.
    """
    return {'result': 'Hello World!'}
