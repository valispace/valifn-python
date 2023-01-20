from pathlib import Path
from typing import Dict, Any
import oct2py # pylint: disable=import-error


def main(**kwargs) -> Dict[str, Any]:
    """
    This is the main function to execute your script and it must exists.
    You shouldn't modify this function unless you are familiar with oct2py.

    Other functions and files can be also created. You have at your disposal
    to import Valispace API, oct2py, scipy, numpy and pint.

    :param kwargs: Dictionary with data received from Valispace.
    :type kwargs: Dict[str, Any]

    :return: Dictionary with data to send back to Valispace.
    :rtype: Dict[str, Any]
    """
    # Initialize octave and add all .m files to octave
    octave = oct2py.Oct2Py()
    octave.addpath(str(Path(__file__).resolve().parent))

    # Run main function from main.m and send response back to Valispace
    return octave.main(kwargs)
