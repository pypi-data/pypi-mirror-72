#!/usr/bin/env python3

def search(df, dataframe_col, tok = ''):
    """
    This functions converts the dataframe column to a list for faster searching.

    :param df:
    :param dataframe_col:
    :param tok:
    :return:
    """
    df = df[df.index.notnull()]
    listed = df[dataframe_col].to_list()
    df['search_flag'] = [tok in str(i) for i in listed]
    return df[df.search_flag==True][dataframe_col].to_frame()


if __name__ == "__main__":
    pass