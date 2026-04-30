import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.auth_service import authenticate_user
from app.core.security import create_access_token, decode_access_token

def test():
    auth_result = authenticate_user("admin", "admin123", "tenant_demo")
    if not auth_result:
        print("Login failed")
        return
        
    print("Login OK")
    token = create_access_token(
        subject=auth_result["username"],
        tenant_id=auth_result["tenant_id"],
        tenant_schema=auth_result["tenant_schema"],
        roles=auth_result["roles"],
    )
    print("Token:", token)
    
    try:
        payload = decode_access_token(token)
        print("Decoded OK:", payload)
    except Exception as e:
        print("Decode Error:", e)

if __name__ == "__main__":
    test()
