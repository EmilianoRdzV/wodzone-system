"""
WodZone Scanner Client
----------------------
Reads QR codes from a barcode scanner (acts as keyboard wedge),
POSTs to the Django API, and opens the React frontend to show the welcome screen.

Usage: python scanner_client.py
"""
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

API_URL = "http://127.0.0.1:8000/api/checkin/"
FRONTEND_URL = "http://localhost:5173"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def make_driver():
    options = Options()
    options.add_argument("--start-fullscreen")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(options=options)


def main():
    clear()
    print("=========================================")
    print("      WODZONE CHECK-IN SYSTEM v2.0       ")
    print("=========================================")
    print(f"  Backend : {API_URL}")
    print(f"  Frontend: {FRONTEND_URL}")
    print("=========================================")
    print("\nEsperando lectura del escáner QR...\n")

    driver = make_driver()
    driver.get(FRONTEND_URL)

    while True:
        try:
            qr_code = input(">> ESCANEAR: ").strip()

            if not qr_code:
                continue

            print("Procesando...", end="\r")

            try:
                response = requests.post(API_URL, json={"qr_code": qr_code}, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    clear()
                    print("=========================================")
                    print(f"  BIENVENIDO : {data.get('name')}")
                    print(f"  RACHA      : {data.get('streakCurrent')} dias")
                    print(f"  LOGRO      : {data.get('streakName')}")
                    print(f"  VENCE      : {data.get('expiryDate')}")
                    print("=========================================")
                    print("(Esperando siguiente miembro...)\n")

                    # Navigate React frontend to the member welcome page
                    driver.get(f"{FRONTEND_URL}/member/{qr_code}")

                else:
                    error_msg = response.json().get("error", "Error desconocido")
                    print(f"\n  ERROR: {error_msg}\n")

            except requests.exceptions.ConnectionError:
                print("\n  ERROR: No hay conexion con el servidor Django.")
                print("  Asegurate de que 'python manage.py runserver' este activo.\n")
            except requests.exceptions.Timeout:
                print("\n  ERROR: El servidor tardo demasiado en responder.\n")

        except KeyboardInterrupt:
            print("\nSaliendo del sistema...")
            try:
                driver.quit()
            except Exception:
                pass
            break
        except Exception as e:
            print(f"\n  Error inesperado: {e}\n")


if __name__ == "__main__":
    main()
