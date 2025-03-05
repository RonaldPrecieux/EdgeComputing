# MQTT_BROKER = "broker.hivemq.com"
# MQTT_PORT = 1883
# MQTT_TOPIC = "iot/ble_gateway"
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC_BASE = "iot"  # Base du topic MQTT

#BLE_DEVICE_ADDRESS = ["A8:42:E3:90:5E:C2", "08:A6:F7:B1:7C:AE"]

CHARACTERISTIC_UUID = "87654321-4321-4321-4321-cba987654321"

# Associer un nom à chaque capteur
CAPTEURS = {
    #"A8:42:E3:90:5E:C2": "Cuisine/Sensor",
    "A0:B7:65:25:4B:22": "Cuisine/Sensor"
}

BLE_DEVICE_ADDRESS = ["A0:B7:65:25:4B:22"] # Adresse MAC de l'appareil BLE
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-cba987654321"  # UUID des données à lire
AES_KEY = bytes([
    0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
    0x39, 0x30, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46,
    0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E,
    0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56
])

# BROKER_HOST = "addf453f21b541ac82d204ed1239f31b.s1.eu.hivemq.cloud" 
# BROKER_PORT = 8883
# TOPIC = "iot/ble_gateway"
# USERNAME = "Rx1234"  # Si nécessaire
# PASSWORD = "Rx1234@1"  