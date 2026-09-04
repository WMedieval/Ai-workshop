# 🚀 BAU MIND AI – KORAK PO KORAK IMPLEMENTACIJA

## 📌 PREDUSLOVI

1. **GitHub / GitLab** nalog (besplatno)
2. **Render.com** ili **PythonAnywhere** nalog (besplatni hosting)
3. **Gmail** nalog (za email integraciju)
4. **OpenAI** API ključ (https://platform.openai.com/api-keys)
5. **Google Cloud** projekat (za Calendar API)

---

## 📥 KORAK 1: POSTAVLJANJE FRONTENDA (Vidljivi deo)

**Opcija A: Na 2star.co (vaš postojeći hosting)**

1. Sačuvajte `index.html` na računaru
2. Prijavite se na cPanel 2star.co
3. Otpremite fajl u `public_html/` folder
4. Otvorite: `https://www.2star.co/index.html`

**Opcija B: Na Netlify (besplatno)**

1. Napravite nalog na https://www.netlify.com
2. Drag & drop `index.html` na dashboard
3. Dobićete link: `https://your-app.netlify.app`

---

## 🐍 KORAK 2: POSTAVLJANJE PYTHON BACKEND-A

**Render.com (Preporučujem – najlakše)**

1. Napravite nalog na https://render.com
2. Kliknite "New +" → "Web Service"
3. Povežite sa GitHub repozitorijumom
4. Postavite:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python email_parser.py`
5. Dodajte Environment Variables (u Render dashboard):
