import http.server
import socketserver
import webbrowser
from pathlib import Path
import os

PORT = 8000
TITLE = "Map Viewer"

base_dir = Path(__file__).resolve().parent

output_dir = base_dir.parent / "Output/GA - Gusti"

if not output_dir.exists():
    raise FileNotFoundError(f"directory not found (/Output): {output_dir}")

vehicle_files = sorted(output_dir.glob("map_vehicle_*_ga.html"))
all_file = output_dir / "map_all_vehicles_ga.html"

html_files = []

if all_file.exists():
    html_files.append(all_file)

html_files.extend(vehicle_files)

if not html_files:
    raise FileNotFoundError(
        "html file not found"
    )

links = []
for f in html_files:
    if f.name == "map_all_vehicles_ga.html":
        display_name = "Map All Vehicles"
    else:
        display_name = f.stem.replace("_", " ").title()
    links.append(f'<li><a href="{f.name}" target="_blank">{display_name}</a></li>')

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{TITLE}</title>
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #eef2ff, #f8fafc);
        }}

        .container {{
            max-width: 720px;
            margin: 60px auto;
            background: white;
            padding: 32px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }}

        h1 {{
            margin: 0 0 8px;
            font-size: 28px;
        }}

        .subtitle {{
            color: #6b7280;
            margin-bottom: 24px;
        }}

        ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        li {{
            margin-bottom: 12px;
        }}

        a {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            text-decoration: none;
            padding: 14px 16px;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
            background: #fafafa;
            color: #111827;
            font-size: 16px;
            transition: all 0.2s ease;
        }}

        a:hover {{
            background: #eef5ff;
            border-color: #3b82f6;
            transform: translateY(-1px);
        }}

        .badge {{
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 6px;
            background: #e0f2fe;
            color: #0369a1;
        }}

        .all {{
            background: #eff6ff;
            border-color: #3b82f6;
        }}

        .all .badge {{
            background: #3b82f6;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🗺️ {TITLE}</h1>
        <p class="subtitle">Select a map to view the route visualization</p>

        <ul>
            {''.join(links)}
        </ul>
    </div>
</body>
</html>
"""

(output_dir / "index.html").write_text(index_html, encoding="utf-8")

os.chdir(output_dir)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    url = f"http://127.0.0.1:{PORT}/index.html"
    print(f"{TITLE} is running at: {url}")
    print(f"Serving folder: {output_dir}")
    print("Press Ctrl+C to stop the server.")
    webbrowser.open(url)
    httpd.serve_forever()