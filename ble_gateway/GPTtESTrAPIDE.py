import paho.mqtt.client as mqtt
import json
import time
import random

BROKER_HOST = "localhost"  # Adresse du broker MQTT
BROKER_PORT = 1883         # Port du broker MQTT
TOPIC_BASE = "iot"         # Base du topic MQTT

CAPTEUR_ADDRESS = "A8:42:E3:90:5E:C2"  # Adresse fictive du capteur
CAPTEUR_NAME = "Cuisine"  # Nom du capteur

CLIENT_ID = "simulated_sensor"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{CAPTEUR_ADDRESS}] Connecté au broker MQTT")
    else:
        print(f"[{CAPTEUR_ADDRESS}] Erreur de connexion: {rc}")

def on_publish(client, userdata, mid):
    print(f"[{CAPTEUR_ADDRESS}] Message publié: {mid}")

# Configuration du client MQTT
client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_start()

try:
    while True:
        # Générer des valeurs aléatoires pour les capteurs
        simulated_data = {
            "water": random.randint(50, 100),
            "gaz": random.randint(0, 10),
            "flame": random.choice([0, 1]),  # 0 = Pas de flamme, 1 = Flamme détectée
            "humidite": random.randint(30, 70),
            "temperature": random.randint(5, 35),
        }

        # Convertir en JSON
        payload = json.dumps(simulated_data)

        print(f"🔹 Données générées : {payload}")

        # Publier chaque valeur sur un topic MQTT distinct
        for key, value in simulated_data.items():
            topic = f"{TOPIC_BASE}/{CAPTEUR_NAME}/{key}"
            client.publish(topic, str(value))
            print(f"📡 Publié sur {topic} → {value}")

        time.sleep(5)  # Attendre 5 secondes avant d'envoyer les prochaines données

except KeyboardInterrupt:
    print("\nSimulation arrêtée.")
    client.loop_stop()
    client.disconnect()
