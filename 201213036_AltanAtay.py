import sqlite3

conn = sqlite3.connect("banka.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS kullanıcılar (
    tc TEXT PRIMARY KEY,
    parola TEXT NOT NULL,
    bakiye REAL DEFAULT 0.0
)""")

def kullanıcı_ekle(tc, parola):
    if len(tc) != 11:
        print("Hatalı TC kimlik numarası.")
        return

    if len(parola) < 6:
        print("Parola en az 6 karakterli olmalıdır.")
        return

    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ?", (tc,))
    sonuç = cur.fetchone()

    if sonuç:
        print("Bu TC kimlik numarası zaten kayıtlı.")
        return

    cur.execute("INSERT INTO kullanıcılar (tc, parola) VALUES (?, ?)", (tc, parola))
    conn.commit()
    print("Kullanıcı başarıyla eklendi.")


def kullanıcı_girişi(tc, parola):

    if len(tc) != 11:
        print("Hatalı TC kimlik numarası.")
        return

    if len(parola) < 6:
        print("Parola en az 6 karakterli olmalıdır.")
        return

    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ? AND parola = ?", (tc, parola))
    sonuç = cur.fetchone()

    if sonuç:
        print("Giriş başarılı.")
        return True

    else:
        print("Giriş başarısız. Lütfen bilgilerinizi kontrol edin.")
        return False


def bakiye_sorgula(tc):
    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ?", (tc,))
    sonuç = cur.fetchone()

    if sonuç:
        bakiye = sonuç[2]
        print(f"Bakiyeniz: {bakiye} TL")
        return bakiye

    else:
        print("Bu TC kimlik numarasına ait bir hesap bulunamadı.")
        return


def para_yatır(tc, miktar):
    if miktar <= 0:
        print("Lütfen pozitif bir miktar girin.")
        return

    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ?", (tc,))
    sonuç = cur.fetchone()

    if sonuç:
        bakiye = sonuç[2]
        yeni_bakiye = bakiye + miktar

        cur.execute("UPDATE kullanıcılar SET bakiye = ? WHERE tc = ?", (yeni_bakiye, tc))
        conn.commit()
        print(f"{miktar} TL başarıyla yatırıldı. Yeni bakiyeniz: {yeni_bakiye} TL")
        return yeni_bakiye

    else:
        print("Bu TC kimlik numarasına ait bir hesap bulunamadı.")
        return


def para_çek(tc, miktar):
    if miktar <= 0:
        print("Lütfen pozitif bir miktar girin.")
        return

    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ?", (tc,))
    sonuç = cur.fetchone()

    if sonuç:
        bakiye = sonuç[2]

        if bakiye >= miktar:
            yeni_bakiye = bakiye - miktar
            cur.execute("UPDATE kullanıcılar SET bakiye = ? WHERE tc = ?", (yeni_bakiye, tc))
            conn.commit()
            print(f"{miktar} TL başarıyla çekildi. Yeni bakiyeniz: {yeni_bakiye} TL")
            return yeni_bakiye

        else:
            print("Bakiyeniz yetersiz. Lütfen daha küçük bir miktar girin.")
            return

    else:
        print("Bu TC kimlik numarasına ait bir hesap bulunamadı.")
        return


def havale_yap(gönderen_tc, alıcı_tc, miktar):
    if miktar <= 0:
        print("Lütfen pozitif bir miktar girin.")
        return

    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ?", (gönderen_tc,))
    gönderen_sonuç = cur.fetchone()

    cur.execute("SELECT * FROM kullanıcılar WHERE tc = ?", (alıcı_tc,))
    alıcı_sonuç = cur.fetchone()

    if gönderen_sonuç and alıcı_sonuç:
        gönderen_bakiye = gönderen_sonuç[2]
        alıcı_bakiye = alıcı_sonuç[2]

        if gönderen_bakiye >= miktar:
            yeni_gönderen_bakiye = gönderen_bakiye - miktar
            yeni_alıcı_bakiye = alıcı_bakiye + miktar

            cur.execute("UPDATE kullanıcılar SET bakiye = ? WHERE tc = ?", (yeni_gönderen_bakiye, gönderen_tc))
            cur.execute("UPDATE kullanıcılar SET bakiye = ? WHERE tc = ?", (yeni_alıcı_bakiye, alıcı_tc))
            conn.commit()

            print(f"{miktar} TL başarıyla {alıcı_tc} numaralı hesaba havale edildi. Yeni bakiyeniz: {yeni_gönderen_bakiye} TL")
            return yeni_gönderen_bakiye

        else:
            print("Bakiyeniz yetersiz. Lütfen daha küçük bir miktar girin.")
            return

    else:
        print("Havale yapmak istediğiniz hesap/hesaplar bulunamadı. Lütfen bilgilerinizi kontrol edin.")
        return


if __name__ == "__main__":
    while True:
        print("Hoşgeldiniz. Lütfen giriş yapın veya kayıt olun.")
        print("1. Giriş")
        print("2. Kayıt ol")
        print("3. Çıkış")

        seçim = input("Lütfen seçiminizi yapın: ")

        if seçim == "1":
            tc = input("Lütfen TC kimlik numaranızı girin: ")
            parola = input("Lütfen parolanızı girin: ")

            giriş = kullanıcı_girişi(tc, parola)

            if giriş:
                while True:
                    print("Yapmak istediğiniz işlemi seçin.")
                    print("1. Göster")
                    print("2. Nakit Ekle")
                    print("3. Nakit Çek")
                    print("4. Nakit Gönder")
                    print("5. Çıkış")

                    işlem = input("Lütfen seçiminizi yapın: ")

                    if işlem == "1":
                        bakiye_sorgula(tc)

                    elif işlem == "2":
                        miktar = float(input("Lütfen yatırmak istediğiniz miktarı girin: "))
                        para_yatır(tc, miktar)

                    elif işlem == "3":
                        miktar = float(input("Lütfen çekmek istediğiniz miktarı girin: "))
                        para_çek(tc, miktar)

                    elif işlem == "4":
                        alıcı_tc = input("Lütfen havale yapmak istediğiniz hesabın TC kimlik numarasını girin: ")
                        miktar = float(input("Lütfen havale yapmak istediğiniz miktarı girin: "))
                        havale_yap(tc, alıcı_tc, miktar)

                    elif işlem == "5":
                        print("İyi günler dileriz.")
                        break

                    else:
                        print("Lütfen geçerli bir seçim yapın.")

        elif seçim == "2":  
            tc = input("Lütfen TC kimlik numaranızı girin: ")
            parola = input("Lütfen parolanızı girin: ")

            kullanıcı_ekle(tc, parola)

        elif seçim == "3":
            print("İyi günler dileriz.")
            break

        else:
            print("Lütfen geçerli bir seçim yapın.")