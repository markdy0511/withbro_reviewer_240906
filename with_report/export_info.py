from datetime import datetime, timedelta 
import pandas as pd

# 주차 계산기
def get_week_info(date, start_weekday):

    if isinstance(date, pd.Timestamp):
        date = date.to_pydatetime()
        date = date.date()
    # Define the start of the week (0 = Monday, 6 = Sunday)
    weekday_dict = {"월요일": 0, "일요일": 6}
    start_weekday_num = weekday_dict[start_weekday]
    # Calculate the start of the week for the given date
    start_of_week = date - timedelta(days=(date.weekday() - start_weekday_num) % 7)

    # Get the month and the week number
    month = start_of_week.month
    start_of_month = datetime(start_of_week.year, month, 1).date()
    week_number = ((start_of_week - start_of_month).days // 7) + 1
    
    # Get the month name in Korean for output
    month_dict_kr = {
        1: "1월", 2: "2월", 3: "3월", 4: "4월", 5: "5월", 6: "6월", 
        7: "7월", 8: "8월", 9: "9월", 10: "10월", 11: "11월", 12: "12월"
    }
    month_name_kr = month_dict_kr[month]
    
    return str(month_name_kr)+" "+str(week_number)+"주"

# 월 계산기
def get_month_info(date):
    return date.month

def get_group_kwr(analysis_period):
    #기간 그룹핑용
    if analysis_period == "일간":
        return "일자"
    elif analysis_period == "주간":
        return "주"
    else:
        return "월"