# Municipality_Database

総務省が発行する全国地方公共団体コードから、日本全国の市区町村の名称・読み仮名・種別を抽出・整形するツールです。

## Overview

PDFから市区町村データを抽出し、正規化されたCSVデータベースを生成します。

```
data_raw/Japan_Municipality.pdf
        │
        ▼
01_extract_from_JapanMunicipalityPDF.py
        │
        ▼
data_output/raw_masterDB.csv
        │
        ▼
02_normalize_municipality.py
        │
        ▼
data_output/municipality_DB.csv
```

## Requirements

```bash
pip install -r requirements.txt
```

| Package | Purpose |
|---|---|
| pdfplumber | PDFからテーブルを抽出 |
| pandas | データ整形・CSV出力 |
| jaconv | カタカナ→ひらがな変換 |

## Usage

### Step 1: PDFからデータ抽出

```bash
python 01_extract_from_JapanMunicipalityPDF.py
```

`data_raw/Japan_Municipality.pdf` を読み込み、`data_output/raw_masterDB.csv` を生成します。

### Step 2: データ正規化

```bash
python 02_normalize_municipality.py
```

`raw_masterDB.csv` を読み込み、種別分類・短縮名の付与・区の除外を行い、`data_output/municipality_DB.csv` を生成します。

## Output Format

`municipality_DB.csv` のカラム構成：

| Column | Description | Example |
|---|---|---|
| `municipality_code` | 団体コード | `011002` |
| `prefecture` | 都道府県名 | `北海道` |
| `municipality_name` | 市区町村名（正式名称） | `札幌市` |
| `reading_hiragana` | 読み仮名（ひらがな） | `さっぽろし` |
| `municipality_category` | 種別（市・町・村） | `市` |
| `name_short` | 短縮名（種別suffix除去） | `札幌` |
| `reading_short` | 短縮読み（suffix除去） | `さっぽろ` |

## Notes

- 政令指定都市の区（例：札幌市中央区）は除外されます
- 読み仮名は半角カタカナ・全角カタカナをひらがなに正規化します
- 出力CSVのエンコーディングは `UTF-8 BOM付き` です（Excel対応）
