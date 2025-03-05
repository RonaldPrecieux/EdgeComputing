import asyncio
import threading
from queue import Queue
from ble_manager import scan_devices, handle_device
from cloud_client import publish_data_on_mqtt
from config import BLE_DEVICE_ADDRESS

# Fonction pour traiter et afficher les logs de log_queue
def log_worker(log_queue):
    while True:
        log = log_queue.get()
        if log is None:  # Permet d'arrêter proprement le thread si nécessaire
            break
        print(log)

# Fonction pour gérer un périphérique BLE dans un thread
def handle_device_thread(address, log_queue, error_queue):
    try:
        print(f"Thread démarré pour {address}")
        asyncio.run(handle_device(address, log_queue))
        print(f"Thread terminé pour {address}")
    except Exception as e:
        error_queue.put((address, str(e)))

# Fonction principale
async def main():
    log_queue = Queue()
    error_queue = Queue()
    #devices = await scan_devices()
    
    # Lancer un thread pour afficher les logs en continu
    log_thread = threading.Thread(target=log_worker, args=(log_queue,), daemon=True)
    log_thread.start()

    threads = []
    for address in BLE_DEVICE_ADDRESS:
        thread = threading.Thread(target=handle_device_thread, args=(address, log_queue, error_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Vérifier s'il y a des erreurs dans la queue et les traiter
    while not error_queue.empty():
        address, error_message = error_queue.get()
        print(f"Erreur avec le périphérique {address}: {error_message}")

    # Arrêter proprement le thread de logs
    log_queue.put(None)
    log_thread.join()

if __name__ == "__main__":
    asyncio.run(main())
