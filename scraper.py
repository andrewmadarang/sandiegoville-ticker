import urllib.request
import xml.etree.ElementTree as ET
import html

def fetch_sandiegoville():
    # SanDiegoVille's official Atom feed URL
    url = "https://sandiegoville.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        # Atom namespaces mapping
        ns = {'atom': 'http://w3.org'}
        
        titles = []
        # Get the 20 most recent posts
        for entry in root.findall('atom:entry', ns)[:10]:
            title_element = entry.find('atom:title', ns)
            if title_element is not None and title_element.text:
                clean_title = html.escape(title_element.text.strip())
                titles.append(f"🔱 {clean_title} 🔱")
                
        if not titles:
            return "🌮 No recent SanDiegoVille stories found. Check back soon! 🌮"
            
        return " ... ".join(titles)
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "⚠️ Temporary error loading SanDiegoVille news... ⚠️"

def generate_html():
    ticker_text = fetch_sandiegoville()
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SanDiegoVille Live Ticker</title>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; background: transparent; font-family: 'Montserrat', 'Arial', sans-serif; }}
        .ticker-wrap {{ width: 100%; overflow: hidden; background-color: rgba(0, 0, 0, 0.85); box-sizing: border-box; padding: 12px 0; border-top: 3px solid #ffcc00; }}
        .ticker {{ display: inline-block; white-space: nowrap; padding-left: 100%; animation: marquee 35s linear infinite; font-size: 26px; color: #ffffff; font-weight: bold; letter-spacing: 0.5px; }}
        @keyframes marquee {{ 0% {{ transform: translate3d(0, 0, 0); }} 100% {{ transform: translate3d(-100%, 0, 0); }} }}
    </style>
</head>
<body>
    <div class="ticker-wrap">
        <div class="ticker">{ticker_text}</div>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_html()
