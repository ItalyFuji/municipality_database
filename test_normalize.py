import importlib.util
import pandas as pd
import pytest
from pathlib import Path

# 02_normalize_municipality.py はファイル名が数字始まりのため importlib で読み込む
spec = importlib.util.spec_from_file_location(
    "normalize", Path(__file__).parent / "02_normalize_municipality.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

format_municipality = module.format_municipality


def make_row(name, reading):
    return pd.Series({"municipality_name": name, "reading_hiragana": reading})


# --- 市 ---

def test_city_shi_ending():
    result = format_municipality(make_row("札幌市", "さっぽろし"))
    assert result.tolist() == ["市", "札幌", "さっぽろ"]

def test_city_reading_not_shi():
    # 「し」で終わる読みでも、短縮名(kanji)が正しく生成されることを確認
    result = format_municipality(make_row("四日市市", "よっかいちし"))
    assert result[0] == "市"
    assert result[1] == "四日市"

# --- 町 ---

def test_town_machi_ending():
    result = format_municipality(make_row("能勢町", "のせまち"))
    assert result.tolist() == ["町", "能勢", "のせ"]

def test_town_cho_ending():
    result = format_municipality(make_row("愛荘町", "あいしょうちょう"))
    assert result.tolist() == ["町", "愛荘", "あいしょう"]

# --- 村 ---

def test_village_mura_ending():
    result = format_municipality(make_row("檜原村", "ひのはらむら"))
    assert result.tolist() == ["村", "檜原", "ひのはら"]

def test_village_son_ending():
    result = format_municipality(make_row("川上村", "かわかみそん"))
    assert result.tolist() == ["村", "川上", "かわかみ"]

# --- 区（除外対象） ---

def test_ward_is_filtered():
    result = format_municipality(make_row("中央区", "ちゅうおうく"))
    assert result.tolist() == [None, None, None]

def test_ward_with_prefix_is_filtered():
    result = format_municipality(make_row("札幌市中央区", "さっぽろしちゅうおうく"))
    assert result.tolist() == [None, None, None]

# --- ヘッダー・ノイズ（除外対象） ---

def test_header_noise_has_no_category():
    # 市・町・村・区に該当しない行はcategory=NaNになる（dropnaで除外される）
    result = format_municipality(make_row("市区町村名", "しくちょうそんめい"))
    assert pd.isna(result[0])
    assert result[1] == "市区町村名"
