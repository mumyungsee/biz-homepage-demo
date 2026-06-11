"""
GPT로 생성한 이미지를 src/images/ 표준 이름으로 복사/리네임하는 스크립트

사용법:
  python import_images.py <원본폴더> exterior=파일1.png interior=파일2.png handdrip=파일3.png cheesecake=파일4.png

예시:
  python import_images.py "C:/Users/user/Downloads" exterior=gen1.png interior=gen2.png handdrip=gen3.png cheesecake=gen4.png

표준 이름 (src/images/ 안에 생성됨):
  exterior.png  - 가게 외관
  interior.png  - 가게 내부
  handdrip.png  - 핸드드립 커피
  cheesecake.png - 바스크 치즈케이크

새 슬롯이 필요하면 STANDARD_NAMES에 추가하면 됨.
"""
import shutil
import sys
from pathlib import Path

STANDARD_NAMES = {"exterior", "interior", "handdrip", "cheesecake"}

sys.stdout.reconfigure(encoding="utf-8")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    src_folder = Path(sys.argv[1])
    if not src_folder.is_dir():
        print(f"폴더를 찾을 수 없음: {src_folder}")
        sys.exit(1)

    images_dir = Path(__file__).parent.parent / "src" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    for arg in sys.argv[2:]:
        if "=" not in arg:
            print(f"형식 오류 (slot=파일명 형태여야 함): {arg}")
            continue

        slot, filename = arg.split("=", 1)
        slot = slot.strip().lower()

        if slot not in STANDARD_NAMES:
            print(f"알 수 없는 슬롯 '{slot}' (허용: {sorted(STANDARD_NAMES)}) -- 그래도 진행함")

        source_path = src_folder / filename
        if not source_path.exists():
            print(f"[건너뜀] 원본 파일 없음: {source_path}")
            continue

        ext = source_path.suffix.lower()
        target_path = images_dir / f"{slot}{ext}"

        shutil.copy2(source_path, target_path)
        print(f"[완료] {source_path.name} -> {target_path.relative_to(images_dir.parent.parent)}")

    print("\n완료. check_images.py로 매핑 확인 권장.")


if __name__ == "__main__":
    main()
