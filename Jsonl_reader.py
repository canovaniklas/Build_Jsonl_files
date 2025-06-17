import json
from pathlib import Path

JSONL_PATH = Path("/Users/niklascanova/Desktop/SwissAI/ToBeUploaded/allegra-de.jsonl")  
HEAD_LEN   = 80

def main() -> None:
    with JSONL_PATH.open(encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(f"{lineno:>5}:  Error ({exc})")
                continue

            snippet  = obj.get("text", "").replace("\n", " ")[:HEAD_LEN]
            language = obj.get("metadata", {}).get("language")
            print(f"{lineno:>5}: [{language}] {snippet}")

if __name__ == "__main__":
    main()
