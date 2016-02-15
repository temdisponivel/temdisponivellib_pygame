import temdisponivellib
import traceback


def handle_exception():
    print traceback.format_exc()
    if temdisponivellib.raise_exception:
        raise