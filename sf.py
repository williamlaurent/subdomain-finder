import requests

def get_subdomains(domain):
    print(f"[+] Mencari subdomain untuk: {domain}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        unwanted_keywords = {
            "cpanel", "webmail", "cpcalendars", "cpcontacts",
            "www", "mail", "webdisk", "whm", "*."
        }

        subdomains = set()
        for entry in data:
            name_value = entry.get("name_value")
            if name_value:
                for sub in name_value.split("\n"):
                    sub = sub.strip().lower()

                    if any(unwanted in sub for unwanted in unwanted_keywords):
                        continue

                    if sub.endswith(domain):
                        subdomains.add(sub)

        return sorted(subdomains)

    except requests.RequestException as e:
        print(f"[!] Error saat request ke crt.sh: {e}")
        return []

def sanitize_filename(domain):
    return domain.replace(".", "-") + ".txt"

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} domain.com")
        sys.exit(1)

    domain = sys.argv[1]
    results = get_subdomains(domain)

    filename = sanitize_filename(domain)

    if results:
        with open(filename, "w") as f:
            for sub in results:
                f.write(sub + "\n")
        print(f"\n[+] Ditemukan {len(results)} subdomain (sudah difilter)")
        print(f"[+] Hasil disimpan ke: {filename}")
    else:
        print("[!] Tidak ada subdomain ditemukan (atau semua kena filter).")
