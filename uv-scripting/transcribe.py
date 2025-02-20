#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mlx_whisper",
# ]
# ///


import sys
import argparse
from mlx_whisper.cli import main, build_parser


def main_with_defaults():
  original_args = sys.argv[1:]
  default_args = [
    "--model", "mlx-community/whisper-turbo",
    "--output-dir", "/Users/markhneedham/Downloads/transcripts",
    "--output-format", "all"
  ]
    
  sys.argv[1:] = default_args + original_args  
  return main()

if __name__ == "__main__":
  sys.exit(main_with_defaults())
