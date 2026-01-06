from __future__ import annotations

from json import dump
from pathlib import Path
from subprocess import Popen
from sys import executable

from backend.app.__main__ import app


if __name__ == '__main__':
    with open('openapi.yaml', 'w') as f:
        dump(app.openapi(), f, indent=4)

    Popen(
        [
            Path(executable).parent / 'openapi-generator-cli',
            'generate',
            '-i',
            'openapi.yaml',
            '-g',
            'typescript-angular',
            '-o',
            '../wf-frontend/src/lib',
        ],
    ).wait()
