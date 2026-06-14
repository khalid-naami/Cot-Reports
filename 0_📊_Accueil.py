import streamlit as st
import pandas as pd
from datetime import datetime
import os
from main_scraper import download_and_process_cot_data

def check_for_updates():
    """Vérifie si les données ont besoin d'être mises à jour (si plus de 7 jours)."""
    eur_csv = os.path.join('csv_folder', 'forex', 'eur.csv')
    
    # S'il n'y a pas de données du tout
    if not os.path.exists(eur_csv):
        with st.status("Initialisation des données en cours (2025-2026)..."):
            download_and_process_cot_data([2025, 2026])
        st.cache_data.clear()
        st.rerun()
        return

    try:
        df = pd.read_csv(eur_csv)
        if df.empty:
            download_and_process_cot_data([2025, 2026])
            st.rerun()
            return

        # Récupérer la date la plus récente
        latest_date_str = df['Date'].iloc[0]
        latest_date = datetime.strptime(latest_date_str, '%d/%m/%y').date()
        days_since = (datetime.now().date() - latest_date).days
        
        # Si les données ont plus de 7 jours, on tente une mise à jour
        if days_since >= 7:
            with st.status("Vérification des nouveaux rapports COT..."):
                success = download_and_process_cot_data([2025, 2026])
                if success:
                    st.cache_data.clear()
                    st.rerun()
    except Exception as e:
        st.error(f"Erreur lors de la vérification des mises à jour : {e}")

def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)

def main():
    st.title("Commitments of traders - Datas 📊")
    
    # Check for updates automatically
    check_for_updates()
    
    st.markdown(
        """
        ### Qu'est-ce que le COT ?

        Le Commitment of Traders report est un rapport hebdomadaire qui dévoile les positions nettes d'achat et de vente prises par les traders spéculateurs et institutionnels.
        Ce rapport indique comment les grosses institutions sont positionnées sur les marchés financiers, de cette manière nous pouvons en déduire dans quel sens la majorité des liquidités est orientée (Orderflow).
        
        ### Objectif

        Cette outil a pour objectif de faciliter l'analyse des rapports "Commitments of Traders" issues du site [cftc.gov](https://www.cftc.gov/).
        Les données récupérées sont des contrats à terme non commerciaux, tels que les devises forex majeures essentiellement.
        💵 💴 💶 💷  

        La finalité est de déduire **l'Orderflow de la Smart Money** de manière la plus probable en fonction de nos analyses.

        ### Applications
        - ⚖️ Comparateur d'actifs
        - 💸 Meilleures metriques

        ### Links
        📊 [Dashboard Options](https://dashboardoptions.com/) — A leading platform in financial market analysis
        
        [Khalid Naami](https://khalidnaami.com/) · [GitHub](https://github.com/khalid-naami) · [𝕏](https://x.com/DashboardOption) · [LinkedIn](https://www.linkedin.com/company/dashboard-options/) · [Instagram](https://www.instagram.com/dashboardoptions/) · [Discord](https://discord.gg/NRSzCYRzpJ) · [Telegram](https://t.me/dashboardoptions) · [YouTube](https://www.youtube.com/@DashboardOptions)
    """ 
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Rapports COT",
        page_icon="📊",
        layout="wide",
    )
    st.sidebar.markdown("""
<div style="color: #00ff85; font-size: 14px; font-weight: 500;">
    📊 <a href="https://dashboardoptions.com/" style="color: #00ff85; text-decoration: none; font-weight:700;">Dashboard Options</a><br>
    <span style="font-size:12px; color:#888;">A leading platform in financial market analysis</span>
</div>
<div style="font-size:13px; margin-top:8px;">
    <a href="https://khalidnaami.com/" style="color: #888;">Khalid Naami</a> · <a href="https://github.com/khalid-naami" style="color: #888;">GitHub</a> · <a href="https://x.com/DashboardOption" style="color: #888;">𝕏</a> · <a href="https://www.linkedin.com/company/dashboard-options/" style="color: #888;">LinkedIn</a> · <a href="https://www.instagram.com/dashboardoptions/" style="color: #888;">Instagram</a> · <a href="https://discord.gg/NRSzCYRzpJ" style="color: #888;">Discord</a> · <a href="https://t.me/dashboardoptions" style="color: #888;">Telegram</a> · <a href="https://www.youtube.com/@DashboardOptions" style="color: #888;">YouTube</a>
</div>
<hr style="border-color: #00ff85; opacity: 0.3;">
""", unsafe_allow_html=True)
    main()