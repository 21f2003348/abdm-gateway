"""
Quick test script to verify database integration is working
Run this after starting the server to test all functionality
"""
import requests
import json
from datetime import datetime
import uuid

BASE_URL = "http://127.0.0.1:8000"

def get_headers():
    """Get required gateway headers"""
    return {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat(),
        "X-CM-ID": "sbx"
    }

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_root():
    print_section("1. Testing Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health():
    print_section("2. Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_auth():
    print_section("3. Testing Authentication (Database)")
    try:
        # Test with default test client
        response = requests.post(
            f"{BASE_URL}/api/auth/session",
            headers=get_headers(),
            json={
                "clientId": "test_client",
                "clientSecret": "test_secret",
                "grantType": "client_credentials"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return data.get("accessToken")
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_bridge_registration(token):
    print_section("4. Testing Bridge Registration (Database)")
    try:
        headers = get_headers()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(
            f"{BASE_URL}/api/bridge/register",
            headers=headers,
            json={
                "bridgeId": "test-bridge-1",
                "entityType": "HIP",
                "name": "Test Hospital"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_linking(token):
    print_section("5. Testing Link Token Generation (Database)")
    try:
        headers = get_headers()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(
            f"{BASE_URL}/api/link/token/generate",
            headers=headers,
            json={
                "patientId": "pat-12345",
                "hipId": "hip-001"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_consent(token):
    print_section("6. Testing Consent Initiation (Database)")
    try:
        headers = get_headers()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(
            f"{BASE_URL}/api/consent/init",
            headers=headers,
            json={
                "patientId": "pat-12345",
                "hipId": "hip-001",
                "purpose": {
                    "code": "TREATMENT",
                    "text": "Treatment purpose"
                }
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_data_request(token):
    print_section("7. Testing Data Request (Database)")
    try:
        headers = get_headers()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(
            f"{BASE_URL}/api/data/request-info",
            headers=headers,
            json={
                "patientId": "pat-12345",
                "hipId": "hip-001",
                "careContextId": "cc-001",
                "dataTypes": ["DiagnosticReport", "Prescription"]
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def verify_database():
    print_section("8. Verifying Database File")
    import os
    db_file = "abdm_gateway.db"
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        print(f"✓ Database file exists: {db_file}")
        print(f"  Size: {size} bytes")
        return True
    else:
        print(f"✗ Database file not found: {db_file}")
        return False

def main():
    print("\n" + "="*60)
    print("  ABDM GATEWAY - DATABASE INTEGRATION TEST")
    print("="*60)
    
    results = []
    
    # Basic tests
    results.append(("Root Endpoint", test_root()))
    results.append(("Health Check", test_health()))
    
    # Database-dependent tests
    token = test_auth()
    if token:
        results.append(("Authentication", True))
        results.append(("Bridge Registration", test_bridge_registration(token)))
        results.append(("Link Token Generation", test_linking(token)))
        results.append(("Consent Initiation", test_consent(token)))
        results.append(("Data Request", test_data_request(token)))
    else:
        results.append(("Authentication", False))
        print("\n⚠️  Cannot proceed with authenticated tests without valid token")
    
    # Database file check
    results.append(("Database File", verify_database()))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPassed: {passed}/{total} tests")
    print("\nDetailed Results:")
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {name}")
    
    if passed == total:
        print("\n🎉 All tests passed! Database integration is working correctly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()

