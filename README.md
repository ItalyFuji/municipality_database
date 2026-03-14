# Municipality_Database

総務省が発行する全国地方公共団体コードから、日本全国の市区町村の名称・読み仮名・種別を抽出・整形するツールです。

A tool that extracts and normalizes municipality names, readings, and categories from the Japanese Municipality Code PDF published by the Ministry of Internal Affairs and Communications.

---

## Overview / 概要

PDFから市区町村データを抽出し、正規化されたCSVデータベースを生成します。

Extracts municipality data from a PDF and generates a normalized CSV database.

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

---

## Requirements / 必要なパッケージ

```bash
pip install -r requirements.txt
```

| Package | Purpose（用途） |
|---|---|
| pdfplumber | PDFからテーブルを抽出 / Extract tables from PDF |
| pandas | データ整形・CSV出力 / Data processing and CSV output |
| jaconv | カタカナ→ひらがな変換 / Convert katakana to hiragana |
| pytest | テスト実行 / Run tests |

---

## Usage / 使い方

### Option A: Run all steps at once / まとめて実行

```bat
run.bat
```

### Option B: Run step by step / ステップごとに実行

#### Step 1: Extract data from PDF / PDFからデータ抽出

```bash
python 01_extract_from_JapanMunicipalityPDF.py
```

`data_raw/Japan_Municipality.pdf` を読み込み、`data_output/raw_masterDB.csv` を生成します。

Reads `data_raw/Japan_Municipality.pdf` and generates `data_output/raw_masterDB.csv`.

#### Step 2: Normalize the database / データ正規化

```bash
python 02_normalize_municipality.py
```

`raw_masterDB.csv` を読み込み、種別分類・短縮名の付与・区の除外を行い、`data_output/municipality_DB.csv` を生成します。

Reads `raw_masterDB.csv`, classifies municipality types, adds short names, removes wards, and generates `data_output/municipality_DB.csv`.

---

## Output Format / 出力フォーマット

`municipality_DB.csv` のカラム構成 / Column structure of `municipality_DB.csv`:

| Column | Description | Example |
|---|---|---|
| `municipality_code` | 団体コード / Municipality code | `011002` |
| `prefecture` | 都道府県名 / Prefecture name | `北海道` |
| `municipality_name` | 市区町村名（正式名称）/ Full municipality name | `札幌市` |
| `reading_hiragana` | 読み仮名（ひらがな）/ Reading in hiragana | `さっぽろし` |
| `municipality_category` | 種別（市・町・村）/ Category | `市` |
| `name_short` | 短縮名（種別suffix除去）/ Short name | `札幌` |
| `reading_short` | 短縮読み（suffix除去）/ Short reading | `さっぽろ` |

---

## Testing / テスト

```bash
pytest test_normalize.py -v
```

`02_normalize_municipality.py` の `format_municipality()` 関数に対する単体テストを実行します。

Runs unit tests for the `format_municipality()` function in `02_normalize_municipality.py`.

---

## Notes / 注意事項

- 政令指定都市の区（例：札幌市中央区）は除外されます / Wards of designated cities (e.g., Chuo-ku, Sapporo) are excluded.
- 読み仮名は半角・全角カタカナをひらがなに正規化します / Readings are normalized from katakana (half/full-width) to hiragana.
- 出力CSVのエンコーディングは `UTF-8 BOM付き` です（Excel対応）/ Output CSV is encoded in `UTF-8 with BOM` for Excel compatibility.
