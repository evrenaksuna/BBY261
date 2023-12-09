import sqlite3

def main():
    conn = sqlite3.connect("kutuphane.db")

    # menü
    while True:
        print("** Kitaplık Uygulaması **")
        print("1. Kitapları listele")
        print("2. Yeni kitap ekle")
        print("3. Kitaplarda arama yap")
        print("4. Kitap sil")
        print("5. Kitap güncelle")
        print("6. Çıkış")
        secim = input("Seçiminiz: ")
        if secim == "1":
            listele()
        elif secim == "2":
            ekle()
        elif secim == "3":
            arama()
        elif secim == "4":
            sil()
        elif secim == "5":
            guncelle()
        elif secim == "6":
            break

def listele():
    # tablodan veri çek
    cur = conn.cursor()
    cur.execute("SELECT * FROM kutuphane")
    kutuphane = cur.fetchall()

    # veri listeleme
    for eser in kutuphane:
        print(eser)

def ekle():
    # Eser bilgilerini kullanıcıdan al.
    eser_adi = input("Eser adı: ")
    eser_yazari = input("Eser yazarı: ")
    eser_yayinevi = input("Eser yayınevi: ")
    eser_konu_basligi = input("Eser konu başlığı: ")

    # veri ekleme
    cur = conn.cursor()
    cur.execute("INSERT INTO kutuphane (eser_adi, eser_yazari, eser_yayinevi, eser_konu_basligi) VALUES (?, ?, ?, ?)", (eser_adi, eser_yazari, eser_yayinevi, eser_konu_basligi))
    conn.commit()
    print("Eser başarıyla eklendi.")

def arama():
    anahtar_kelime = input("Arama anahtar kelimesi: ")

    cur = conn.cursor()
    cur.execute("SELECT * FROM kutuphane WHERE eser_adi LIKE ? OR eser_yazari LIKE ? OR eser_konu_basligi LIKE ?", (f"%{anahtar_kelime}%", f"%{anahtar_kelime}%", f"%{anahtar_kelime}%"))
    kutuphane = cur.fetchall()

    for eser in kutuphane:
        print(eser)

def sil():
    silme_anahtar_kelime = input("Silmek istediğiniz eserin adını girin: ")

    cur = conn.cursor()
    cur.execute("SELECT * FROM kutuphane WHERE eser_adi = ?", (silme_anahtar_kelime,))
    kutuphane = cur.fetchall()

    # eser var mı kontrol et
    if len(kutuphane) == 0:
        print("Böyle bir kitap yok.")
        return

    # eseri sil.
    cur.execute("DELETE FROM kutuphane WHERE eser_adi = ?", (silme_anahtar_kelime,))
    conn.commit()
    print("Eser başarıyla silindi.")

def guncelle():
    eser_adi = input("Güncellemek istediğiniz eserin adını girin: ")

    cur = conn.cursor()
    cur.execute("SELECT * FROM kutuphane WHERE eser_adi = ?", (eser_adi,))
    kutuphane = cur.fetchall()

    if len(kutuphane) == 0:
        print
