#!/usr/bin/env python3
"""
Pack every text file under --src into a gz-compressed JSON-Lines file

One record ➜ one file, following:
{
  "text": "...entire file contents...",
  "id": "<uuid4>",
  "metadata": {
      "filename": "<basename>",
      "language": "<de|rm|unknown>",a
      "language_script": "Latn",
      "source": "convivenza_blogs"
  }
}
"""

import argparse, gzip, json, os, pathlib, uuid, sys

def detect_language(path: pathlib.Path) -> str:
    """Infer language from filename extension (.de / .rm)."""
    ext = path.suffix.lstrip(".").lower()
    return ext if ext in {"de", "rm"} else "unknown"

def iter_text_files(root: pathlib.Path):
    """Yield all regular files under *root* in lexicographic order."""
    for p in sorted(root.rglob("*")):          # <- sort once, simplest
        if p.is_file():
            yield p



def build_record(path: pathlib.Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="latin-1")
    return {
        "text": text,
        "id": str(uuid.uuid4()),
        "metadata": {
            "language": "rm",
            "language_script": "Latn",
        },
    }



def main(src: str, out: str):
    src_root = pathlib.Path(src).expanduser().resolve()
    if not src_root.is_dir():
        sys.exit(f"Source directory not found: {src_root}")

    out_path = pathlib.Path(out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with gzip.open(out_path, "wt", encoding="utf-8") as fout:
        for path in iter_text_files(src_root):
            rec = build_record(path)
            json.dump(rec, fout, ensure_ascii=False)
            fout.write("\n")

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a folder of .de/.rm text files to gzipped JSON-Lines"
    )
    parser.add_argument(
        "--src", required=True, help="Source directory containing the files"
    )
    parser.add_argument(
        "--out", required=True, help="Output file name (should end in .jsonl.gz)"
    )
    args = parser.parse_args()
    main(src=args.src, out=args.out)
