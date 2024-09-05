def comparing_df(df, period_set):

    try:
        df.loc['변화량'] = df.diff().iloc[1]
        df.loc['증감율'] = df.apply(lambda x: ((x[period_set["now"]] - x[period_set["pre"]]) / x[period_set["pre"]]) * 100 if x[period_set["pre"]] != 0 else 0, axis=0)

        return df
    except:
        return df