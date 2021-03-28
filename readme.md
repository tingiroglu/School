# Basit Okul Yönetim Sistemi

Şuan Okulda Super User dan Başka kullanıcı yok müdür ve öğretmenleri ekleyiniz

## Özellikler
- Django'nun kendi admin sayfası kullanılıyor
- Önceden veritabanına tanımlı 3 Okul ve 4 Sınıf var(postgresql server olarak denemelik sürüm)
- Super user olarak daha fazla okul veya sınıf ekleyebilirsiniz
- Her okulun bir tane sınıf öğretmeni var
- Müdür hiyerarşık olarak aynı okuldaki öğretmenleri görebilir, öğrencileri ise ekleyip değiştirip silebilir. Öğretmenler ise sadece kendi öğrencilerini silip düzenleyebilir.
- Super user kullanıcı adı :fatih password: fatih

## Kurulum
İsterseniz sanal python3 kurulumu yapıp sisteme kütüphane yüklememiş olursunuz
```
    python3 -m venv "istediğiniz-ismi-verin"
```
Aktif etmek için
```
    source "tanımladığınız-isim"/bin/activate
```
Kapatmak için

```
    deactivate
```

Gerekli olan kütüphaneler
```
pip3 install Django
pip3 install psycopg2-binary
```




