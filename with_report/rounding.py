def round_two_axis(df, row_index, col_name, period_set):

    # 특정 열에 대해 round 2 적용
    df[col_name] = df[col_name].round(2)

    # 특정 행에 대해 round 2 적용
    #df.loc[row_index] = df.loc[row_index].round(2)

    # 그 행과 열이 포함되지 않은 나머지에 대해 round 0 적용
    for i in df.index:
        for j in df.columns:
            if i != row_index and j != col_name:
                df.at[i, j] = round(df.at[i, j], 0)
            if i == '증감율':
                df.at[i, j] = round(df.at[i, j], 2)

    df.loc['변화량'] = df.loc[period_set["now"]] - df.loc[period_set["pre"]]

    return df

def round_multi_axis(df, row_index, col_list, period_set):

    # 특정 열에 대해 round 2 적용
    for col_name in col_list:
        df[col_name] = df[col_name].round(2)

    # 특정 행에 대해 round 2 적용
    #df.loc[row_index] = df.loc[row_index].round(2)

    # 그 행과 열이 포함되지 않은 나머지에 대해 round 0 적용
    for i in df.index:
        for j in df.columns:
            if i != row_index and j not in col_list:
                df.at[i, j] = round(df.at[i, j], 0)
            if i == '증감율':
                df.at[i, j] = round(df.at[i, j], 2)

    df.loc['변화량'] = df.loc[period_set["now"]] - df.loc[period_set["pre"]]

    return df


def round_col_axis(df, col_name):

    # 특정 열에 대해 round 2 적용
    df[col_name] = df[col_name].round(2)

    # 특정 행에 대해 round 2 적용
    #df.loc[row_index] = df.loc[row_index].round(2)

    # 그 행과 열이 포함되지 않은 나머지에 대해 round 0 적용
    for i in df.index:
        for j in df.columns:
            if j != col_name:
                try:
                    df.at[i, j] = round(df.at[i, j], 0)
                except:
                    pass

    return df