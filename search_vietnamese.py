import re

with open(r"e:\Bao Cao Ha Dung\Tuan6-Test Huong di ha dung\Project\FAIR_2025_-_9435.pdf.txt", "r", encoding="utf-8") as f:
    text = f.read()

vietnamese_words = ["tóm tắt", "giới thiệu", "phương pháp", "kết quả", "thực nghiệm", "báo cáo", "nghiên cứu"]

with open("search_results.txt", "w", encoding="utf-8") as out:
    for word in vietnamese_words:
        matches = list(re.finditer(word, text, re.IGNORECASE))
        out.write(f"Word '{word}': {len(matches)} matches\n")
        if matches:
            idx = matches[0].start()
            start = max(0, idx - 100)
            end = min(len(text), idx + 200)
            out.write(f"Context: ...{text[start:end]}...\n\n")

print("Done. Saved to search_results.txt")
