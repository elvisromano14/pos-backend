import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.almacen_service import get_almacenes

def test():
    try:
        almacenes = get_almacenes("tenant_demo")
        print("Almacenes:", almacenes)
    except Exception as e:
        print("Error fetching almacenes:", e)

if __name__ == "__main__":
    test()
