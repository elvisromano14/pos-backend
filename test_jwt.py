import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.security import create_access_token, decode_access_token

def test():
    try:
        token = create_access_token(
            subject="admin",
            tenant_id=1,
            tenant_schema="tenant_demo",
            roles=["Administrador"]
        )
        print("Token generated:", token)
        
        payload = decode_access_token(token)
        print("Payload decoded:", payload)
        
        required_claims = {"sub", "tenant_id", "tenant_schema", "roles"}
        if not required_claims.issubset(payload.keys()):
            print("Missing claims:", required_claims - set(payload.keys()))
        else:
            print("Claims OK!")
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
