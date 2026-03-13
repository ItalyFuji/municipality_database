import pandas as pd
from pathlib import Path

# Path setting
INPUT_PATH = Path("data_output/raw_masterDB.csv")
OUTPUT_PATH = Path("data_output/municipality_DB.csv")

def format_municipality(row):
    kanji = str(row["municipality_name"])
 
    gana = str(row["reading_hiragana"])

    category = None
    short_kanji = kanji
    short_gana = gana

    # Filter out wards ("区") by returning None
    if kanji.endswith("区"):
        return pd.Series([None, None, None])

    # Extract category and remove suffixes from kanji and hiragana
    # Handle Cities (市)
    if kanji.endswith("市"):
        short_kanji = kanji[:-1]
        category = "市"
        if gana.endswith("し"):
            short_gana = gana[:-1]

    # Handle Towns (町)
    elif kanji.endswith("町"):
        short_kanji = kanji[:-1]
        category = "町"
        if gana.endswith("まち"):
            short_gana = gana[:-2]
        elif gana.endswith("ちょう"):
            short_gana = gana[:-3]

    # Handle Villages (村)
    elif kanji.endswith("村"):
        short_kanji = kanji[:-1]
        category = "村"
        if gana.endswith("むら"):
            short_gana = gana[:-2]
        elif gana.endswith("そん"):
            short_gana = gana[:-2]        
    
    return pd.Series([category, short_kanji, short_gana])

def main():
    df = pd.read_csv(INPUT_PATH)

    df[["municipality_category", "name_short", "reading_short"]] = df.apply(format_municipality, axis=1)

    # Remove rows that were identified as wards ("区")
    df = df.dropna(subset=["municipality_category"])

    # Remove duplicate entries based on municipality code, prefecture, and name
    df = df.drop_duplicates(subset=["municipality_code", "prefecture", "municipality_name"], keep="first")

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Completed building Municipality_Database")

if __name__ == "__main__":
    main()