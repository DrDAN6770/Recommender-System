# 資料分析專案名稱
**電影推薦系統**

## 專案概述
在這個部分，提供對你的專案進行簡要描述，說明你專案的目的和主要功能。

觀察到Netflix上的 **xx%推薦**大多時候都是蠻受用的(個人感受)，可以大致引導我去點擊觀看高推薦度的電影/影集，因此對推薦系統產生興趣，打算在一定程度上做到這點
1. 透過輸入電影找出相似度高的電影做推薦(內容相似度)
2. 透過協同過濾推薦電影(從使用者角度去推薦, A相似B, 可以互推對方未看過的電影)

## 專案結構
描述你專案的目錄結構，以及每個檔案或資料夾的用途。這可以幫助其他使用者更好地理解你的專案組織和如何導覽。
|檔案、資料夾名稱|用途|備註|
|:--|:--|:--|
|README.md|這份專案的簡介、Demo|無|
|input|電影資料集來源、經處理後資料檔案|*from movielens 100k dataset* *cleaned_data.csv*|
|DataProcess.py|原始資料處理||
|RS_CB.ipynb|基於內容相似度做推薦|.py為py版本|
|RS_CF.ipynb(待補)|基於協同過濾做推薦|.py為py版本|

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
  
  ![image](https://github.com/dscareer-bootcamp/data-analytics-starter-DrDAN6770/assets/118630187/1260afb8-58fa-4776-95fc-82a459ae57b5)

* 欄位定義

|No.|名稱|定義|
|:--|:--|:--|
|1|user_id|使用者id|
|2| movie_id | 電影id|
|3| rating | 評分(1~5)|
|4| timestamp | UTC of 1/1/1970 後幾秒|
|5| age | 年紀|
|6| sex | 性別|
|7| occupation | 職業|
|8| zip_code | 郵政編碼|
|9| movie_title | 電影名稱|
|10| release_date | 發佈日期|
|11| video_release_date | 家用媒體市場發佈日期(DVD、非電影院)|
|12| IMDb_URL | 該電影IMDb網址|
|13 ~ 31| 電影分類類別|unknown, Action, Adventure, Animation, Children's, Comedy, Crime, Documentary,                      Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western|

## 資料分析流程
這一部分描述你的資料分析流程，包括你使用的方法、模型或演算法。你可以提供程式碼片段或流程圖來幫助讀者理解你的分析過程。
1. 根據需求載入資料集
2. 檢視資料集以及彙整
3. 進行資料EDA
4. 進行資料清理(去重、去無效值、刪減欄位)
5. 根據不同推薦法進行處理
    * **Content-based filtering (CB)**

            透過電影的類型(genre)
            算出每一部電影對其他不電影的相似度
            這裡是透過餘弦相似度的方式

    * **Collaborative filtering (CF)**

            待補

    *   **餘弦相似度(Cosine Similarity)**:

            藉由測量2個向量夾角的餘弦值，來度量它們之間的相似性。
            向量之間夾角越小，表示2個向量的方向越接近
            方向一致夾角度數θ為0，餘弦值為1
            反之向量之間夾角θ越大，表示2個向量的方向差異越大
            當方向相反時餘弦值為-1
        
          ![image](https://github.com/dscareer-bootcamp/data-analytics-starter-DrDAN6770/assets/118630187/2eac0c68-ba5b-49af-a895-d84ef047fc0f)


## 結果展示
展示和解釋你的資料分析結果。可以包括圖表、視覺化效果或統計數據，並提供解釋和洞察。

* Rating 數量分佈

    ![image](https://github.com/dscareer-bootcamp/data-analytics-starter-DrDAN6770/assets/118630187/5e71ab77-07d6-4185-ba78-9a359591ec29)

* 電影類型 數量分佈

    ![image](https://github.com/dscareer-bootcamp/data-analytics-starter-DrDAN6770/assets/118630187/1a8e77c0-a2cc-4579-ac61-ed987aa41688)

* 內容過濾 Content-based filtering (CB)
    ```
    # Test
    # get_similar_movies_bycontent(data_set, 來源電影編號, 已看過電影編號(內建無), 推薦幾部相似的(內建10))
    # 電影編號1為 Toy Story (1995)
    # seen = contentBased_df['movie_id'].values << 全電影都看過
    
    seen = [700, 240, 18, 2]
    get_similar_movies_bycontent(contentBased_df, 1, seen)
    ```
    ![image](https://github.com/dscareer-bootcamp/data-analytics-starter-DrDAN6770/assets/118630187/2304940c-7519-4435-97f8-76a28c782217)

