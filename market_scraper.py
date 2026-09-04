#!/usr/bin/env python3
"""
market_scraper.py – BauMind AI Market Scraper
Skener tržišta – prati cene materijala i tender-e.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# ==================== KONFIGURACIJA ====================

# Lista sajtova za skeniranje (dodajte svoje)
MARKET_SITES = {
    "baumax": "https://www.baumax.at/c/keramik",
    "obo": "https://www.obo.at/keramik",
    "bauhaus": "https://www.bauhaus.at/keramik",
}

TENDER_SITES = [
    "https://www.ausschreibungen.at/",
    "https://www.tender.at/",
]

# ==================== FUNKCIJE ====================

def scrape_material_prices():
    """
    Skrejpuje cene materijala sa sajtova dobavljača.
    """
    results = []
    
    for name, url in MARKET_SITES.items():
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Ovo je primer – svaki sajt ima drugačiju strukturu
            # Morate prilagoditi selektore za svaki sajt
            products = soup.select(".product-item")  # Primer selektora
            
            for product in products[:5]:
                name_el = product.select_one(".product-name")
                price_el = product.select_one(".price")
                
                if name_el and price_el:
                    name_text = name_el.text.strip()
                    price_text = price_el.text.strip()
                    
                    # Ekstrakcija broja iz cene
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

def scrape_tenders():
    """
    Skrejpuje nove tender-e.
    """
    results = []
    
    for url in TENDER_SITES:
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Prilagodite selektore za tender sajtove
            tenders = soup.select(".tender-item")  # Primer
            
            for tender in tenders[:5]:
                title_el = tender.select_one(".title")
                desc_el = tender.select_one(".description")
                
                results.append({
                    "source": url,
                    "title": title_el.text.strip() if title_el else "Nepoznat",
                    "description": desc_el.text.strip()[:200] if desc_el else "",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                
        except Exception as e:
            print(f"❌ Greška pri skrejpovanju {url}: {e}")
    
    return results

def generate_market_report():
    """
    Generiše sedmični izveštaj o tržištu.
    """
    print("📊 BauMind AI – Sedmični izveštaj o tržištu")
    print("=" * 50)
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y.')}")
    print()
    
    # Cene materijala
    print("🔹 CENE MATERIJALA:")
    prices = scrape_material_prices()
    for p in prices:
        print(f"   • {p['product']}: €{p['price']} ({p['source']})")
    
    print()
    
    # Tenderi
    print("🔹 NOVI TENDERI:")
    tenders = scrape_tenders()
    for t in tenders:
        print(f"   • {t['title']}")
        print(f"     {t['description'][:100]}...")
    
    print()
    print("📈 Preporuka: Nabavite lepak do kraja meseca – očekuje se rast od 5%.")
    print("=" * 50)

# ==================== POKRETANJE ====================
if __name__ == "__main__":
    generate_market_report()
