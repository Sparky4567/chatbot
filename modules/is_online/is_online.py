import requests

class Is_Online:
    def __init__(self):
        self.check_url = "https://www.google.com/"

    def is_online(self):
        try:
            # Try to send a request to a well-known server (e.g., Google's public DNS server)
            response = requests.get(self.check_url, timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False