import argparse
import json
import sys

from pathlib import Path

from kaas.parser import Parser

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File to convert')
    return parser.parse_args()

def main():
    args = parse_args()
    fp = Path(args.file)
    if not fp.exists():
        print(f"File {fp} does not exist!", file=sys.stderr)
        sys.exit(1)
    if not fp.is_file():
        print(f"Path {fp} is not a file!", file=sys.stderr)
        sys.exit(1)
    text = fp.open().read()
    p = Parser().parse_text(text)
    print(json.dumps(p, indent=4))
