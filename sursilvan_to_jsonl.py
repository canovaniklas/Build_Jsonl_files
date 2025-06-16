#!/usr/bin/env python3
"""
Convert the NVS dictionary JSON export to gzipped JSON-Lines.

Usage
-----
python nvs_to_jsonl.py --in nvs.json --out nvs_entries.jsonl.gz
"""

import argparse, gzip, json, uuid, pathlib

# --------------------------------------------------------------------------- #
def load_entries(path: pathlib.Path):
    """Return the `.data` array inside the first object whose type=='table'."""
    obj_list = json.loads(path.read_text(encoding="utf-8"))
    for item in obj_list:
        if item.get("type") == "table" and "data" in item:
            return item["data"], item["name"]
    raise RuntimeError("No table object with data array found.")


def entry_to_record(entry: dict, dict_name: str) -> dict:
    """Flatten one dictionary entry into our standard schema."""
    parts = [
        entry.get("RStichwort", ""),
        entry.get("Corp", ""),
        entry.get("Redewendung", ""),
        entry.get("Etymologie", ""),
    ]
    # keep only non-empty chunks, join with newlines
    text = "\n".join(p.strip() for p in parts if p.strip())

    return {
        "text": text,
        "id": str(uuid.uuid4()),
        "metadata": {
            "dictionary": dict_name,
            "cn_DS": entry.get("cn_DS"),
            "RStichwort": entry.get("RStichwort"),
            "DStichwort": entry.get("DStichwort"),
            "language": "rm&de",          # everything is Romansh-led
            "language_script": "Latn",
            "idiom": "Sursilvan",
            "source": "NVS_json_export",
        },
    }



def main(inp: str, out: str):
    in_path = pathlib.Path(inp).expanduser().resolve()
    out_path = pathlib.Path(out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    entries, dict_name = load_entries(in_path)

    with gzip.open(out_path, "wt", encoding="utf-8") as gz:
        for e in entries:
            rec = entry_to_record(e, dict_name)
            json.dump(rec, gz, ensure_ascii=False)
            gz.write("\n")

    print(f"Wrote {out_path}  ({len(entries)} entries)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Flatten NVS dictionary JSON")
    ap.add_argument("--in",  required=True, help="Path to original JSON file")
    ap.add_argument("--out", required=True, help="Output .jsonl.gz file")
    args = ap.parse_args()
    main(inp=args.__dict__['in'], out=args.out)
