import os
from pathlib import Path

def delete_https_files(root_dir, dry_run=True):
    root = Path(root_dir)
    if not root.is_dir():
        print(f"? Error: '{root_dir}' bukan folder yang valid.")
        return

    # Cari semua file index-https.html di folder & subfolder
    files = list(root.rglob('index-https.html'))
    if not files:
        print("?? Tidak ada file 'index-https.html' yang ditemukan.")
        return

    print(f"?? Ditemukan {len(files)} file 'index-https.html':")
    for f in files:
        print(f"   - {f}")

    # ?? Mode DRY-RUN (hanya simulasi)
    if dry_run:
        print("\n?? Mode DRY-RUN aktif. Tidak ada file yang dihapus.")
        print("?? Untuk eksekusi nyata, ubah `dry_run=False` di baris pemanggilan script.")
        return

    # ?? Konfirmasi sebelum menghapus permanen
    confirm = input("\n??  File akan dihapus PERMANEN. Lanjutkan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("? Operasi dibatalkan.")
        return

    success = fail = 0
    for f in files:
        try:
            f.unlink()  # Hapus file
            print(f"? Deleted: {f}")
            success += 1
        except PermissionError:
            print(f"?? Gagal (Permission denied): {f}")
            fail += 1
        except Exception as e:
            print(f"? Gagal: {f} | {e}")
            fail += 1

    print(f"\n?? Selesai! Berhasil: {success} | Gagal: {fail}")

if __name__ == '__main__':
    target = input("Masukkan path folder: ").strip().strip('"')
    
    # ?? PENTING: Ubah dry_run=False HANYA jika sudah yakin ingin menghapus
    delete_https_files(target, dry_run=True)