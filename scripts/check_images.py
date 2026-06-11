"""
이미지-슬롯 매핑 검증 스크립트

index.html에서 <img src="images/...">와 alt 텍스트를 추출해서
1. 파일이 실제 존재하는지
2. src 파일명과 alt 텍스트가 서로 어울리는지(키워드 매칭)
를 점검한다.

사용법: python check_images.py [index.html 경로]
       (경로 생략 시 ../src/index.html)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# 파일명 키워드 -> 그 사진이어야 의미가 통하는 alt 키워드들
KEYWORD_MAP = {
    "handdrip": ["핸드드립", "드립", "커피", "hand drip"],
    "cheesecake": ["치즈케이크", "케이크", "cheesecake"],
    "interior": ["내부", "공간", "편안", "인테리어", "interior"],
    "exterior": ["외관", "가게", "입구", "exterior"],
}


def main():
    html_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "src" / "index.html"
    html_path = html_path.resolve()

    if not html_path.exists():
        print(f"파일을 찾을 수 없음: {html_path}")
        sys.exit(1)

    html = html_path.read_text(encoding="utf-8")
    src_dir = html_path.parent

    img_tags = re.findall(r'<img\s+[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>', html)

    if not img_tags:
        print("img 태그를 찾지 못함.")
        return

    problems = []

    for src, alt in img_tags:
        img_path = (src_dir / src).resolve()
        exists = img_path.exists()

        if not exists:
            problems.append(f"  [파일 없음] {src} (alt=\"{alt}\")")
            continue

        filename_key = next((k for k in KEYWORD_MAP if k in src.lower()), None)
        if filename_key:
            expected = KEYWORD_MAP[filename_key]
            if not any(kw in alt for kw in expected):
                problems.append(
                    f"  [매칭 의심] {src} (alt=\"{alt}\") "
                    f"-> 파일명은 '{filename_key}' 계열인데 alt에 관련 단어가 없음"
                )

    print(f"검사 대상: {html_path}")
    print(f"img 태그 {len(img_tags)}개 발견\n")

    if problems:
        print("문제 발견:")
        for p in problems:
            print(p)
        sys.exit(1)
    else:
        print("이상 없음 — 파일 존재 + 파일명/alt 매칭 정상")


if __name__ == "__main__":
    main()
