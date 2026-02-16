import requests
import os
import time

# En producción (Gym), esto seguirá siendo localhost si corren en la misma máquina.
API_URL = "http://127.0.0.1:8000/api/checkin/"

def limpiar_pantalla():
    # Comando 'cls' para Windows, 'clear' para Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    limpiar_pantalla()
    print("=========================================")
    print("   WODZONE CHECK-IN SYSTEM (ACTIVO)   ")
    print("=========================================")
    print("\nEsperando lectura del escáner...")

    while True:
        try:
            # El escáner actúa como teclado y da ENTER al final
            qr_code = input("\n>> ESCANEAR AHORA: ")

            # Si se presiona Enter sin escribir nada, ignorar
            if not qr_code:
                continue

            print("Procesando...", end="\r")

            # Enviamos el código al backend
            try:
                response = requests.post(API_URL, json={'qr_code': qr_code})
                
                if response.status_code == 200:
                    data = response.json()
                    limpiar_pantalla()
                    print("=========================================")
                    print(f"✅ BIENVENIDO: {data.get('name')}")
                    print(f"🔥 RACHA ACTUAL: {data.get('streakCurrent')} DÍAS")
                    print(f"🔥 NOMBRE RACHA ACTUAL: {data.get('streakName')}")
                    print(f"🔥 NOMBRE RACHA ACTUAL: {data.get('expireDate')}")
                    print("=========================================")
                    print("\n(Esperando siguiente miembro...)")
                    
                    # Sonido de éxito (solo Windows)
                    # print('\a') 
                else:
                    error_msg = response.json().get('error', 'Error desconocido')
                    print(f"\n❌ ERROR: {error_msg}")
            
            except requests.exceptions.ConnectionError:
                print("\n⚠️ ERROR CRÍTICO: No se puede conectar al servidor.")
                print("   Asegúrate de que la ventana negra de 'runserver' esté abierta.")

        except KeyboardInterrupt:
            print("\nSaliendo del sistema...")
            break
        except Exception as e:
            print(f"\n⚠️ Error inesperado: {e}")

if __name__ == "__main__":
    main()