import streamlit as st
import pandas as pd
import requests
import zipfile
import io

st.title("Excel 表格上傳與顯示")

file_name = "Links_Gov_Data_to_get.xlsx"

if file_name is not None:

    # 讀取 Excel 文件的 'ALLTEMP' 工作表
    tables = pd.read_excel(file_name, sheet_name='ALLTEMP')

    st.write("工作表 'ALLTEMP' 中名為 'table' 的表格內容：")
    st.dataframe(tables)

    # 檢查是否存在 'DailyMeanTemperature_AllYear_url' 列
    if 'DailyMeanTemperature_AllYear_url' in tables.columns:
        urls = tables['DailyMeanTemperature_AllYear_url'].dropna().tolist()

        # 創建一個 BytesIO 物件，用於存儲 ZIP 文件
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            # 遍歷所有 URL，下載文件並添加到 ZIP 文件中
            for idx, url in enumerate(urls):
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # 檢查請求是否成功

                    # 根據 URL 或文件內容確定文件名和擴展名
                    file_extension = url.split('.')[-1] if '.' in url else 'txt'
                    file_name = f"file_{idx + 1}.{file_extension}"

                    # 將文件寫入 ZIP
                    zip_file.writestr(file_name, response.content)
                    
                except Exception as e:
                    st.error(f"下載 {url} 時發生錯誤：{e}")

        # 將 ZIP 文件的指針移到開始位置
        zip_buffer.seek(0)

        # 在 Streamlit 中提供下載按鈕
        st.download_button(
            label="下載所有文件",
            data=zip_buffer,
            file_name="downloaded_files.zip",
            mime="application/zip"
        )
    
    else:
        st.error("資料中沒有 'DailyMeanTemperature_AllYear_url' 列。")