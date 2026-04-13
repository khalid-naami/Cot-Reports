# Commitment of Traders application d'analyse
Cette application web a été développée à l'aide de la librairie [Streamlit](https://streamlit.io/). 

![Aperçu de l'application](preview.png)

### À propos & Projets
- [About me](https://khalid-naami.github.io/)
- [Times series analysis](https://seasonality-data.streamlit.app/)

L'objectif de cet outil est de faciliter l'analyse des rapports **"Commitments of Traders"** issues du site [cftc.gov](https://www.cftc.gov/).

## Qu'est-ce que le COT ?
Le Commitment of Traders report est un rapport hebdomadaire qui dévoile les positions nettes d'achat et de vente prises par les traders spéculateurs et institutionnels.
Ce rapport indique comment les grosses institutions sont positionnées sur les marchés financiers, de cette manière nous pouvons en déduire dans quel sens la majorité des liquidités est orientée (Orderflow).

#### En savoir plus
Pour comprendre comment utiliser un rapport et savoir de quoi il est constitué, visitez **https://www.cftc.gov/MarketReports/CommitmentsofTraders/AbouttheCOTReports/index.htm**
## Objectif
Les données récupérées sont des contrats à terme non commerciaux, tels que les devises forex majeures essentiellement.
💵 💴 💶 💷  
La finalité est de déduire **l'Orderflow de la Smart Money** de manière la plus probable en fonction de nos analyses.
       
## Applications
### ⚖️ Comparateur d'actifs
Le comparateur d'actifs permet d'identifier le flux d'ordres à l'achat et à la vente d'un actif donné puis de le comparer à celui d'un autre actif.
Les tableaux représentent tous les rapports COT hebdomadaires publiés depuis plusieurs mois.
Ainsi, deux actifs corrélés négativement démontrent que la paire d'actifs tend vers un Orderflow important.

#### Exemple
- Le nombre d'**achat** sur EUR ne cesse d'**augmenter**.
- Le nombre de **vente** sur USD ne cesse d'**augmenter**. 
                
 **Conclusion**: Un plan d'achat sur la paire de devise EUR/USD est à privilégier.

![image](https://user-images.githubusercontent.com/80407460/207116155-2478972d-e7d9-42c3-8e46-2f201f3287b9.png)

### 💸 Meilleures metriques
Un algorithme permet d'identifier puis de classer les actifs qui ont reçu les plus grosses injections de positions, selon les derniers rapports "Commitments of traders" publiés le vendredi le plus récent.

#### Etape 1 : Premier tri effectué sur chaque actif.

Pour un actif donné:
1. Récupère le **volume de position long** du dernier rapport en date. (Injection de long + clotûre de short).
2. Récupère le **volume de position short** du dernier rapport en date. (Injection de short + clotûre de long).
3. On fait la différence entre le volume de long et de short pour identifier l'orderflow.
4. On refait les mêmes opérations avec tous les autres rapports précédents. ( échantillon de données sur quasi 1 an, depuis le 4 Janvier 2022)
5. On classe tous les volumes de positions long d'une part, et les volumes de positions short d'autre part. **Du plus grand au plus petit**.
6. Avec ce classement, on peut comparer le dernier volume de position injecté dans l'actif avec tous les autres volumes précédemment injectés.
7. De cette manière, plus la position du dernier volume de position injecté est importante dans le classement, plus l'actif est susceptible de nous    intéresser car fort orderflow.
8. (Exemple: Si le dernier volume de position injecté est classé 1er du classement, alors on en conclu que c'est la plus grosse injection d'ordre de l'année sur cet actif )
#### Etape 2 : Nouveau tri

Enfin, on effectue un nouveau classement composé du rang des derniers volumes injectés de chaque actif (grâce à l'étape 1)
Ce classement est observable ci-dessous sous forme de métrique.
            
![image](https://user-images.githubusercontent.com/80407460/207116695-ca7cfd49-18ed-4b17-813e-81aa96235bfd.png)


# Assets & Data sources

| Asset       | Symbol| Type | Data source |
| -------------|-------------| -------------|-------------|
| Dollar américain | USD| Major currency | https://www.cftc.gov/dea/futures/deanybtsf.htm |
| Euro | EUR | Major currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Yen japonais | JPY | Major currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Dollar australien | AUD | Major currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Dollar néo-zélandais | NZD | Major currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Dollar canadien | CAD | Major currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Franc suisse | CHF | Major currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Peso mexicain | MXN | Minor currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Réal brésilien | BRL | Minor currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Rand | ZAR | Minor currency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Bitcoin| BTC | Cryptocurrency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| Ethereum | ETH | Cryptocurrency | https://www.cftc.gov/dea/futures/deacmesf.htm |
| NASDAQ-100 | NASDAQ | Index | https://www.cftc.gov/dea/futures/deacmesf.htm |
| S&P500 | S&P500 | Index | https://www.cftc.gov/dea/futures/deacmesf.htm |
| DOW JONES | DJ | Index | https://www.cftc.gov/dea/futures/deacbtsf.htm |
| Petrole | OIL | Depleting asset | https://www.cftc.gov/dea/futures/deanymesf.htm |
| Gaz | GAS | Depleting asset | https://www.cftc.gov/dea/futures/deanymesf.htm |
| Argent | SILVER | Metals | https://www.cftc.gov/dea/futures/deacmxsf.htm |
| Cuivre | COPPER | Metals | https://www.cftc.gov/dea/futures/deacmxsf.htm |
| OR | GOLD | Metals | https://www.cftc.gov/dea/futures/deacmxsf.htm |



