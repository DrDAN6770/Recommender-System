# 資料分析專案名稱
**電影推薦系統**

## 專案概述
在這個部分，提供對你的專案進行簡要描述，說明你專案的目的和主要功能。

觀察到Netflix上的 **xx%推薦**大多時候都是蠻受用的(個人感受)，可以大致引導我去點擊觀看高推薦度的電影/影集，因此對推薦系統產生興趣，打算在一定程度上做到這點
1. 透過輸入電影找出相似度高的電影做推薦(電影相似度)
2. 透過協同過濾推薦電影(從使用者角度去推薦, A相似B, 可以互推對方未看過的電影) >> 如何建立使用者相思度待思考

## 專案結構
描述你專案的目錄結構，以及每個檔案或資料夾的用途。這可以幫助其他使用者更好地理解你的專案組織和如何導覽。
|檔案、資料夾名稱|用途|備註|
|:--|:--|:--|
|README.md|這份專案的簡介、Demo|無|
|input|電影資料集來源|*from movielens 100k dataset*|
|RS.ipynb|推薦系統主程式|RS.py為py版本|

## 安裝與使用方法
提供安裝和使用你的專案的指示。包括所需的相依套件、如何設置環境、安裝步驟和執行專案的指令。

* 環境設置 `Python3.11.2 +`
* 相依套件
    ```
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    ```
* 安裝步驟
    ```
    待補
    ```
* 執行
    ```
    待補
    ```
## 資料收集
如果你的專案需要特定的資料集，這裡可以提供一些關於如何獲取、處理或下載資料的指示。
* [MoiveLens](https://grouplens.org/datasets/movielens/)

## 資料分析流程
這一部分描述你的資料分析流程，包括你使用的方法、模型或演算法。你可以提供程式碼片段或流程圖來幫助讀者理解你的分析過程。
1. 根據需求載入資料集
2. 檢視資料集以及彙整

## 結果展示
展示和解釋你的資料分析結果。可以包括圖表、視覺化效果或統計數據，並提供解釋和洞察。
    ```
    待補
    ```