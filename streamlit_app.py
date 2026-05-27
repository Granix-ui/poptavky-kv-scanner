import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

st.set_page_config(page_title="Poptávky KV", layout="wide")
st.title("🔨 Poptávky Scanner – Stavebnictví & Řemesla")
st.markdown("**Karlovarský kraj** | Pouze relevantní stavební poptávky")

now = datetime.now()

# Opravené a funkční URL
portaly = {
    "ePoptávka.cz": "https://poptavky.epoptavka.cz/karlovarsky-kraj",
    "AAA Poptávka": "https://www.aaapoptavka.cz/poptavky?filters%5Bregion%5D=karlovarsky-kraj",
    "Poptavky.cz": "https://www.poptavky.cz/poptavky/karlovarsky-kraj",
    "Poptavej.cz": "https://www.poptavej.cz/poptavky/kraj-karlovarsky",
    "NejŘemeslníci.cz": "https://www.nejremeslnici.cz/poptavky?region=karlovarsky-kraj"
}

if st.button("🔄 Načíst aktuální poptávky", type="primary"):
    with st.spinner("Prohledávám portály..."):
        for nazev, base_url in portaly.items():
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                response = requests.get(base_url, timeout=15, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "lxml")

                st.markdown(f"### {nazev}")

                active = []
                keywords = ["stavba", "rekonstrukce", "střecha", "fasáda", "omítka", "podlaha", "instalace", "topná", "izolace", "zednické", "malování", "okna", "dveře", "koupelna", "kuchyň", "terasa", "garáž"]

                for a in soup.find_all("a", href=True):
                    text = a.text.strip()
                    if len(text) < 15:
                        continue
                    
                    href = a["href"]
                    full_link = urljoin(base_url, href)

                    if any(kw in text.lower() for kw in keywords):
                        active.append(f"[{text}]({full_link})")

                if active:
                    for item in active[:12]:   # omezíme na 12 položek na portál
                        st.markdown(f"- {item}", unsafe_allow_html=True)
                else:
                    st.markdown("Žádné aktuální stavební poptávky nenalezeny.")

            except Exception as e:
                st.error(f"{nazev}: Chyba ({e})")

st.caption("Poptávkový scanner • Karlovarský kraj • Stavebnictví a řemesla")
