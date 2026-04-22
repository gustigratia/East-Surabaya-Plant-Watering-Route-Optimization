import http.server
import socketserver
import webbrowser
from pathlib import Path
import os

PORT = 8000
TITLE = "Map Viewer"

base_dir = Path(__file__).resolve().parent.parent

# Ambil semua file vehicle
vehicle_files = sorted(base_dir.glob("map_vehicle_*.html"))

# Ambil file gabungan kalau ada
all_vehicles_file = base_dir / "map_all_vehicles.html"

html_files = []

if all_vehicles_file.exists():
    html_files.append(all_vehicles_file)

html_files.extend(vehicle_files)

if not html_files:
    raise FileNotFoundError(
        "Tidak ditemukan file map_vehicle_*.html atau map_all_vehicles.html"
    )

# Buat menu index
links = []
for f in html_files:
    display_name = f.name.replace(".html", "").replace("_", " ").title()
    links.append(f'<li><a href="{f.name}" target="_blank">{display_name}</a></li>')

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{TITLE}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 24px;
            background: #f7f7f7;
        }}
        .container {{
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}
        h1 {{
            margin-top: 0;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
        }}
        a {{
            display: block;
            text-decoration: none;
            color: #0d6efd;
            font-size: 18px;
            padding: 10px 14px;
            border: 1px solid #dcdcdc;
            border-radius: 8px;
            background: #fafafa;
        }}
        a:hover {{
            background: #eef5ff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🗺️ {TITLE}</h1>
        <p>Pilih map yang ingin dilihat:</p>
        <ul>
            {''.join(links)}
        </ul>
    </div>
</body>
</html>
"""

(base_dir / "index.html").write_text(index_html, encoding="utf-8")

os.chdir(base_dir)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    url = f"http://127.0.0.1:{PORT}/index.html"
    print(f"{TITLE} berjalan di: {url}")
    print("Tekan Ctrl+C untuk menghentikan server.")
    webbrowser.open(url)
    httpd.serve_forever()