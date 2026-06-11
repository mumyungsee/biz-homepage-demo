"""
Claude Design 핸드오프 번들(.bin/gzip/tar) 압축 해제 + 정리 스크립트

Claude Design(claude.ai/design)에서 받은 핸드오프 파일을 받으면
project/, chats/, README.md 구조로 압축 해제하고
docs/design-handoff/ 아래로 정리해 보관한다.

사용법:
  python unpack_handoff.py <받은파일경로> [버전이름]

예시:
  python unpack_handoff.py "C:/Users/user/Downloads/data.bin" v2

버전이름 생략 시 오늘 날짜(YYYY-MM-DD)로 폴더 생성.
결과: docs/design-handoff/<버전이름>/{README.md, chats/, project/}
"""
import gzip
import shutil
import sys
import tarfile
import tempfile
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src_file = Path(sys.argv[1])
    if not src_file.exists():
        print(f"파일을 찾을 수 없음: {src_file}")
        sys.exit(1)

    version = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()

    project_root = Path(__file__).parent.parent
    dest_dir = project_root / "docs" / "design-handoff" / version
    dest_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # gzip 해제 시도
        tar_path = tmp_path / "bundle.tar"
        try:
            with gzip.open(src_file, "rb") as f_in, open(tar_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        except gzip.BadGzipFile:
            tar_path = src_file  # 이미 tar인 경우

        with tarfile.open(tar_path) as tf:
            tf.extractall(tmp_path)

        # 추출 결과에서 최상위 폴더(보통 'untitled' 등) 찾아서 내용물만 옮김
        extracted_items = [p for p in tmp_path.iterdir() if p.name != "bundle.tar"]
        if len(extracted_items) == 1 and extracted_items[0].is_dir():
            source_root = extracted_items[0]
        else:
            source_root = tmp_path

        for item in source_root.iterdir():
            target = dest_dir / item.name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            shutil.move(str(item), str(target))

    print(f"완료: {dest_dir}")
    print("내용물:")
    for p in sorted(dest_dir.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(dest_dir)}")


if __name__ == "__main__":
    main()
