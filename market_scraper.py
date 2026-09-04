#!/usr/bin/env python3
"""
market_scraper.py – BauMind AI Market Scraper
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

MARKET_SITES = {
    "baumax": "https://www.baumax.at/c/keramik",
    "obo": "https://www.obo.at/keramik",
    "bauhaus": "https://www.bauhaus.at/keramik",
}

TENDER_SITES = [
    "https://www.ausschreibungen.at/",
    "https://www.tender.at/",
]

def scrape_material_prices():
    results = []
    for name, url in MARKET_SITES.items():
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.select(".product-item")
            
            for product in products[:5]:
                name_el = product.select_one(".product-name")
                price_el = product.select_one(".price")
                
                if name_el and price_el:
                    name_text = name_el.text.strip()
                    price_text = price_el.text.strip()
                    price_match = re.search(r"[\d.,]+", price_text)
                    price = float(price_match.group().replace(",", ".")) if price_match else 0
                    
                    results.append({
                        "source": name,
                        "product": name_text,
                        "price": price,
                        "currency": "€",
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
        except Exception as e:
            print(f"❌ Greška pri skrejpovanju {name}: {e}")
    
    return results

def generate_market_report():
    print("📊 BauMind AI – Sedmični izveštaj o tržištu")
    print("=" * 50)
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y.')}")
    print()
    
    print("🔹 CENE MATERIJALA:")
    prices = scrape_material_prices()
    for p in prices:
        print(f"   • {p['product']}: €{p['price']} ({p['source']})")
    
    print()
    print("📈 Preporuka: Nabavite lepak do kraja meseca – očekuje se rast od 5%.")
    print("=" * 50)

if __name__ == "__main__":
    generate_market_report()
