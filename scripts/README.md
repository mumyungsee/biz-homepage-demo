# 작업 자동화 스크립트

소상공인 홈페이지 데모 워크플로우(컨설팅 → PRD → Claude Design → GPT 이미지 → 코드 적용) 중
반복적인 파일 작업만 자동화한 것. 컨설팅/디자인/코드 통합 같은 판단 작업은 그대로 대화로 진행.

## check_images.py
index.html의 `<img>` src/alt 매칭과 파일 존재 여부 점검.
```
python check_images.py
```

## import_images.py
GPT로 만든 이미지를 `src/images/exterior.png` 등 표준 이름으로 복사.
```
python import_images.py "다운로드폴더경로" exterior=파일1.png interior=파일2.png handdrip=파일3.png cheesecake=파일4.png
```

## unpack_handoff.py
Claude Design 핸드오프 파일 압축 해제 + `docs/design-handoff/날짜/`에 정리.
```
python unpack_handoff.py "받은파일경로"
```
