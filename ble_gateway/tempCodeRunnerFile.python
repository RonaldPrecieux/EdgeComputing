import asyncio
import random
import base64
import json
import uuid
from bleak import BleakServer, BleakGATTCharacteristic
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Définition du service et de la caractéristique BLE
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-cba987654321"

# Clé AES 256 bits (32 octets)
aes_key = bytes([
    0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
    0x39, 0x30, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46,
    0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E,
    0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56
])

# Génération d'un IV aléatoire
def generate_iv():
    return bytes([random.randint(0, 255) for _ in range(16)])

# Génération d'une adresse MAC aléatoire
def generate_mac():
    return ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)])

# Fonction de chiffrement AES CBC
def encrypt_aes(plain_text):
    iv = generate_iv()
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_data = pad(plain_text.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(iv).decode() + "|" + base64.b64encode(encrypted_data).decode()

# Formater automatiquement les données au format JSON
def format_sensor_data(water_level, flame, gaz, mac_address):
    return json.dumps({
        "waterLevel": water_level,
        "flame": flame,
        "gaz": gaz,
        "mac": mac_address
    })

class ESP32Simulator:
    def __init__(self):
        self.server = None
        self.characteristic = None
        self.mac_address = "A8:42:E3:90:5E:C2"

    async def start_server(self):
        self.server = BleakServer()
        self.characteristic = BleakGATTCharacteristic(
            CHARACTERISTIC_UUID,
            ["read", "notify", "write"],
        )
        self.server.add_service(SERVICE_UUID, [self.characteristic])
        await self.server.start()
        print(f"Serveur BLE prêt... MAC: {self.mac_address}")

        while True:
            water_level = random.randint(0, 100)
            flame_level = random.randint(20, 30)
            gaz_level = random.randint(40, 60)
            
            json_payload = format_sensor_data(water_level, flame_level, gaz_level, self.mac_address)
            encrypted_payload = encrypt_aes(json_payload)
            
            print(f"Données envoyées : {json_payload}")
            await self.characteristic.notify(encrypted_payload.encode())
            
            await asyncio.sleep(5)

async def main():
    esp32 = ESP32Simulator()
    await esp32.start_server()

if __name__ == "__main__":
    asyncio.run(main())
