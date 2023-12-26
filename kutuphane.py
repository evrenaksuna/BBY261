import sqlite3
from tkinter import Tk, Label, Button, Text, Scrollbar, END, Entry

class KutuphaneUygulamasi:
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Kütüphane Uygulaması")

        # Etiketler
        self.etiket = Label(ana_pencere, text="Yapmak İstediğiniz İşlemi Seçin:")
        self.etiket.grid(row=0, column=0, columnspan=2, pady=10)

        # Butonlar
        self.ara_button = Button(ana_pencere, text="Eser Ara", command=self.eser_ara_pencere)
        self.ara_button.grid(row=1, column=0, pady=5, padx=10)

        self.listele_button = Button(ana_pencere, text="Eser Listele", command=self.eser_listele)
        self.listele_button.grid(row=1, column=1, pady=5, padx=10)

        self.ekle_button = Button(ana_pencere, text="Yeni Eser Ekle", command=self.yeni_eser_ekle_pencere)
        self.ekle_button.grid(row=2, column=0, pady=5, padx=10)

        self.sil_button = Button(ana_pencere, text="Eser Sil", command=self.eser_sil_pencere)
        self.sil_button.grid(row=2, column=1, pady=5, padx=10)

        # Metin Kutusu ve Kaydırma Çubuğu
        self.metin_kutusu = Text(ana_pencere, height=10, width=50)
        self.metin_kutusu.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

        self.kaydirma_cubugu = Scrollbar(ana_pencere, command=self.metin_kutusu.yview)
        self.kaydirma_cubugu.grid(row=3, column=2, sticky="nsew")

        self.metin_kutusu.config(yscrollcommand=self.kaydirma_cubugu.set)

    def eser_ara_pencere(self):
        pencere = Tk()
        pencere.title("Eser Ara")

        etiket = Label(pencere, text="Aranacak Bilgiyi Girin:")
        etiket.grid(row=0, column=0, padx=10, pady=5)

        arama_entry = Entry(pencere)
        arama_entry.grid(row=0, column=1, padx=10, pady=5)

        ara_button = Button(pencere, text="Ara", command=lambda: self.eser_ara(arama_entry.get()))
        ara_button.grid(row=1, column=0, columnspan=2, pady=10)

    def eser_ara(self, arama_kelimesi):
        self.ekran_yazisi("Aranan Eser:")
        self.metin_kutusu.delete(1.0, END)
        conn = sqlite3.connect("kutuphane.db")
        cursor = conn.cursor()
        arama_kelimesi_kucuk = arama_kelimesi.lower()
        # Tüm alanlarda arama yapmak için LIKE ve % işaretini kullanıyoruz
        cursor.execute("SELECT * FROM kutuphane WHERE LOWER(eser) LIKE ? OR LOWER(yazar) LIKE ? OR LOWER(yayinevi) LIKE ? OR LOWER(konubasligi) LIKE ?",
                       (f"%{arama_kelimesi_kucuk}%", f"%{arama_kelimesi_kucuk}%", f"%{arama_kelimesi_kucuk}%", f"%{arama_kelimesi_kucuk}%"))
        eserler = cursor.fetchall()
        conn.close()
        if eserler:
            for eser in eserler:
                self.metin_kutusu.insert(END, f"Eser Adı: {eser[0]}\nYazar: {eser[1]}\nYayınevi: {eser[2]}\nKonu Başlığı: {eser[3]}\n\n")
        else:
            self.metin_kutusu.insert(END, "Eser bulunamadı.\n")

    def yeni_eser_ekle_pencere(self):
        pencere = Tk()
        pencere.title("Yeni Eser Ekle")

        etiketler = ["Yeni Eser Adı:", "Yazar Adı:", "Yayınevi:", "Konu Başlığı:"]
        entry_değerleri = []

        for i, etiket in enumerate(etiketler):
            Label(pencere, text=etiket).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(pencere)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry_değerleri.append(entry)

        ekle_button = Button(pencere, text="Ekle", command=lambda: self.yeni_eser_ekle(entry_değerleri))
        ekle_button.grid(row=len(etiketler), column=0, columnspan=2, pady=10)

    def yeni_eser_ekle(self, entry_değerleri):
        degerler = [entry.get() for entry in entry_değerleri]
        if all(degerler):
            conn = sqlite3.connect("kutuphane.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kutuphane VALUES (?, ?, ?, ?)", tuple(degerler))
            conn.commit()
            conn.close()
            self.ekran_yazisi(f"{degerler[0]} adlı eser başarıyla eklendi.")
        else:
            self.ekran_yazisi("Lütfen tüm alanları doldurun.")

    def eser_sil_pencere(self):
        pencere = Tk()
        pencere.title("Eser Sil")

        etiket = Label(pencere, text="Silinecek Eser Adını Girin:")
        etiket.grid(row=0, column=0, padx=10, pady=5)

        eser_adı_entry = Entry(pencere)
        eser_adı_entry.grid(row=0, column=1, padx=10, pady=5)

        sil_button = Button(pencere, text="Sil", command=lambda: self.eser_sil(eser_adı_entry.get()))
        sil_button.grid(row=1, column=0, columnspan=2, pady=10)

    def eser_sil(self, eser_adı):
        if eser_adı:
            conn = sqlite3.connect("kutuphane.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kutuphane WHERE eser=?", (eser_adı,))
            conn.commit()
            conn.close()
            self.ekran_yazisi(f"{eser_adı} adlı eser başarıyla silindi.")
        else:
            self.ekran_yazisi("Lütfen bir eser adı girin.")

    def eser_listele(self):
        self.ekran_yazisi("Kütüphane Verileri:")
        veriler = self.tum_verileri_getir()
        self.metin_kutusu.delete(1.0, END)
        for eser in veriler:
            self.metin_kutusu.insert(END, f"Eser Adı: {eser[0]}\nYazar: {eser[1]}\nYayınevi: {eser[2]}\nKonu Başlığı: {eser[3]}\n\n")

    def tum_verileri_getir(self):
        conn = sqlite3.connect("kutuphane.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kutuphane")
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    def ekran_yazisi(self, mesaj):
        self.metin_kutusu.delete(1.0, END)
        self.metin_kutusu.insert(END, mesaj)

if __name__ == "__main__":
    root = Tk()
    uygulama = KutuphaneUygulamasi(root)
    root.mainloop()
