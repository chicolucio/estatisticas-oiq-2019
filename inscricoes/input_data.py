# coding: utf-8

import pandas as pd

def input_data(file_path):
    """Gera um Pandas DF a partir de um arquivo csv
    :type file_path: string
    """
    df = pd.read_csv(file_path)
    return df


def time_index(df, column_name):
    """Converte a coluna fornecida (string) para formato data/hora do Pandas
    :type column_name: string
    :param column_name: Nome da coluna no Pandas dataframe
    :type df: pandas dataframe
    """
    df[column_name] = pd.to_datetime(df[column_name], utc=True)
    df.index = pd.DatetimeIndex(df[column_name].dt.tz_localize(None))
    df.drop([column_name], axis=1, inplace=True)
    return df


def no_duplicates(df, column_name):
    """Remove duplicatas encontradas na coluna fornecida
    :type column_name: string
    :param column_name: Nome da coluna no Pandas dataframe
    :type df: pandas dataframe
    """
    return df.drop_duplicates(subset=[column_name])


def count_date(df, column_name, count_name="Contagem", from_date=''):
    """Conta número de ocorrências iguais na coluna fornecida. Retorna
    tabela, com coluna nomeada'Contagem'."""

    count_df = pd.DataFrame(df[column_name].rename(
        count_name).groupby(pd.Grouper(freq='D')).count())

    if from_date != '':
        count_df = count_df.loc[count_df.index > from_date]

    return count_df


def count_date_interval(df,
                        column_name,
                        count_name="Contagem",
                        from_date='',
                        to_date=''):
    """Conta número de ocorrências iguais na coluna fornecida. Retorna
    tabela, com coluna nomeada'Contagem'."""

    count_df = pd.DataFrame(df[column_name].rename(
        count_name).groupby(pd.Grouper(freq='D')).count())

    if from_date != '':
        # count_df = count_df.loc[from_date:to_date]
        count_df = count_df[(count_df.index > from_date) &
                            (count_df.index <= to_date)]

    return count_df


def pivot_tables(df, values, index, column, margins_name='Total'):
    """Gera tabela dinâmica Pandas de acordo com os dados passados"""
    pivot_df = pd.pivot_table(df, values=values, index=index, columns=column,
                              aggfunc=pd.Series.nunique, margins=True,
                              margins_name=margins_name)
    return pivot_df.fillna(0)


def latex(df):
    """Converte o DF fornecido para tabela LaTeX"""
    return print(df.to_latex())


def pivot_data(df, column):
    """Extrai dados de uma dada coluna (contagem de 0) de uma pivot table,
    excluindo a linha de total"""
    rows = df.shape[0]
    return df.iloc[:rows - 1, column]


def pivot_index(df):
    """Extrai os indexadores de uma pivot table, exlcuindo a linha de total"""
    rows = df.shape[0]
    return df.index[:rows - 1]


def pivot_total(df):
    """Extrai os totais por coluna de uma pivot table. Retorna valores e labels"""
    rows = df.shape[0]
    columns = df.shape[1]
    values = df.iloc[rows - 1, :columns - 1]
    labels = df.columns[:columns - 1]
    return values, labels
