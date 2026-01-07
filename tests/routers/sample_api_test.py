import requests

BaseUrl = "http://localhost:8000"

def test_get_sample():
    response = requests.get(f"{BaseUrl}/api/v1/sample")
    print("status code: ", response.status_code)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def main():
    test_get_sample()

if __name__ == "__main__":
    main()
