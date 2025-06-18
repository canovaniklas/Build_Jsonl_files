import json
from pathlib import Path

JSONL_PATH = Path("/Users/niklascanova/Desktop/SwissAI/ToBeUploaded/allegra-interleaved-de-rm.jsonl")  
HEAD_LEN   = 100

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
    # print number of lines in the file
    print(f"Total lines: {sum(1 for _ in JSONL_PATH.open(encoding='utf-8'))}")
    
    # text entry of the 100th line
    with JSONL_PATH.open(encoding="utf-8") as fh:
        for _ in range(99):
            next(fh)
        hundredth_line = next(fh)
        print(f"100th line: {hundredth_line.strip()}")

