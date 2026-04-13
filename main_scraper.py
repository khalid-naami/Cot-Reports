import pandas as pd
import requests
import zipfile
import io
import os
from datetime import datetime

# --- GLOBAL --- #
# Asset , Code, End_url, Type(folder), List of value
CHICAGO = [
    ['EUR','099741','deacmesf','forex',[]],
    ['JPY','097741','deacmesf','forex',[]],
    ['AUD','232741','deacmesf','forex',[]],
    ['NZD','112741','deacmesf','forex',[]],
    ['CAD','090741','deacmesf','forex',[]],
    ['GBP','096742','deacmesf','forex',[]],
    ['CHF','092741','deacmesf','forex',[]],
    ['MXN','095741','deacmesf','forex',[]],
    ['BRL','102741','deacmesf','forex',[]],
    ['ZAR','122741','deacmesf','forex',[]],
    ['BTC','133741','deacmesf','crypto',[]],
    ['ETH','146021','deacmesf','crypto',[]],
    ['NASDAQ-100','209742','deacmesf','index',[]],
    ['S&P 500','13874A','deacmesf','index',[]],
]

DJ = [['DOW JONES','124603','deacbtsf','index',[]]]
USD = [['USD','098662','deanybtsf','forex',[]]]
NEW_YORK = [
    ['OIL','067651','deanymesf','other',[]],
    ['GAS','023651','deanymesf','other',[]],
]
COMMODITY = [
    ['SILVER','084691','deacmxsf','metals',[]],
    ['COPPER','085692','deacmxsf','metals',[]],
    ['GOLD','088691','deacmxsf','metals',[]],
]

ALL_ASSET = CHICAGO + DJ + USD + NEW_YORK + COMMODITY 

def download_and_process_cot_data(years=[2025, 2026]):
    """Downloads annual COT ZIP files and processes them for all assets."""
    all_years_data = []
    
    for year in years:
        print(f"Fetching COT data for {year}...")
        url = f"https://www.cftc.gov/files/dea/history/deacot{year}.zip"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print(f"  Failed to download {year} (Status: {response.status_code})")
                continue
                
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                filename = [name for name in z.namelist() if name.endswith('.txt') or name.endswith('.csv')][0]
                with z.open(filename) as f:
                    df_year = pd.read_csv(f, low_memory=False)
                    # Standardize column names (remove quotes and spaces)
                    df_year.columns = [c.strip().strip('"') for c in df_year.columns]
                    all_years_data.append(df_year)
            print(f"  Loaded {year}")
        except Exception as e:
            print(f"  Error for {year}: {e}")

    if not all_years_data:
        return False
        
    df_full = pd.concat(all_years_data, ignore_index=True)
    
    # Process each asset
    for asset in ALL_ASSET:
        name = asset[0]
        code = asset[1]
        report_url = asset[2]
        outdir = asset[3]
        
        # Filter by code (handling potential string variations)
        df_asset = df_full[df_full['CFTC Contract Market Code'].astype(str).str.strip().str.contains(code)].copy()
        
        if df_asset.empty:
            print(f"  No data found for {name} ({code})")
            continue
            
        # Map columns to original project format
        # Original: Date, Long, Short, Change long, Change short, Net position, url_report, type
        
        # Format Date to DD/MM/YY
        df_asset['Date'] = pd.to_datetime(df_asset['As of Date in Form YYYY-MM-DD']).dt.strftime('%d/%m/%y')
        
        res_df = pd.DataFrame({
            'Date': df_asset['Date'],
            'Long': df_asset['Noncommercial Positions-Long (All)'],
            'Short': df_asset['Noncommercial Positions-Short (All)'],
            'Change long': df_asset['Change in Noncommercial-Long (All)'],
            'Change short': df_asset['Change in Noncommercial-Short (All)'],
            'Net position': df_asset['Noncommercial Positions-Long (All)'] - df_asset['Noncommercial Positions-Short (All)'],
            'url_report': report_url,
            'type': outdir
        })
        
        # Sort newest first
        res_df = res_df.sort_values(by='Date', ascending=False, key=lambda x: pd.to_datetime(x, format='%d/%m/%y'))
        
        # Drop duplicates if any across years
        res_df = res_df.drop_duplicates(subset=['Date'])
        
        # Ensure output directory exists
        path = os.path.join('csv_folder', outdir)
        if not os.path.exists(path):
            os.makedirs(path)
            
        res_df.to_csv(os.path.join(path, f"{name.lower()}.csv"), index=False)
        print(f"  Processed {name}")
        
    return True

def main():
    success = download_and_process_cot_data([2025, 2026])
    if success:
        print("\nAll data updated successfully from 2025 until now.")
    else:
        print("\nData update failed.")

if __name__ == "__main__":
    main()