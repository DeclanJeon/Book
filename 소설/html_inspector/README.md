# HTML Inspector

URL을 입력하면 해당 페이지의 HTML 구조를 가져와서 보여주는 간단한 도구.

## 실행 방법

```bash
cd /home/declan/Documents/Book/소설/html_inspector
/home/declan/Documents/Book/소설/venv/bin/python app.py
```

브라우저에서 <http://127.0.0.1:5000> 접속.

## 기능

- URL 입력 후 "가져오기" 버튼 (또는 Enter)
- **Pretty / Raw** 모드 토글
- **들여쓰기** 크기 조절 (1~8)
- 결과 메타 정보 표시 (HTTP 상태, 최종 URL, Content-Type, 인코딩, 크기)
- 클립보드 복사, 파일로 저장 (.html 다운로드)
- HTML 구문 강조 (태그/속성/문자열/주석 색상 구분)

## API

`GET /api/fetch?url=<URL>&mode=pretty|raw&indent=<1~8>`

성공 시:
```json
{
  "ok": true,
  "url": "https://example.com/",
  "status": 200,
  "content_type": "text/html; charset=UTF-8",
  "final_encoding": "ISO-8859-1",
  "size_bytes": 559,
  "mode": "pretty",
  "html": "<!DOCTYPE html>\n..."
}
```

실패 시 `{"ok": false, "error": "사유"}`.

## 파일

- `app.py` — Flask 백엔드
- `templates/index.html` — UI (CSS/JS 포함, 단일 파일)

## 제한

- 응답 크기 10MB 초과 시 거부
- 타임아웃 15초
- http/https만 허용