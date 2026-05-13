import os
from pathlib import Path

def rename_https_files(root_dir, dry_run=False):
    root = Path(root_dir)
    if not root.is_dir():
        print(f"? Error: '{root_dir}' bukan folder yang valid.")
        return

    count = 0
    for file_path in root.rglob('index-https.html'):
        new_path = file_path.with_name('index.html')
        if new_path.exists():
            print(f"??  Skip: {file_path} (index.html sudah ada)")
        else:
            if dry_run:
                print(f"?? Dry-run: Akan rename {file_path} -> {new_path}")
            else:
                try:
                    file_path.rename(new_path)
                    print(f"? Rename: {file_path.name} -> {new_path.name} ({new_path.parent})")
                    count += 1
                except Exception as e:
                    print(f"? Gagal rename {file_path}: {e}")
    
    if not dry_run:
        print(f"\n?? Selesai! Total {count} file berhasil di-rename.")

if __name__ == '__main__':
    target = input("Masukkan path folder: ").strip().strip('"')
    # Ubah dry_run=True untuk mencoba tanpa mengubah file asli
    rename_https_files(target, dry_run=False)