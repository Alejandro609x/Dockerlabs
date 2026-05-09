import requests

url = "http://172.17.0.2/unprivate/secret/generate.php"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

print(f"{'NUM':<5} {'STATUS':<8} {'SIZE':<10} {'FILENAME'}")
print("-" * 50)

for i in range(1, 101):
    data = {
        "content": "test",
        "number": str(i)
    }

    try:
        r = requests.post(url, headers=headers, data=data, timeout=5)

        size = r.headers.get("Content-Length", "0")
        disposition = r.headers.get("Content-Disposition", "")

        filename = "N/A"

        if "filename=" in disposition:
            filename = disposition.split("filename=")[1].replace('"', '')

        print(f"{i:<5} {r.status_code:<8} {size:<10} {filename}")

    except Exception as e:
        print(f"{i:<5} ERROR -> {e}")
