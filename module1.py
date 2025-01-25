import os
from datetime import datetime

domain = "https://www.web-sciences.fr"
folder_path = "C:/Users/CAMPION Philippe/bultec.github.io"

def generate_sitemap():
    urls = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.relpath(os.path.join(root, file), folder_path)
                url = f"{domain}/{file_path.replace(os.sep, '/')}"
                lastmod = datetime.now().strftime('%Y-%m-%d')
                urls.append(f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>"""
    with open("sitemap.xml", "w") as file:
        file.write(sitemap)
    print("Sitemap generated as sitemap.xml")

# Utilisation
generate_sitemap()
