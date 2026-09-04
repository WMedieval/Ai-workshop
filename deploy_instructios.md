# 🚀 BAU MIND AI – KORAK PO KORAK IMPLEMENTACIJA

## 📌 PREDUSLOVI

1. **GitHub** nalog (besplatno)
2. **Render.com** nalog (besplatni hosting)
3. **Gmail** nalog (za email integraciju)
4. **OpenAI** API ključ (https://platform.openai.com/api-keys)
5. **Google Cloud** projekat (za Calendar API)

## 📥 KORAK 1: POSTAVLJANJE FRONTENDA

1. Uploaduj sve fajlove na GitHub repozitorijum
2. Poveži sa Netlify ili Render (staticki deo)

## 🐍 KORAK 2: POSTAVLJANJE PYTHON BACKEND-A

1. Na Render.com klikni "New +" → "Web Service"
2. Poveži sa GitHub repozitorijumom
3. Postavi:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python email_parser.py`
4. Dodaj Environment Variables (u Render dashboard):
   - `EMAIL_USER=your_email@gmail.com`
   - `EMAIL_PASS=your_app_password`
   - `OPENAI_API_KEY=your_key`

## 🌐 KORAK 3: TESTIRANJE

1. Otvori: `https://your-app.onrender.com`
2. Testiraj prijavu radnika
3. Testiraj email analizu
4. Testiraj dashboard

## ⚠️ VAŽNO

- Nikad ne uploaduj `.env` fajl na GitHub
- Koristi Environment Variables na Render-u
- Google Calendar zahteva `credentials.json` (ne uploaduj na GitHub)
