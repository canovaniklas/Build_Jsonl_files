#!/usr/bin/env python3
"""
Combiner.py – interleave two parallel-text JSONL files.

Each input line must be a JSON object containing at least the key "text".
The output file (plain or .gz) will contain one JSON object per line:

  {"text": "This is a text translated from <SOURCE-LANG> to Rumantsch Grischun.\n<src>\n<tgt>"}

Usage
-----
    python Combiner.py  <SOURCE.jsonl>  <TARGET.jsonl>  <OUTPUT.jsonl[.gz]> \
        [--source-name "<Readable language name>"]

Example
-------
    python Combiner.py \
        "/Users/niklascanova/Desktop/allegra-raw-2012-05-07(2)/it/Ciao.jsonl" \
        "/Users/niklascanova/Desktop/allegra-raw-2012-05-07(2)/rm/Bundi.jsonl" \
        "/Users/niklascanova/Desktop/SwissAI/ToBeUploaded/allegra-interleaved-de-rm.jsonl.gz" \
        --source-name "German"
"""

import argparse, gzip, itertools, json, sys
from pathlib import Path

CODE_TO_NAME = {
    "de": "German",
    "fr": "French",
    "it": "Italian",
    "en": "English",
    "es": "Spanish",
    "pt": "Portuguese",
    "rm": "Rumantsch Grischun",
}


def guess_name(obj):
    """Try to infer a readable language name from metadata in the JSON line."""
    code = (
        obj.get("metadata", {}).get("language")  # preferred
        or obj.get("lang")                       # fallbacks
        or obj.get("language")
    )
    return CODE_TO_NAME.get(code, code or "Unknown")


def read_jsonl(path):
    """Yield JSON objects from a .jsonl file."""
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            if ln.strip():
                yield json.loads(ln)


def smart_open(path, mode="wt"):
    """
    Open *path* normally, or with gzip if the filename ends with .gz.
    Returns a file-like object in text mode.
    """
    path = str(path)
    if path.endswith(".gz"):
        return gzip.open(path, mode, encoding="utf-8")
    return open(path, mode, encoding="utf-8")



def combine(src_path, tgt_path, out_path, src_name):
    with smart_open(out_path, "wt") as out_fh:
        for src_obj, tgt_obj in itertools.zip_longest(
            read_jsonl(src_path), read_jsonl(tgt_path)
        ):
            if src_obj is None or tgt_obj is None:
                sys.exit("Error: the two files do not have the same number of lines.")

            # Determine the readable source language
            lang = src_name or guess_name(src_obj)
            header = f"This is a text translated from {lang} to Rumantsch Grischun."

            # Assemble the combined text field
            combined_text = f"{header}\n{src_obj['text']}\n{tgt_obj['text']}"

            json.dump({"text": combined_text}, out_fh, ensure_ascii=False)
            out_fh.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_jsonl", help="Path to the file with texts in the original language")
    ap.add_argument("target_jsonl", help="Path to the file with Rumantsch Grischun texts")
    ap.add_argument("output_jsonl", help="Path for the interleaved output (.jsonl or .jsonl.gz)")
    ap.add_argument("--source-name", help="Readable name of the original language (e.g. 'German')")
    args = ap.parse_args()

    combine(Path(args.source_jsonl), Path(args.target_jsonl), Path(args.output_jsonl), args.source_name)


if __name__ == "__main__":
    main()
