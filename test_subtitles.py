import requests
import time
import json

# GANTI DENGAN URL RENDER ANDA
BACKEND_URL = "https://viral-test-backend.onrender.com"

with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

results = []
print(f"🔍 Mengujii {len(urls)} URL...")

for i, url in enumerate(urls, 1):
    print(f"\n[{i}/{len(urls)}] {url}")
    try:
        start = time.time()
        resp = requests.post(
            f"{BACKEND_URL}/analyze-subtitle-only",
            json={"url": url},
            timeout=60
        )
        duration = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            results.append(data)
            status = "✅" if data.get("success") else "⚠️"
            has_sub = data.get("subtitle_found", False)
            print(f"{status} {duration:.2f}s | Subtitle: {has_sub}")
        else:
            results.append({"url": url, "error": f"HTTP {resp.status_code}", "duration_seconds": duration})
            print(f"❌ {duration:.2f}s | HTTP {resp.status_code}")
    except Exception as e:
        duration = time.time() - start
        results.append({"url": url, "error": str(e), "duration_seconds": duration})
        print(f"💥 {duration:.2f}s | {str(e)[:80]}")

# Simpan hasil
with open("test_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Ringkasan
success = sum(1 for r in results if r.get("success"))
subs = sum(1 for r in results if r.get("subtitle_found"))
avg = sum(r["duration_seconds"] for r in results) / len(results) if results else 0

print("\n" + "="*50)
print(f"✅ Berhasil: {success}/{len(urls)}")
print(f"📜 Ada subtitle: {subs}/{len(urls)}")
print(f"⏱️ Rata-rata: {avg:.2f} detik")
print("💾 Hasil: test_results.json")