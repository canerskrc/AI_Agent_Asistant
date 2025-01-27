import subprocess
import requests
import time

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def wait_for_service(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(1)
    return False

def test_integration():
    process = subprocess.Popen(["docker-compose", "up", "--build"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert wait_for_service(BACKEND_URL), "Backend service is not running."
        assert wait_for_service(FRONTEND_URL), "Frontend service is not running."

        backend_response = requests.post(
            f"{BACKEND_URL}/query",
            json={"query": "What is the capital of France?", "context": {"sector": "general"}}
        )
        assert backend_response.status_code == 200, "Backend did not return a 200 status code."
        assert "response" in backend_response.json(), "Backend response missing 'response' key."

        frontend_response = requests.get(FRONTEND_URL)
        assert frontend_response.status_code == 200, "Frontend did not return a 200 status code."
        assert "AI Agent Assistant" in frontend_response.text, "Frontend page did not load correctly."

    finally:
        subprocess.call(["docker-compose", "down"])
