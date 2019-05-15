# Scrapy框架製作求職網爬蟲  
----------------------  
我利用Scrapy製作了104和1111人力銀行的爬蟲，並存到Mongodb中，以下簡單說明操作及框架內容。  
如果想了解Scrapy內容可以到Scrapy的官網參考他們的[Documentation](https://docs.scrapy.org/en/latest/)(附上連結)。  
  
## 操作說明
將這個專案Clone後，開啟終端機到專案資料夾，輸入以下指令。  
`scrapy crawl [spider名稱]`  
`[spider名稱]` 專案內有兩隻spider，依照要爬取的網站輸入名稱，如果想要輸出`json`或`csv`的話，在後面加上`-o 檔案名稱.json`，詳參考官網說明。  
  
輸入之後會顯示，  
`Enter the keyword to be 104/1111 scrape:`  
輸入關鍵字後即開始爬取。  
如果不想寫入資料庫請在`setting.py`中，把`MongoDBPipline`關掉。

## 框架說明
* Spider  
我製作了兩隻spider，分別爬取104和1111人力銀行，Spider名稱分別是`crawler104`和`crawler104`。  
其中我有限制爬取頁數限制(50頁)。  
\*友善提醒: 一定要設頁數限制，有些關鍵字會爬不完而且造成人家網站負擔。

* Item  
item內容如下:  
```python
    jobsalary = scrapy.Field() # 薪資
    jobname = scrapy.Field()   # 職稱
    jobcompany = scrapy.Field()# 公司名稱
    jobexp = scrapy.Field()    # 經驗條件
    jobedu = scrapy.Field()    # 學歷條件
    jobarea = scrapy.Field()   # 工作地點
    jobindcat = scrapy.Field() # 產業
    jobdate = scrapy.Field()   # 更新日期
    jobapply = scrapy.Field()  # 應徵人數
    sourceweb = scrapy.Field() # 來源網站
    keyword = scrapy.Field()   # 關鍵字
```
* Pipeline  
本專案主要有3個pipeline，  
    * DuplicatesPipeline  
    功能為避免重複資料寫入。
    * JobItemPipeline  
    此為item pipeline，將item整理成要寫入的格式，以下說明。  
        * 日期  
        因為兩個網站日期格式不同，整理後以`datetime.datetime`格式存入資料庫。  
        * 應徵人數  
        將應徵人數分3大類`Class 1 < 10人 < Class 2 < 30人 < Class 3`  
        * 薪資  
        我將薪資範圍平均後存入資料庫 (~~雖然一直想取最低值 你懂 呵呵~~)，時薪的部分乘以160小時換算月薪 (台灣平均每月工作時數)。  
        * 經驗條件  
        換算成整數形式寫入資料庫。
    * MongoDBPipline  
    將資料寫入MongoDB內，uri、Client設定要改一下哦。

* Setting  
`setting.py` 這個檔案是支配Scrapy框架的配置檔，可以在裡面設定整個框架的默認設定。  

##   附上爬取後資料統計結果(5/14)
  [統計結果](demo.ipynb)
  
內容僅供技術交流   
如有問題或建議，敬請不吝指教。  
<jiasi.cv03g@g2.nctu.edu.tw>
