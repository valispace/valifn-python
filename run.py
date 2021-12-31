import argparse
import json
import traceback

from encoders import JSONEncoder
from pathlib import Path


def run_script(**kwargs) -> str:
    """
    Execute main function from script.

    The code function will be replaced when container is built
    by the code from the script.

    :return: JSON string with the execution's result.
    :rtype: str
    """
    # Parse arguments from calling script (expected data as JSON)
    parser = argparse.ArgumentParser(description='Call script with specific data and return url')
    parser.add_argument('data', type=str, default=dict(), help='Data with kwargs to execute script as JSON')
    args = parser.parse_args()
    data = json.loads(args.data)

    try:
        # Execute script
        # --------------------------------------------------
        # NOTE: Import code from here to be capture and send back
        # as an error in case it fails or file does not exist
        from script_code.main import main
        result = json.dumps(main(**data) or {}, cls=JSONEncoder)

    except Exception as exc:
        result = json.dumps({
            'error': str(exc),
            'traceback': traceback.format_exc(),
        })

    # Write result to file for ValiFn to be able to read it
    BASE_DIR = Path(__file__).resolve().parent
    with open(BASE_DIR / 'result.json', 'w') as f:
        f.write(result)

if __name__ == '__main__':
   run_script()
