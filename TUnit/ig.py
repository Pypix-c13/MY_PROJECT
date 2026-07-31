import sys
import sqlite3
import os

DB_NAME = "database.db"
TXT_NAME = "kosakata.txt"

def init_db():
    """Inisialisasi database SQLite dan impor data dari txt jika database baru dibuat"""
    db_exists = os.path.exists(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Buat tabel kamus jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kamus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jerman TEXT UNIQUE,
            indo TEXT
        )
    """)
    conn.commit()

    # Jika database baru dan file teks ada, lakukan impor otomatis sekali saja
    if not db_exists and os.path.exists(TXT_NAME):
        print("[INFO] Mengimpor kosakata dari file teks ke SQLite...")
        with open(TXT_NAME, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                
                # Pisahkan Jerman dan Indonesia, lalu bersihkan spasi ekstra
                parts = line.split(":", 1)
                jerman = parts[0].strip().lower()
                indo = parts[1].strip().lower()

                try:
                    cursor.execute("INSERT OR IGNORE INTO kamus (jerman, indo) VALUES (?, ?)", (jerman, indo))
                except sqlite3.Error:
                    pass
        conn.commit()
    
    conn.close()

def cari_kata(keyword):
    """Mencari kata (bisa dari Jerman ke Indo atau sebaliknya)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    keyword = keyword.strip().lower()

    # Cari apakah kata yang dimasukkan ada di kolom Jerman atau Indonesia
    cursor.execute("""
        SELECT jerman, indo FROM kamus 
        WHERE jerman LIKE ? OR indo LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    
    hasil = cursor.fetchall()
    conn.close()

    if hasil:
        print(f"\nHasil pencarian untuk '{keyword}':")
        print("-" * 30)
        for row in hasil:
            print(f"🇩🇪 Jerman : {row[0]}")
            print(f"🇮🇩 Indo   : {row[1]}")
            print("-" * 30)
    else:
        print(f"Maaf, kata '{keyword}' tidak ditemukan di kamus offline.")

if __name__ == "__main__":
    # Jalankan inisialisasi database di awal
    init_db()

    # Cek apakah argumen CLI diberikan
    if len(sys.argv) < 2:
        print("Gunakan: python kamus.py <kata>")
        print("Contoh:  python kamus.py schlüssel")
        print("Contoh:  python kamus.py halo")
        sys.exit(1)

    # Ambil kata dari argumen CLI (menggabungkan argumen jika lebih dari 1 kata)
    kata_kunci = " ".join(sys.argv[1:])
    cari_kata(kata_kunci)