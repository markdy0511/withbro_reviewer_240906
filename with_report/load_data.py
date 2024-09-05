import pandas as pd

# 파일 입력기
def load(file):
    if file is not None:
        try:
            try:
                data = pd.read_csv(file)
            except:
                data = pd.read_excel(file)
        except:
            try:
                data = pd.read_csv(file, encoding='cp949')
            except:
                data = pd.read_excel(file, encoding='cp949')
        return data
    return None