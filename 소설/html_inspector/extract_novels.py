"""HTML에서 제목+본문을 추출해 JSON으로 저장"""
import json
import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup

SRC_DIR = Path("/home/declan/Documents/Book/소설/html-inspector-20260830-173241")
OUT_JSON = Path("/home/declan/Documents/Book/소설/html_inspector/_extracted.json")


def extract_one(path: Path) -> dict | None:
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    for sel in (".p-novel__title", "h1.p-novel__title", "h1"):
        el = soup.select_one(sel)
        if el:
            title = el.get_text(strip=True)
            break
    if not title and soup.title:
        title = soup.title.get_text(strip=True)
    title = title.replace(" -", "-").strip(" -")

    body = None
    for sel in (".p-novel__body", "#novel_honbun", ".novel_body", ".p-novel__text"):
        el = soup.select_one(sel)
        if el:
            body = el
            break
    if body is None:
        return None

    paragraphs = []
    for p in body.find_all("p", recursive=True):
        text = p.get_text("\n", strip=True)
        if not text or text == "\n":
            continue
        paragraphs.append(text)

    seen = set()
    unique = []
    for p in paragraphs:
        key = p.strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(p)
    if not unique:
        return None

    return {
        "file": path.name,
        "title": title,
        "body": "\n\n".join(unique),
    }


def main() -> int:
    files = sorted(SRC_DIR.glob("*.html"))
    items = []
    skipped = 0
    for f in files:
        item = extract_one(f)
        if item is None:
            skipped += 1
            print(f"  SKIP {f.name}", file=sys.stderr)
            continue
        items.append(item)
    OUT_JSON.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    total_chars = sum(len(i["body"]) for i in items)
    print(f"추출: {len(items)}개 / 스킵 {skipped} / 본문 총 {total_chars:,}자 / 평균 {total_chars // max(len(items),1):,}자")
    return 0


if __name__ == "__main__":
    sys.exit(main())