import paho.mqtt.client as mqtt
from config import BROKER_HOST, BROKER_PORT, TOPIC_BASE, CAPTEURS
import asyncio
import json

CLIENT_ID = "ble_device_publisher"

async def publish_data_on_mqtt(address, data):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[{address}] Connecté au broker MQTT")
        else:
            print(f"[{address}] Erreur de connexion: {rc}")

    def on_publish(client, userdata, mid):
        print(f"[{address}] Message publié: {mid}")

    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    try:
        capteur_base = CAPTEURS.get(address, "Unknown")
        data_dict = json.loads(data)  # Convertir la donnée en dictionnaire

        for key, value in data_dict.items():
            topic = f"{TOPIC_BASE}/{capteur_base}/{key}"
            payload = str(value)
            result = client.publish(topic, payload)
            await asyncio.to_thread(result.wait_for_publish)

    except json.JSONDecodeError:
        print(f"[{address}] Erreur: Données reçues non valides")
    except Exception as e:
        print(f"[{address}] Erreur MQTT: {e}")

    client.loop_stop()
