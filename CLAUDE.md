# 소상공인-홈페이지_demo 작업 규칙

## 워크플로우
컨설팅(전략/페르소나) → PRD → Claude Design(claude.ai/design) → GPT 이미지 생성 → 코드 적용

## 자동화 스크립트 (scripts/)
아래 상황이 되면 묻지 말고 바로 실행:

- **GPT로 만든 이미지를 받으면** → `python scripts/import_images.py <폴더> exterior=... interior=... handdrip=... cheesecake=...`로 `src/images/` 표준 이름에 배치
- **Claude Design 핸드오프 파일을 받으면** → `python scripts/unpack_handoff.py <받은파일경로>`로 `docs/design-handoff/날짜/`에 정리 후 내용 반영
- **index.html의 이미지/사진 관련 수정 후** → `python scripts/check_images.py`로 src/alt 매칭·파일 존재 검증

자세한 사용법은 `scripts/README.md` 참고.
