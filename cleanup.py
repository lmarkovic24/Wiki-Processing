from collections import defaultdict

INPUT_FILE = "output.txt"
OUTPUT_FILE = "output_lowercase.txt"

# word -> [unique_articles_sum, total_count_sum]
merged = defaultdict(lambda: [0, 0])

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        try:
            word, unique_articles, total_count = line.split("|")

            # Case-insensitive merge
            word_lower = word.lower()

            merged[word_lower][0] += int(unique_articles)
            merged[word_lower][1] += int(total_count)

        except ValueError:
            print(f"Skipping malformed line: {line}")

# Save result
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for word, (unique_articles, total_count) in merged.items():
        f.write(f"{word}|{unique_articles}|{total_count}\n")

print(f"Done. Saved to {OUTPUT_FILE}")