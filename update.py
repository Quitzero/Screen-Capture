import requests

url = "http://localhost:8000/UI/main.py"
filename = "main.py"

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))
chunk_size = 1024
progress = 0

with open(filename, 'wb') as file:
    for data in response.iter_content(chunk_size=chunk_size):
        file.write(data)
        progress += len(data)
        percent = (progress / total_size) * 100
        print(f"Downloaded {progress} bytes ({percent:.2f}%)")

print(f"File downloaded successfully: {filename}")
