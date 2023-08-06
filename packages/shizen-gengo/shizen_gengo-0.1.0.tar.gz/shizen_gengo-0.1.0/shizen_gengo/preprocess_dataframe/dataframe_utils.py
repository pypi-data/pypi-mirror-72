#!/usr/bin/env python3

def rename_col(df_column_names, before, after):
    """

    :param df_column_names:
    :param before:
    :param after:
    :return:
    """
    return map(lambda x: str.replace(x, before, after), df_column_names)

if __name__ == "__main__":
    pass