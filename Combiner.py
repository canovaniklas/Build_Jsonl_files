import argparse, itertools, json, sys

CODE_TO_NAME = {
    "de": "German",
    "fr": "French",
    "it": "Italian",
    "en": "English",
    "rm": "Rumantsch Grischun",
}

def guess_name(obj):
    code = (
        obj.get("metadata", {}).get("language")      # preferred
        or obj.get("lang")                           # fallbacks
        or obj.get("language")
    )
    return CODE_TO_NAME.get(code, code or "Unknown")

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def main(src_path, tgt_path, out_path, src_name):
    with open(out_path, "w", encoding="utf-8") as out:
        for src_obj, tgt_obj in itertools.zip_longest(
            read_jsonl(src_path), read_jsonl(tgt_path)
        ):
            if src_obj is None or tgt_obj is None:
                sys.exit("Error: the two files do not have the same number of lines.")
            lang = src_name or guess_name(src_obj)
            header = f"This is a text translated from {lang} to Rumantsch Grischun."
            combined = f"{header}\n{src_obj['text']}\n{tgt_obj['text']}"
            json.dump({"text": combined}, out, ensure_ascii=False)
            out.write("\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source_jsonl", help="File with texts in the original language")
    ap.add_argument("target_jsonl", help="Corresponding Rumantsch Grischun file")
    ap.add_argument("output_jsonl", help="Where to write the interleaved result")
    ap.add_argument("--source-name", help="Human-readable name of the original language")
    args = ap.parse_args()
    main(args.source_jsonl, args.target_jsonl, args.output_jsonl, args.source_name)
