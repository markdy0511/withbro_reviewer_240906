import pandas as pd
import streamlit as st

def grouped_media(df, metric_set, group_period):            
    target_list_media = metric_set["inflow_metric"] + metric_set["trans_metric"]

    df_no_index = df.reset_index(drop=True)

    result = {}
    for idx, row in df_no_index.iterrows(): #group by

        category = row[group_period]
        
        if category not in result:
            result[category] = {col: 0 for col in target_list_media}
        
        for col in target_list_media:
            result[category][col] += row[col]
    
    grouped_df = pd.DataFrame(result).T
    grouped_df.index.name = group_period

    return grouped_df

def grouped_ga(df, metric_set, group_period):            
    target_list_ga = metric_set["trans_ga_metric"]

    df_no_index = df.reset_index(drop=True)

    result = {}
    for idx, row in df_no_index.iterrows(): #group by
        category = row[group_period]
        
        if category not in result:
            result[category] = {col: 0 for col in target_list_ga}
        
        for col in target_list_ga:
            result[category][col] += row[col]
    
    grouped_df = pd.DataFrame(result).T
    grouped_df.index.name = group_period

    return grouped_df

def grouped_media_with(df, col_name, metric_set, group_period):            
    target_list_media = metric_set["inflow_metric"] + metric_set["trans_metric"]

    df_no_index = df.reset_index(drop=True)

    result = {}
    for idx, row in df_no_index.iterrows(): #group by

        key = (row[col_name], row[group_period])

        if key not in result:
            result[key] = {col: 0 for col in target_list_media}
        
        for col in target_list_media:
            result[key][col] += row[col]
    
    grouped_df = pd.DataFrame(result).T
    #st.write(grouped_df)
    #print(col_name, group_period)
    grouped_df.index.names = [col_name, group_period]
    

    return grouped_df

def grouped_ga_with(df, col_name, metric_set, group_period):            
    if df.empty:
        # Create an empty DataFrame with the expected columns
        target_list_ga = metric_set["trans_ga_metric"]
        empty_df = pd.DataFrame(columns=[col_name, group_period] + target_list_ga)
        empty_df.set_index([col_name, group_period], inplace=True)
        return empty_df
    
    target_list_ga = metric_set["trans_ga_metric"]

    df_no_index = df.reset_index(drop=True)

    result = {}
    for idx, row in df_no_index.iterrows(): #group by
        key = (row[col_name], row[group_period])
        
        if key not in result:
            result[key] = {col: 0 for col in target_list_ga}
        
        for col in target_list_ga:
            result[key][col] += row[col]
    
    grouped_df = pd.DataFrame(result).T
    grouped_df.index.names = [col_name, group_period]

    return grouped_df

def grouped_media_kwrd(df, metric_set, group_period):            
    target_list_media = metric_set["inflow_metric"] + metric_set["trans_metric"]

    df_no_index = df.reset_index(drop=True)

    result = {}
    for idx, row in df_no_index.iterrows(): #group by

        key = (row['매체'],row['캠페인'],row['광고그룹'], row['소재명/키워드'], row[group_period])

        if key not in result:
            result[key] = {col: 0 for col in target_list_media}
        
        for col in target_list_media:
            result[key][col] += row[col]
    
    grouped_df = pd.DataFrame(result).T
    #st.write(grouped_df)
    #print(col_name, group_period)
    grouped_df.index.names = ['매체','캠페인','광고그룹','소재명/키워드', group_period]
    

    return grouped_df

def grouped_ga_kwrd(df, metric_set, group_period):            
    if df.empty:
        # Create an empty DataFrame with the expected columns
        target_list_ga = metric_set["trans_ga_metric"]
        empty_df = pd.DataFrame(columns=['매체','캠페인','광고그룹','소재명/키워드', group_period] + target_list_ga)
        empty_df.set_index(['매체','캠페인','광고그룹','소재명/키워드', group_period], inplace=True)
        return empty_df
    
    target_list_ga = metric_set["trans_ga_metric"]

    df_no_index = df.reset_index(drop=True)

    result = {}
    for idx, row in df_no_index.iterrows(): #group by
        key = (row['매체'],row['캠페인'],row['광고그룹'], row['소재명/키워드'], row[group_period])
        
        if key not in result:
            result[key] = {col: 0 for col in target_list_ga}
        
        for col in target_list_ga:
            result[key][col] += row[col]
    
    grouped_df = pd.DataFrame(result).T
    grouped_df.index.names = ['매체','캠페인','광고그룹','소재명/키워드', group_period]

    return grouped_df