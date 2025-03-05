from bleak import BleakScanner, BleakClient
import asyncio
import base64
import json
from Crypto.Cipher import AES
from cloud_client import publish_data_on_mqtt
from config import CHARACTERISTIC_UUID, AES_KEY, CAPTEURS

async def scan_devices():
    devices = await BleakScanner.discover()
    print("Devices found:")
    for device in devices:
        print(f"Name: {device.name}, Address: {device.address}")
    return [device.address for device in devices if device.name is not None]

async def scan_devices():
    devices = await BleakScanner.discover()
    print("Devices found:")
    for device in devices:
        print(f"Name: {device.name}, Address: {device.address}")
    return [device.address for device in devices if device.name is not None]

def decryptAES(encrypted_data):
    try:
        if "|" not in encrypted_data.decode():
            raise ValueError("Format invalide")

        iv_b64, cipher_b64 = encrypted_data.decode().split("|")
        iv = base64.b64decode(iv_b64)
        cipher_text = base64.b64decode(cipher_b64)

        if len(AES_KEY) not in [16, 24, 32]:
            raise ValueError("Longueur de clé invalide")

        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(cipher_text)

        pad_len = decrypted_data[-1]
        decrypted_data = decrypted_data[:-pad_len]

        return json.loads(decrypted_data.decode())
    except Exception as e:
        print(f"Erreur de déchiffrement: {e}")
        return None

async def notification_handler(sender, data, address, log_queue):
    decrypted_data = decryptAES(data)
    if decrypted_data:
        log_queue.put(f"[{CAPTEURS.get(address, 'Unknown')}] {decrypted_data}")
        await publish_data_on_mqtt(address, decrypted_data)
    else:
        log_queue.put(f"[{address}] Erreur de déchiffrement")

async def handle_device(address, log_queue):
    async with BleakClient(address) as client:
        print('Connected')

        if client.is_connected:
            log_queue.put(f"[{address}] Connecté")
            try:
                await client.start_notify(CHARACTERISTIC_UUID, lambda s, d: asyncio.create_task(notification_handler(s, d, address, log_queue)))
                while client.is_connected:
                    await asyncio.sleep(1)
                await client.stop_notify(CHARACTERISTIC_UUID)
                log_queue.put(f"[{address}] Déconnecté")
            except Exception as e:
                log_queue.put(f"[{address}] Erreur: {e}")
        else:
            log_queue.put(f"[{address}] Échec de connexion")
