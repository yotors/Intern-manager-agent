import requests
import json

class MCPClient:
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url

    def get_capabilities(self):
        response = requests.get(f"{self.server_url}/capabilities")
        return response.json()

    def search_files(self, query: str, max_results: int = 10):
        response = requests.post(
            f"{self.server_url}/tools/search_files",
            json={"query": query, "max_results": max_results}
        )
        return response.json()

    def read_file(self, path: str):
        response = requests.post(
            f"{self.server_url}/tools/read_file",
            json={"path": path}
        )
        return response.json()

def main():
    client = MCPClient()
    print("Server Capabilities:")
    print(json.dumps(client.get_capabilities(), indent=2))

    print("\nSearch Results:")
    print(json.dumps(client.search_files("example"), indent=2))

    print("\nFile Content:")
    print(json.dumps(client.read_file("example.txt"), indent=2))

if __name__ == "__main__":
    main() 