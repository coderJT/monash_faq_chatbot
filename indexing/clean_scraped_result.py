from trafilatura import extract
import os

from bs4 import BeautifulSoup

def preclean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for h in soup.find_all(['h1', 'h2', 'h3']):
        h.insert_before("\n\n## " + h.get_text(strip=True) + "\n")

    for ul in soup.find_all(["ul", "ol"]):
        bullets = []
        for li in ul.find_all("li"):
            bullets.append("• " + li.get_text(strip=True))
        ul.replace_with("\n".join(bullets))

    return str(soup)

os.makedirs("cleaned", exist_ok=True)

for filename in os.listdir("pages"):
    if not filename.endswith(".txt"):
        continue

    try:
        with open(f"pages/{filename}", encoding="utf-8") as f:
            html = f.read()
        
        cleaned_html = preclean_html(html)
        text = extract(cleaned_html, include_tables=True, include_links=True)
        
        if text and text.strip():
            out_path = f"cleaned/{filename.replace('.txt', '.clean.txt')}"
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(text)
        else:
            print(f"[Empty] No extractable text in: {filename}")

    except Exception as e:
        print(f"[Error] Failed to process {filename}: {e}")