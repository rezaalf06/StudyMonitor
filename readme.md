# StudyMonitor

StudyMonitor adalah proyek Internet of Things (IoT) untuk memantau pergerakan smartphone selama sesi belajar menggunakan sensor akselerometer dan giroskop. Data sensor diolah menggunakan algoritma sederhana, kemudian dikirim melalui protokol MQTT untuk dipantau melalui laptop.

## Teknologi yang Digunakan

- **Python:** pemrograman dan pengolahan data.
- **Termux:** menjalankan program pada smartphone Android.
- **Akselerometer dan giroskop:** membaca pergerakan perangkat.
- **MQTT:** komunikasi data antara perangkat dan laptop.
- **Broker MQTT:** perantara pengiriman pesan.

## Cara Kerja

1. Smartphone membaca data dari sensor akselerometer dan giroskop.
2. Data sensor diolah menggunakan algoritma klasifikasi berbasis aturan.
3. Pergerakan perangkat dikelompokkan menjadi TENANG, SEDANG, atau TINGGI berdasarkan aturan program.
4. Data dikirim melalui MQTT.
5. Laptop menerima dan menampilkan data yang dikirimkan.

*Catatan: Klasifikasi menunjukkan tingkat pergerakan smartphone, bukan tingkat konsentrasi pengguna secara langsung.*

## Cara Menjalankan

### 1. Program pada Smartphone

Buka Termux, masuk ke direktori proyek, kemudian jalankan:

```bash
python studimonitor.py
```

### 2. Program pada Laptop

Buka terminal VS Code, aktifkan virtual environment jika diperlukan, kemudian jalankan:

```powershell
python monitor.py
```

Pastikan konfigurasi broker MQTT dan topik yang digunakan pada kedua program sudah sesuai.

### 3. Menghentikan Program

Tekan `Ctrl + C` pada terminal tempat program berjalan.

## Pengujian

Pengujian dilakukan dengan memeriksa pembacaan sensor, pengolahan data, klasifikasi pergerakan, serta pengiriman dan penerimaan pesan MQTT. Hasil pengujian dicatat berdasarkan hasil pelaksanaan program.

## Anggota Kelompok

1. [Nama Anggota 1] — [NIM]
2. [Nama Anggota 2] — [NIM]
3. [Nama Anggota 3] — [NIM]