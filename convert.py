import os
import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

try:
    from markdownify import markdownify as md
except ImportError:
    print("? Library belum lengkap. Jalankan: pip install markdownify beautifulsoup4")
    exit(1)

def clean_html(html_content):
    """Membersihkan HTML dari tag & atribut CSS/JS sebelum konversi"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Hapus seluruh tag CSS/JS & elemen head/metadata
    for tag in soup(['script', 'style', 'link', 'meta', 'noscript', 'iframe', 'head', 'nav', 'footer']):
        tag.decompose()

    # 2. Hapus atribut inline yang membawa CSS/JS
    for tag in soup.find_all(True):  # True = semua tag
        tag.attrs = {
            k: v for k, v in tag.attrs.items()
            if k not in ('style', 'class', 'id') and not k.startswith('on')
        }

    return str(soup)

def clean_markdown_output(md_text):
    """Rapihkan hasil Markdown (hapus baris kosong berlebihan)"""
    md_text = re.sub(r'\n{3,}', '\n\n', md_text)
    return md_text.strip() + '\n'

def process_html_to_markdown(root_dir):
    root_path = Path(root_dir).resolve()
    if not root_path.is_dir():
        print(f"? '{root_dir}' bukan direktori yang valid.")
        return

    html_files = list(root_path.rglob('index-https.html'))
    if not html_files:
        print("? Tidak ditemukan file 'index-https.html'.")
        return

    # Urutkan dari TERDALAM ke TERLUAR (mencegah konflik folder vs file)
    html_files.sort(key=lambda x: len(x.parts), reverse=True)
    print(f"?? Ditemukan {len(html_files)} file. Memproses dari struktur terdalam...\n")

    for html_file in html_files:
        parent_dir = html_file.parent
        dir_name = parent_dir.name
        target_md = parent_dir.parent / dir_name if dir_name.endswith('.md') else parent_dir / 'index.md'
        
        print(f"?? Proses: {html_file.relative_to(root_path)}")

        try:
            # 1. Baca & Bersihkan HTML dari CSS/JS
            html_content = html_file.read_text(encoding='utf-8')
            cleaned_html = clean_html(html_content)

            # 2. Konversi ke Markdown
            md_content = md(cleaned_html, heading_style="ATX", bullets="-", strip=['script', 'style', 'link', 'meta', 'noscript', 'iframe'])
            md_content = clean_markdown_output(md_content)

            # 3. Hapus file HTML asli
            html_file.unlink()
            print("   ??? File HTML dihapus")

            # 4. Tangani konflik folder *.md yang masih berisi data lain
            if dir_name.endswith('.md') and parent_dir.exists():
                if any(parent_dir.iterdir()):
                    backup_name = f"{dir_name}_isifolder"
                    backup_path = parent_dir.parent / backup_name
                    print(f"   ?? '{dir_name}' berisi data lain. Dipindah ke '{backup_name}'")
                    shutil.move(str(parent_dir), str(backup_path))
                else:
                    parent_dir.rmdir()
                    print(f"   ?? Folder '{dir_name}' dihapus (kosong)")

            # 5. Simpan Markdown
            target_md.write_text(md_content, encoding='utf-8')
            print(f"   ? Markdown tersimpan: {target_md.relative_to(root_path)}")

        except Exception as e:
            print(f"   ? Gagal: {e}")

    print("\n?? Konversi selesai! Periksa folder `*_isifolder` jika ada.")

if __name__ == "__main__":
    TARGET_FOLDER = "./"  # ? GANTI dengan path folder Anda
    process_html_to_markdown(TARGET_FOLDER)