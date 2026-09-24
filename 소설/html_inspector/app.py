"""HTML Inspector - URL을 입력하면 해당 페이지의 HTML 구조를 가져와 보여주는 Flask 앱"""
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

MAX_RESPONSE_BYTES = 10 * 1024 * 1024
REQUEST_TIMEOUT = 15
MAX_FILENAME_LEN = 80
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Accept-Encoding": "identity",
}


def _normalize_url(url: str) -> tuple[str, str | None]:
    """URL을 정규화하고 (url, error) 반환. error가 None이면 정상."""
    url = url.strip()
    if not url:
        return "", "URL을 입력해주세요."

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", url):
        url = "https://" + url

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return "", "URL은 http 또는 https로 시작해야 합니다."
    if not parsed.netloc:
        return "", "유효한 호스트가 없습니다."

    return url, None


def _reindent(text: str, indent_size: int) -> str:
    """BeautifulSoup.prettify() 결과의 들여쓰기 단위를 indent_size에 맞춘다."""
    if indent_size <= 1:
        return text
    base = 1
    lines = text.split("\n")
    out = []
    for line in lines:
        stripped = line.lstrip(" ")
        spaces = len(line) - len(stripped)
        if spaces == 0:
            out.append(line)
        else:
            level = spaces // base
            remainder = spaces % base
            out.append(" " * (level * indent_size + remainder) + stripped)
    return "\n".join(out)


def _pretty_html(html: str, indent_size: int = 2) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return _reindent(soup.prettify(formatter="html5"), indent_size)


def _fetch_one(raw_url: str, indent_size: int = 2) -> dict:
    """단일 URL을 가져와서 결과 dict 반환.
    성공 시 'raw'(원본 문자열)와 'pretty'(들여쓰기 정리본)를 모두 포함.
    실패 시 ok=False, error 포함.
    """
    result = {"requested": raw_url}
    url, err = _normalize_url(raw_url)
    if err:
        result["ok"] = False
        result["error"] = err
        return result

    result["url"] = url
    try:
        resp = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        result["ok"] = False
        result["error"] = "요청 시간이 초과되었습니다 (15s)."
        return result
    except requests.exceptions.SSLError:
        result["ok"] = False
        result["error"] = "SSL 인증서 오류가 발생했습니다."
        return result
    except requests.exceptions.ConnectionError as e:
        result["ok"] = False
        result["error"] = f"연결 실패: {str(e)[:200]}"
        return result
    except requests.exceptions.HTTPError as e:
        result["ok"] = False
        result["error"] = f"HTTP 오류: {e.response.status_code}"
        result["status"] = e.response.status_code
        return result
    except requests.exceptions.RequestException as e:
        result["ok"] = False
        result["error"] = f"요청 실패: {str(e)[:200]}"
        return result

    raw_bytes = resp.content
    if len(raw_bytes) > MAX_RESPONSE_BYTES:
        result["ok"] = False
        result["error"] = (
            f"응답이 너무 큽니다 ({len(raw_bytes):,} bytes). "
            f"최대 {MAX_RESPONSE_BYTES:,} bytes."
        )
        return result

    encoding = resp.encoding or resp.apparent_encoding or "utf-8"
    try:
        raw_html = raw_bytes.decode(encoding, errors="replace")
    except LookupError:
        raw_html = raw_bytes.decode("utf-8", errors="replace")

    result["ok"] = True
    result["url"] = resp.url
    result["status"] = resp.status_code
    result["contentType"] = resp.headers.get("Content-Type", "")
    result["finalEncoding"] = encoding
    result["sizeBytes"] = len(raw_bytes)
    result["raw"] = raw_html
    result["pretty"] = _pretty_html(raw_html, indent_size=max(1, min(indent_size, 8)))
    return result


def _safe_filename_for(url: str, idx: int, used: set) -> str:
    """001_도메인.html 형식. 중복은 -2, -3 접미사."""
    try:
        parsed = urlparse(url)
        host = (parsed.netloc or "site").replace(":", "_")
        path = parsed.path.strip("/").replace("/", "_") if parsed.path.strip("/") else "index"
    except Exception:
        host, path = "site", "index"

    base = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{host}_{path}")[:MAX_FILENAME_LEN].strip("._")
    if not base:
        base = "page"
    name = f"{idx:03d}_{base}.html"

    candidate = name
    n = 2
    while candidate.lower() in used:
        candidate = f"{idx:03d}_{base}-{n}.html"
        n += 1
    used.add(candidate.lower())
    return candidate


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/fetch")
def api_fetch():
    raw_url = request.args.get("url", "")
    mode = request.args.get("mode", "pretty")
    indent_size = int(request.args.get("indent", "2"))

    url, err = _normalize_url(raw_url)
    if err:
        return jsonify({"ok": False, "error": err}), 400

    result = _fetch_one(raw_url, indent_size=indent_size)
    if not result.get("ok"):
        status = result.get("status") or 502
        return jsonify({"ok": False, "error": result.get("error", "실패")}), status

    if mode == "raw":
        result["html"] = result["raw"]
    else:
        result["html"] = result["pretty"]
    result["mode"] = mode
    result.pop("raw", None)
    result.pop("pretty", None)
    return jsonify(result)


@app.route("/api/batch", methods=["POST"])
def api_batch():
    """여러 URL을 처리해 zip으로 스트리밍."""
    data = request.get_json(silent=True) or {}
    urls = data.get("urls") or []
    if not isinstance(urls, list):
        return jsonify({"ok": False, "error": "urls는 배열이어야 합니다."}), 400
    if not urls:
        return jsonify({"ok": False, "error": "URL이 비어있습니다."}), 400

    indent_size = int(data.get("indent", 2))
    seen_filenames: set = set()
    results: list[dict] = []
    error_lines: list[str] = []

    for i, raw in enumerate(urls, start=1):
        if not isinstance(raw, str):
            continue
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        r = _fetch_one(raw, indent_size=indent_size)
        r["index"] = i
        results.append(r)
        if r.get("ok"):
            filename = _safe_filename_for(r.get("url") or raw, i, seen_filenames)
            r["filename"] = filename
        else:
            error_lines.append(
                f"[{i:03d}] {raw} -> {r.get('error', 'unknown error')}"
            )

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    zip_name = f"html-inspector-{timestamp}.zip"
    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "total": len(urls),
        "processed": len(results),
        "succeeded": sum(1 for r in results if r.get("ok")),
        "failed": sum(1 for r in results if not r.get("ok")),
        "items": [
            {
                "index": r.get("index"),
                "requested": r.get("requested"),
                "url": r.get("url"),
                "filename": r.get("filename"),
                "ok": r.get("ok"),
                "status": r.get("status"),
                "contentType": r.get("contentType"),
                "sizeBytes": r.get("sizeBytes"),
                "error": r.get("error") if not r.get("ok") else None,
            }
            for r in results
        ],
    }

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for r in results:
            if not r.get("ok") or "pretty" not in r:
                continue
            zf.writestr(r["filename"], r["pretty"])
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        if error_lines:
            zf.writestr("errors.log", "\n".join(error_lines) + "\n")
        else:
            zf.writestr("errors.log", "(no errors)\n")

    buf.seek(0)
    return Response(
        buf.getvalue(),
        mimetype="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{zip_name}"',
            "X-Stats-Succeeded": str(manifest["succeeded"]),
            "X-Stats-Failed": str(manifest["failed"]),
        },
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)