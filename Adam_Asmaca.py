import os
import re
import random


def şifre_kontrol(parola):
    if (len(parola) < 8 or
            not re.search(r"[A-Z]", parola) or
            not re.search(r"[a-z]", parola) or
            not re.search(r"[0-9]", parola) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>+-/]", parola)):
        return False
    return True


def kullanıcı_kayıt():
    while True:
        kullanıcı_adı = input("Kullanıcı adınızı girin: ").strip()
        parola = input("Parolanızı girin: ").strip()

        if os.path.exists("kullanıcılar.txt"):
            with open("kullanıcılar.txt", "r") as dosya:
                for satır in dosya:
                    kayıtlı_ad = satır.split(",")[0].strip()
                    if kullanıcı_adı == kayıtlı_ad:
                        print(
                            "Bu kullanıcı adı zaten mevcut. Lütfen başka bir kullanıcı adı seçin.")
                        continue

        if not şifre_kontrol(parola):
            print("Parola en az 8 karakter uzunluğunda olmalı, en az bir büyük harf, bir küçük harf, bir rakam ve bir özel karakter içermelidir.")
            continue

        with open("kullanıcılar.txt", "a") as dosya:
            dosya.write(f"{kullanıcı_adı},{parola}\n")
        print("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
        break


def kullanıcı_giriş():
    kullanıcı_adı = input("Kullanıcı adınızı girin: ").strip()
    parola = input("Parolanızı girin: ").strip()

    if not os.path.exists("kullanıcılar.txt"):
        print("Kayıtlı kullanıcı bulunamadı. Lütfen önce kayıt olun.")
        return None

    with open("kullanıcılar.txt", "r") as dosya:
        kullanıcılar = dosya.readlines()
        for kullanıcı in kullanıcılar:
            kayıtlı_ad, kayıtlı_parola = kullanıcı.strip().split(",")
            if kullanıcı_adı == kayıtlı_ad and parola == kayıtlı_parola:
                print(f"Giriş başarılı! Hoşgeldiniz, {kullanıcı_adı}")
                return kullanıcı_adı, parola

    print("Kullanıcı adı veya parola yanlış. Tekrar deneyin.")
    return None


def ana_menü():
    while True:
        print("--- Ana Menü ---")
        giriş_türü = input(
            "Adam Asmaca oyununa hoşgeldiniz giriş yapmak mı kayıt olmak mı istiyorsunuz? (giriş/kayıt): ").strip().lower()

        if giriş_türü == "kayıt":
            kullanıcı_kayıt()
        elif giriş_türü == "giriş":
            global kullanıcı_adi, parola
            kullanıcı_adi, parola = kullanıcı_giriş() or (None, None)
            if kullanıcı_adi:
                break
        else:
            print("Geçersiz giriş türü. Lütfen 'giriş' veya 'kayıt' yazın.")


def oyuncu_profili():
    print("----- Oyuncu Profili -----")
    print(f"Kullanıcı Adı: {kullanıcı_adi}")
    print(f"Parola: {parola}")
    print(f"Toplam Puan: {Toplam_Puan}")
    print("--------------------------")


def bilgilendirme():
    print("----- Bilgilendirme -----")
    print("Bu oyun Adam Asmaca oyunudur. Kelimeyi tahmin etmeye çalışın!")
    print("Seçtiğiniz kategori ve zorluk seviyesine göre kazanacağınız puan değişir.")
    print("Kolay kategori: 2-5 harfli kelimeler içerir.")
    print("Orta kategori: 6-9 harfli kelimeler içerir.")
    print("Zor kategori: 10 ve üzeri harfli kelimeler içerir.")
    print("----- Bol şans! -----")


def kategori_seçimi():
    while True:
        kategori = input(
            "Bir kategori seçin (eşyalar, hayvanlar, yiyecekler, isimler, tüm kategoriler): ").strip().lower()
        if kategori in ["eşyalar", "hayvanlar", "yiyecekler", "isimler", "tüm kategoriler"]:
            return kategori
            break
        else:
            print("Geçersiz kategori. Lütfen tekrar deneyin.")
            continue


def zorluk_seçimi():
    while True:
        zorluk = input(
            "Bir zorluk seviyesi seçin (kolay, orta, zor): ").strip().lower()
        if zorluk in ["kolay", "orta", "zor"]:
            return zorluk
            break
        else:
            print("Geçersiz zorluk seviyesi. Lütfen tekrar deneyin.")
            continue


def seçim_ekranı():
    while True:
        seçim = input(
            "Ne yapmak istersiniz? (1: Oyuncu Profili, 2: Bilgilendirme, 3: Oyna, 4: Giriş Ekranına Dön, 5: Çıkış): ").strip()
        if seçim == "1":
            toplam_puan_güncelle()
            oyuncu_profili()
        elif seçim == "2":
            bilgilendirme()
        elif seçim == "3":
            global kategori, zorluk, puan
            kategori = kategori_seçimi()
            zorluk = zorluk_seçimi()
            dosya_oluşturucu()
            puan = puan_hesaplama(kategori, zorluk)
            print(f"Seçilen Kategori: {kategori}, Seçilen Zorluk: {zorluk}")
            oyun()
        elif seçim == "4":
            print("Ana menüye dönülüyor...")
            ana_menü()
        elif seçim == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")
            continue


def puan_hesaplama(kategori, zorluk):
    puan = 0
    if kategori == "tüm kategoriler":
        if zorluk == "kolay":
            puan = 10
        elif zorluk == "orta":
            puan = 20
        elif zorluk == "zor":
            puan = 30
    else:
        if zorluk == "kolay":
            puan = 5
        elif zorluk == "orta":
            puan = 10
        elif zorluk == "zor":
            puan = 15
    return puan


def kazanılan_puan(puan):
    with open("puanlar.txt", "a", encoding='utf-8') as dosya:
        dosya.write(f"{kullanıcı_adi},{puan}\n")


def dosya_oluşturucu():
    dosyalar = ["eşyalar_kolay.txt", "eşyalar_orta.txt", "eşyalar_zor.txt",
                "hayvanlar_kolay.txt", "hayvanlar_orta.txt", "hayvanlar_zor.txt",
                "yiyecekler_kolay.txt", "yiyecekler_orta.txt", "yiyecekler_zor.txt",
                "isimler_kolay.txt", "isimler_orta.txt", "isimler_zor.txt",
                "tüm_kategoriler_kolay.txt", "tüm_kategoriler_orta.txt", "tüm_kategoriler_zor.txt"]
    for dosya in dosyalar:
        if not os.path.exists(dosya):
            with open(dosya, "w", encoding='utf-8') as f:
                f.write("")  # Boş dosya oluştur


def toplam_puan_güncelle():
    global Toplam_Puan
    if os.path.exists("puanlar.txt"):
        with open("puanlar.txt", "r", encoding='utf-8') as dosya:
            Toplam_Puan = sum(int(satır.strip().split(",")[1])
                              for satır in dosya if satır.strip().split(",")[0] == kullanıcı_adi)
    else:
        Toplam_Puan = 0


asılma_aşamaları = [r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', r'''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

tahmin_edilen_harfler = []
tahmin_hakkı = 6


def kelime_listesi_yükle(kategori, zorluk):
    kelimeler = []
    if kategori == "eşyalar" and zorluk == "kolay":
        with open("eşyalar_kolay.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "eşyalar" and zorluk == "orta":
        with open("eşyalar_orta.txt", "r",  encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "eşyalar" and zorluk == "zor":
        with open("eşyalar_zor.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "hayvanlar" and zorluk == "kolay":
        with open("hayvanlar_kolay.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "hayvanlar" and zorluk == "orta":
        with open("hayvanlar_orta.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "hayvanlar" and zorluk == "zor":
        with open("hayvanlar_zor.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "yiyecekler" and zorluk == "kolay":
        with open("yiyecekler_kolay.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "yiyecekler" and zorluk == "orta":
        with open("yiyecekler_orta.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "yiyecekler" and zorluk == "zor":
        with open("yiyecekler_zor.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "isimler" and zorluk == "kolay":
        with open("isimler_kolay.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "isimler" and zorluk == "orta":
        with open("isimler_orta.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "isimler" and zorluk == "zor":
        with open("isimler_zor.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "tüm kategoriler" and zorluk == "kolay":
        with open("tüm_kategoriler_kolay.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "tüm kategoriler" and zorluk == "orta":
        with open("tüm_kategoriler_orta.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    elif kategori == "tüm kategoriler" and zorluk == "zor":
        with open("tüm_kategoriler_zor.txt", "r", encoding='utf-8') as dosya:
            kelimeler = [satır.strip() for satır in dosya.readlines()]
    return kelimeler


def kelime_seç():
    kelimeler = kelime_listesi_yükle(kategori, zorluk)
    if not kelimeler:
        print("Seçilen kategori ve zorluk için kelime bulunamadı. Lütfen başka bir seçim yapın.")
        seçim_ekranı()
        return None
    return random.choice(kelimeler).lower()


def oyun():
    kelime = kelime_seç()
    if not kelime:
        return
    tahmin_edilen_harfler = []
    tahmin_hakkı = 6
    while tahmin_hakkı > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(asılma_aşamaları[tahmin_hakkı])
        display_kelime = ' '.join(
            [harf if harf in tahmin_edilen_harfler else '_' for harf in kelime])
        print(f"Kelime: {display_kelime}")
        print(f"Tahmin Edilen Harfler: {', '.join(tahmin_edilen_harfler)}")
        print(f"Kalan Tahmin Hakkı: {tahmin_hakkı}")

        if all(harf in tahmin_edilen_harfler for harf in kelime):
            print(f"Tebrikler! Kelimeyi doğru bildiniz: {kelime}")
            print(f"Kazandığınız Puan: {puan}")
            kazanılan_puan(puan)
            break

        tahmin = input("Bir harf tahmin edin: ").lower().strip()
        if len(tahmin) != 1 or not tahmin.isalpha():
            print("Lütfen geçerli bir harf girin.")
            continue
        if tahmin in tahmin_edilen_harfler:
            print("Bu harfi zaten tahmin ettiniz. Başka bir harf deneyin.")
            continue

        tahmin_edilen_harfler.append(tahmin)
        if tahmin not in kelime:
            tahmin_hakkı -= 1
            print(f"Yanlış tahmin! '{tahmin}' kelimede yok.")

    if tahmin_hakkı == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(asılma_aşamaları[6])
        print(f"Maalesef, hakkınız bitti. Doğru kelime: {kelime}")


ana_menü()
bilgilendirme()
seçim_ekranı()
