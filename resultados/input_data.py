# coding: utf-8

import pandas as pd
import numpy as np


def input_data(file_path):
    """Gera um Pandas DF a partir de um arquivo csv.

    Parameters
    ----------
    file_path : type string
        Caminho do arquivo.

    Returns
    -------
    type
        Pandas DataFrame. NaN substituído por 0

    """
    df = pd.read_csv(file_path)
    return df.fillna(0)


def no_absents(df):
    """Elimina alunos faltosos. No caso, considerou-se que faltaram os alunos
    que estavam com todas as notas zeradas (coluna 2 em diante). Funciona pois
    nenhum aluno presente zerou a prova. Caso isso algum dia aconteça, vai
    falhar. Talvez adotar um sistema de coluna de flag para indicar presença.

    Parameters
    ----------
    df : type Pandas DataFrame.
        DataFrame que será tratado.

    Returns
    -------
    type
        DataFrame sem alunos faltosos.

    """
    columns = df.columns[2:]
    index_values = df[(df[columns] == 0).all(axis=1)].index
    return df.drop(index_values).reset_index(drop=True)


def grades(df):
    """Calcula a pontuação da prova considerando objetivas e discursivas.

    Parameters
    ----------
    df : type Pandas DataFrame
        DataFrame de início.

    Returns
    -------
    type Pandas DataFrame
        DataFrame com as colunas de pontuação.

    """
    df['Pontos - Objetiva'] = df.iloc[:, 2] * 5
    df['Pontos - Discursiva'] = df.iloc[:, 3] + df.iloc[:, 4]
    df['Pontuação final'] = df['Pontos - Objetiva'] + df['Pontos - Discursiva']
    return df


def awards(df, head=10):
    """Ordena DataFrame de acordo com a nota final. Desempate na discursiva.

    Parameters
    ----------
    df : type Pandas DataFrame
        DataFrame de início.
    head : type integer
        Número de linhas que será exibido (padrão é 10 pois costuma-se premiar
        os 10 primeiros - 3 medalhas e 7 menções honrosas).

    Returns
    -------
    type Pandas DataFrame
        DataFrame de saída.

    """
    df = df.sort_values(['Pontuação final', 'Pontos - Discursiva'],
                        ascending=False).head(head).reset_index(drop=True)
    df.index = df.index + 1     # para facilitar, numerando a partir de 1
    return df


def bins(df):
    """Segrega os dados de notas de 10 em 10 pontos para construção de gráficos.

    Parameters
    ----------
    df : type Pandas DataFrame
        DataFrame de início.

    Returns
    -------
    type Pandas DataFrame
        DataFrame final.

    """
    df_bins = pd.DataFrame(df['ALUNO'].rename('Contagem').groupby(pd.cut(
        df['Pontuação final'].rename('Intervalos'), np.arange(0, 101, 10), right=False)).count())

    df_bins['Contagem /%'] = round(100 * df_bins['Contagem'] /
                                   df_bins['Contagem'].sum(), 2)
    df_bins['Contagem cumulativa'] = df_bins['Contagem'].cumsum()
    df_bins['Contagem /% cumulativa'] = df_bins['Contagem /%'].cumsum()

    return df_bins


def latex(df):
    """Converte DataFrame em tabela para LaTeX.

    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame de início.

    Returns
    -------
    type None
        Comando print para apresentar tabela em LaTeX que pode ser copiada.

    """
    return print(df.to_latex())


def pivot_tables(df, values, index, column, margins_name='Total'):
    """Gera tabela dinâmica Pandas de acordo com os dados passados"""
    pivot_df = pd.pivot_table(df, values=values, index=index, columns=column,
                              aggfunc=pd.Series.nunique, margins=True,
                              margins_name=margins_name)
    return pivot_df.fillna(0)


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


def stats_table(df):
    """Gera tabela com resumo dos dados estatíticos"""
    df.loc['IQR'] = df.loc['75%'] - df.loc['25%']
    df = df.T.drop(['Acertos parte A'])
    df = df.drop(['count'], axis=1)
    df = df.reindex(['Pontos - Objetiva',
                     'Q17',
                     'Q18',
                     'Pontos - Discursiva',
                     'Pontuação final'])
    df['mean'] = round(df['mean'], 2)
    df['std'] = round(df['std'], 2)
    return df


def semester(df_row):
    """Retorna o perído do aluno de acordo com o código da turma"""
    number = df_row[1]
    return '{0}º período'.format(number)


def semester_shift(df):
    """Retorna DF com o turno e o período do aluno de acordo com o código da turma"""
    df[['cod', 'num']] = df['TURMA'].str.split(
        '(\d+)', expand=True).drop(2, axis=1)

    df['Período'] = df.loc[:, 'num'].apply(semester)

    df['Turno'] = np.where(df['num'].str[0] == '1', 'Manhã',
                           np.where(df['num'].str[0] == '2', 'Tarde', 'Noite'))

    return df
