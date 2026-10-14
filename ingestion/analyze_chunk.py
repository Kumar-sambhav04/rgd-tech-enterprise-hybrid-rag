import json
from pathlib import Path
from statistics import mean


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNK_FILE = BASE_DIR / "data" / "chunk_preview.json"


def main():

    chunks = json.loads(
        CHUNK_FILE.read_text(encoding="utf-8")
    )

    lengths = [
        len(chunk["chunk_text"])
        for chunk in chunks
    ]

    print("\n======== Chunk Analysis ========\n")

    print("Total chunks :", len(chunks))
    print("Minimum size :", min(lengths))
    print("Maximum size :", max(lengths))
    print("Average size :", round(mean(lengths), 2))

    tiny_chunks = [
        chunk
        for chunk in chunks
        if len(chunk["chunk_text"]) < 100
    ]

    large_chunks = [
        chunk
        for chunk in chunks
        if len(chunk["chunk_text"]) > 1200
    ]

    print("\nTiny chunks (<100 chars):", len(tiny_chunks))
    print("Large chunks (>1200 chars):", len(large_chunks))

    if tiny_chunks:

        print("\n--- Tiny chunks ---")

        for chunk in tiny_chunks:

            print(
                chunk["id"],
                "|",
                chunk["section"],
                "|",
                len(chunk["chunk_text"])
            )

    if large_chunks:

        print("\n--- Large chunks ---")

        for chunk in large_chunks:

            print(
                chunk["id"],
                "|",
                chunk["section"],
                "|",
                len(chunk["chunk_text"])
            )


if __name__ == "__main__":
    main()