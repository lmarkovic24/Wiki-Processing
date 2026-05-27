import re
import json
import html
from libzim.reader import Archive

CYRILLIC_RE = re.compile(r'^[\u0400-\u04FF]+$')

# Total number of occurrences
counts = {}

# Number of unique articles
unique_article_counts = {}

CHARS_TO_REMOVE = "\n\r ,.;=+?!()[]{}<>:\"'*/\\|-_—"

SAVE_EVERY = 250_000


def save_to_file():

    print("Saving...")

    with open("count.json", "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=4, ensure_ascii=False)

    with open("unique_articles.json", "w", encoding="utf-8") as f:
        json.dump(unique_article_counts, f, indent=4, ensure_ascii=False)

    print("Saved.")


def process_zim(zim_file_path):

    archive = Archive(zim_file_path)

    total_entries = archive.all_entry_count

    for idx in range(total_entries):

        if idx % 1000 == 0:
            print(f"Processed {idx:,}/{total_entries:,}")

        if idx > 0 and idx % SAVE_EVERY == 0:
            save_to_file()

        try:
            entry = archive._get_entry_by_id(idx)

            if entry.is_redirect:
                continue

            try:
                item = entry.get_item()

                html_content = bytes(item.content).decode(
                    "utf-8",
                    errors="replace"
                )

                html_content = html.unescape(html_content)

            except Exception:
                continue

            seen_in_article = set()

            for word in html_content.split():

                for c in CHARS_TO_REMOVE:
                    word = word.replace(c, "")

                if not word:
                    continue

                if not CYRILLIC_RE.fullmatch(word):
                    continue

                counts[word] = counts.get(word, 0) + 1

                if word not in seen_in_article:

                    seen_in_article.add(word)

                    unique_article_counts[word] = (
                        unique_article_counts.get(word, 0) + 1
                    )

        except Exception:
            continue



ZIM_PATH = "srb2.zim"


process_zim(ZIM_PATH)

save_to_file()

print("Done.")