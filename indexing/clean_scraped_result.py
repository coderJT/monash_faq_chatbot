from trafilatura import extract
import os

from bs4 import BeautifulSoup

def preclean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for h in soup.find_all(['h1', 'h2', 'h3']):
        h.insert_before("\n\n## " + h.get_text(strip=True) + "\n")

    for ul in soup.find_all(['ul', 'ol']):
        bullets = []
        for li in ul.find_all('li', recursive=False):
            # Check for links
            link = li.find('a')
            if link:
                text = link.get_text(strip=True)
                href = link.get('href')
                bullets.append(f"• [{text}]({href})")
            else:
                bullets.append("• " + li.get_text(strip=True))
        ul.replace_with("\n" + "\n".join(bullets) + "\n")

    for box in soup.find_all(class_='semester-box'):
        output = []
        # Get semester title
        title = box.find(class_='semester-title')
        if title:
            output.append(f"\n\n### {title.get_text(strip=True)}")

        # Get each event with <strong> and <br>
        for obj in box.find_all(class_='semester-object'):
            strong = obj.find('strong')
            label = strong.get_text(strip=True) if strong else ""
            strong.extract() if strong else None

            # Get remaining value text
            value = obj.get_text(" ", strip=True)
            if label and value:
                output.append(f"- {label}: {value}")
            elif label:
                output.append(f"- {label}")
            elif value:
                output.append(f"- {value}")

        # Replace the box with our clean markdown
        box.replace_with("\n".join(output))


    return str(soup)

os.makedirs("cleaned", exist_ok=True)

for filename in os.listdir("pages"):
    if not filename.endswith(".txt"):
        continue

    try:
        with open(f"pages/{filename}", encoding="utf-8") as f:
            html = f.read()
        
        cleaned_html = preclean_html(html)
        text = extract(cleaned_html, favor_precision=False, include_tables=True, include_links=True)
        
        if text and text.strip():
            out_path = f"cleaned/{filename.replace('.txt', '.clean.txt')}"
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(text)
        else:
            print(f"[Empty] No extractable text in: {filename}")

    except Exception as e:
        print(f"[Error] Failed to process {filename}: {e}")