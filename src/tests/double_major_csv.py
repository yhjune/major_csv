import tabula
import pandas as pd
import numpy as np

root = '/Users/yhjune/Desktop/playground/pdf/'
dm_pdf_path = root+'major_origin/스크랜튼대학/복수전공_뇌인지과학부.pdf'
dm_csv_name = dm_pdf_path.split('/')[-1].split('.')[0]+".csv"
dm_condi_name = "S_condi_"+dm_csv_name.split("_")[-1]
output_path = root+'/'

msg = "double major"
    
df = tabula.read_pdf(dm_pdf_path, pages="all",lattice=True, area=[163.5, 13,802.1,580.5]) # read pdf (head include)
df_concat = pd.concat(df, ignore_index=True).dropna(thresh=4) # concat dataframe, drop rows na < 4 

if len(df_concat.columns)==13:
        df_concat.columns = ["구분","_id","교과목명","이수권장학년","설정학기","시간","학점","필수여부","학사편입생제외여부","개설학과","2023학년2학기개설여부","비고","교과과정안내"] # colums name
else: df_concat.columns = ["구분","_id","교과목명","이수권장학년","설정학기","시간","학점","필수여부","학사편입생제외여부","개설학과","2023학년2학기개설여부","비고"]
    
df_concat = df_concat.drop(columns='학사편입생제외여부') # colum's details
df_concat.replace(r'\r','', regex=True, inplace=True)
df_concat["구분"] = df_concat["구분"].ffill()
df_concat["영역"] = df_concat['_id'].astype(str).replace(r'\d+',np.nan,regex=True).ffill().replace(r'[^A-Za-z0-9ㄱ-ㅎㅏ-ㅣ가-핳]','',regex=True)
df_concat["이수권장학년"] = df_concat["이수권장학년"].fillna(0).replace('계절',5).astype(int)

print(df_concat["설정학기"].dtype)
df_concat["설정학기"] = df_concat["설정학기"].astype(str).str.split(',')

df_concat = df_concat[["_id","구분","영역","교과목명","이수권장학년","설정학기","시간","학점","필수여부","개설학과","2023학년2학기개설여부","비고"]] # colum order

df_list = df_concat.dropna(subset=["시간"]).reset_index(drop=True) # 복수 전공 이수 과목 목록
df_list.to_csv(output_path+dm_csv_name, mode="w") # export csv

df_condi = df_concat[df_concat["교과목명"].notnull() & df_concat["교과목명"].str.contains("이수")].drop(columns=["구분","이수권장학년","설정학기","시간","학점","개설학과","2023학년2학기개설여부","영역"]).replace(r'[^A-Za-z0-9ㄱ-ㅎㅏ-ㅣ가-후]+','',regex=True).reset_index(drop=True)
df_condi.columns = ["_id","이수조건","필수여부","비고"] # 복수전공 이수 조건 
df_condi.to_csv(output_path+dm_condi_name, mode="w") # export csv
print(msg+': '+dm_csv_name)