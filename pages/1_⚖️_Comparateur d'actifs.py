import streamlit as st
import pandas as pd
from datetime import date
import seaborn as sns
import os

CHICAGO = [
            ['EUR','Code-099741','deacmesf','forex',[]], 
            ['JPY','Code-097741','deacmesf','forex',[]],
            ['AUD','Code-232741','deacmesf','forex',[]],
            ['NZD','Code-112741','deacmesf','forex',[]],
            ['CAD','Code-090741','deacmesf','forex',[]],
            ['GBP','Code-096742','deacmesf','forex',[]],
            ['CHF','Code-092741','deacmesf','forex',[]],
            ['MXN','Code-095741','deacmesf','forex',[]],
            ['BRL','Code-102741','deacmesf','forex',[]],
            ['ZAR','Code-122741','deacmesf','forex',[]],
            ['BTC','Code-133741','deacmesf','crypto',[]],
            ['ETH','Code-146021','deacmesf','crypto',[]],
            ['NASDAQ-100','Code-209742','deacmesf','index',[]],
            ['S&P 500','Code-13874A','deacmesf','index',[]],
]

DJ = [['DOW JONES','Code-124603','deacbtsf','index',[]]]
USD = [['USD','Code-098662','deanybtsf','forex',[]]]
NEW_YORK = [
            ['OIL','Code-067651','deanymesf','other',[]],
            ['GAS','Code-023651','deanymesf','other',[]],
]
COMMODITY = [
            ['SILVER','Code-084691','deacmxsf','metals',[]],
            ['COPPER','Code-085692','deacmxsf','metals',[]],
            ['GOLD','Code-088691','deacmxsf','metals',[]],
]

ALL_ASSET = CHICAGO + DJ + USD + NEW_YORK + COMMODITY

def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)

def customize_dataframe(df, start):
    # Palette with vivid red, neutral, and vivid green
    cm = sns.blend_palette(['#ff4b4b', '#1e1e1e', '#00c04b'], as_cmap=True, n_colors=100)
    
    df_sliced = df.drop(['Long','Short','url_report', 'type'], axis=1).head(start)
    
    # Calculate global max abs for Net position so gradient is centered on 0 if possible
    # We'll let seaborn handle min/max, but for bars we want positive/negative coloring.
    
    df_customized = (
        df_sliced.style.background_gradient(subset=['Net position'], cmap=cm)
        .bar(color=['#ff4b4b','#00c04b'], align='zero', subset=['Change long', 'Change short'])
        .format(thousands=' ')
    )
    return df_customized

def convert_df(df):
    return df.to_csv().encode('utf-8')

def main():
    st.header("Comparateur d'actifs financiers")
    
    st.markdown(
            """
            Le comparateur d'actifs permet d'identifier le flux d'ordres à l'achat et à la vente d'un actif donné puis de le comparer à celui d'un autre actif.
            
            Les tableaux représentent tous les rapports COT hebdomadaires publiés depuis plusieurs mois.
            Ainsi, deux actifs corrélés négativement démontrent que la paire d'actifs tend vers un Orderflow important.
            """ 
        )
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Voir exemple"):
            st.markdown(
                """
                - Le nombre d'**achat** sur EUR ne cesse d'**augmenter**.
                - Le nombre de **vente** sur USD ne cesse d'**augmenter**. 
                
                **Conclusion**: Un plan d'achat sur la paire de devise EUR/USD est à privilégier.
            """ 
            )

    try:
        df_usd = csv_to_dataframe("csv_folder/forex/usd.csv")
        dates = list(df_usd.index)
        default_start = dates[-1] if dates else None
    except FileNotFoundError:
        st.error("Les données ne sont pas encore disponibles. Veuillez initialiser les données sur la page d'Accueil.")
        st.stop()

    # Input slider pour filter la date range
    start = st.select_slider("Sélectionner la date de début", options=list(reversed(dates)), value=default_start)

    # Récupère l'index de l'USD dans la liste pour l'afficher par défaut dans la selectbox
    choices_asset = [item[0] for item in ALL_ASSET]
    st.caption("Etude sur **{}** semaines".format(dates.index(start)+1))
    col1, col2 = st.columns(2)

    with col1:
        option1 = st.selectbox('Premier actif ?', choices_asset, index=0) # EUR default
        index1 = choices_asset.index(option1)
        df_asset1 = csv_to_dataframe(f"csv_folder/{ALL_ASSET[index1][3]}/{option1.lower()}.csv",'Date')
        
        csv1 = convert_df(df_asset1)
        df_custom_1 = customize_dataframe(df_asset1, dates.index(start)+1)
        
        st.markdown(f"<h1 style='text-align: center; color: white;'>{option1}</h1>", unsafe_allow_html=True)
        # CHANGED BACK: st.table is required to render pandas Styler `.bar()` HTML
        st.table(df_custom_1)
        
        # Download button
        date_str1 = df_asset1.index[0].replace("/","-")
        st.download_button(
            label="Exporter le CSV",
            data=csv1,
            file_name=f'{option1}_{date_str1}.csv',
            mime='text/csv',
            key='button1',
        )

    with col2:
        option2 = st.selectbox('Second actif ?', choices_asset, index=15) # USD default
        index2 = choices_asset.index(option2)
        df_asset2 = csv_to_dataframe(f"csv_folder/{ALL_ASSET[index2][3]}/{option2.lower()}.csv",'Date')
        
        csv2 = convert_df(df_asset2)
        df_custom_2 = customize_dataframe(df_asset2, dates.index(start)+1)
        
        st.markdown(f"<h1 style='text-align: center; color: white;'>{option2}</h1>", unsafe_allow_html=True)
        st.table(df_custom_2)
       
        # Download button
        date_str2 = df_asset2.index[0].replace("/","-")
        st.download_button(
            label="Exporter le CSV",
            data=csv2,
            file_name=f'{option2}_{date_str2}.csv',
            mime='text/csv',
            key='button2',
        )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Comparateur d'actifs",
        page_icon="⚖️",
        layout="wide",
    )
    main()
