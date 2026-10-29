import subprocess
import json
import time
import math
import socket
import paho.mqtt.client as mqtt

# Identitas perangkat
DEVICE_ID = "HP1"
GROUP_ID = "kelompok16"

# Konfigurasi MQTT
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "studymonitor/kelompok16/sensor"

# Nama sensor sesuai hasil pengujian Termux
ACCELEROMETER = "sc7a20h_acc"
GYROSCOPE = "virtual_gyro"

INTERVAL = 3


def baca_sensor(nama_sensor):
    try:
        hasil = subprocess.run(
            [
                "termux-sensor",
                "-s", nama_sensor,
                "-n", "1"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if hasil.returncode != 0:
            print("Gagal membaca:", nama_sensor)
            return None

        data = json.loads(hasil.stdout)
        return data[nama_sensor]["values"]

    except (
        subprocess.TimeoutExpired,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        FileNotFoundError
    ) as error:
        print("Kesalahan sensor:", error)
        return None


def hitung_magnitudo(nilai):
    return math.sqrt(sum(x * x for x in nilai))


def klasifikasi_gerakan(akselerometer, giroskop):
    # Besar percepatan total
    magnitudo_acc = hitung_magnitudo(akselerometer)

    # Besar rotasi
    magnitudo_gyro = hitung_magnitudo(giroskop)

    # Percepatan sensor mencakup gravitasi.
    # Selisih dari 9,81 digunakan sebagai perkiraan
    # perubahan percepatan, bukan pengukuran sempurna.
    perubahan_acc = abs(magnitudo_acc - 9.81)

    # Algoritma berbasis aturan sederhana
    skor = perubahan_acc + magnitudo_gyro

    if skor < 1.5:
        status = "TENANG"
    elif (skor >= 1 and skor < 4):
        status = "SEDANG"
    else:
        status = "TINGGI"

    return status, magnitudo_acc, magnitudo_gyro, skor


def main():
    print("StudyMonitor - Kelompok 16")
    print("Perangkat:", DEVICE_ID)
    print("Menghubungkan ke MQTT...")

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="sm16_" + DEVICE_ID + "_" + socket.gethostname()
    )

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        print("Berhasil terhubung ke broker MQTT.")

    except Exception as error:
        print("Gagal menghubungkan MQTT:", error)
        return

    try:
        while True:
            acc = baca_sensor(ACCELEROMETER)
            gyro = baca_sensor(GYROSCOPE)

            if acc is None or gyro is None:
                print("Data belum lengkap. Mencoba lagi...")
                time.sleep(INTERVAL)
                continue

            status, magnitudo_acc, magnitudo_gyro, skor = (
                klasifikasi_gerakan(acc, gyro)
            )

            payload = {
                "kelompok": GROUP_ID,
                "perangkat": DEVICE_ID,
                "waktu": time.strftime("%Y-%m-%d %H:%M:%S"),
                "akselerometer": acc,
                "giroskop": gyro,
                "magnitudo_acc": round(magnitudo_acc, 3),
                "magnitudo_gyro": round(magnitudo_gyro, 3),
                "skor_gerakan": round(skor, 3),
                "status": status
            }

            pesan = json.dumps(payload)

            hasil = client.publish(
                TOPIC,
                pesan,
                qos=0
            )

            if hasil.rc == mqtt.MQTT_ERR_SUCCESS:
                print("\nData terkirim:")
                print(json.dumps(payload, indent=2))
            else:
                print("Pengiriman data gagal.")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nStudyMonitor dihentikan.")

    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
