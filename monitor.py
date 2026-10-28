import json
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "studymonitor/kelompok16/sensor"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Terhubung ke broker MQTT.")
        client.subscribe(TOPIC)
        print("Menunggu data StudyMonitor...")
    else:
        print("Koneksi MQTT gagal:", reason_code)


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))

        print("\n========== STUDYMONITOR ==========")
        print("Kelompok    :", data.get("kelompok"))
        print("Perangkat   :", data.get("perangkat"))
        print("Waktu       :", data.get("waktu"))
        print("Akselerometer:", data.get("akselerometer"))
        print("Giroskop    :", data.get("giroskop"))
        print("Skor gerakan:", data.get("skor_gerakan"))
        print("Status      :", data.get("status"))
        print("==================================")

    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Pesan yang diterima bukan JSON valid.")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="monitor_kelompok16"
)

client.on_connect = on_connect
client.on_message = on_message

print("StudyMonitor - Penerima Data")
print("Menghubungkan ke broker...")

client.connect(BROKER, PORT, 60)
client.loop_forever()