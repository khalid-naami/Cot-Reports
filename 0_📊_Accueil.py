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

        ### Contact & Autres Projets
        - [About me](https://khalid-naami.github.io/)
        - [Times series analysis](https://seasonality-data.streamlit.app/)
    """ 
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Rapports COT",
        page_icon="📊",
        layout="wide",
    )
    main()