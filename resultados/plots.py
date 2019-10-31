import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import numpy as np


def histogram(df, df_column, binwidth=10, including=10,
              ultima_medalha=3, ultima_mencao=10, ax=None):
    """Gera histograma com os dados de notas, com linhas destacando
    a zona de medalhistas e a zona de menções honrosas"""
    bins = np.arange(including, 101, binwidth)
    xmax = np.floor(df[df_column].max() + binwidth / 2)

    n = ax.hist(df[df_column], bins, align='mid', facecolor='g',
                alpha=0.6, edgecolor='k', label='')

    ax.set_xticks(np.arange(0, 101, 5))
    ax.set_xlim(including, xmax + binwidth / 2)
    ax.set_ylim(0, n[0].max())
    ax.set_yticks(np.arange(0, n[0].max() + 1, 1))
    ax.set_axisbelow(True)
    ax.grid(b=True, which='major', linestyle=':', linewidth=1.0)
    ax.tick_params(which='both', labelsize=14)

    ax.axvline(x=df[df_column].median(), color='blue', zorder=2, label='Mediana ({0:0})'.format(
        df[df_column].median()), linewidth=2, linestyle='--')
    ax.axvline(x=df[df_column].mean(), color='orange', zorder=2, label='Média ({0:0.1f})'.format(
        df[df_column].mean()), linewidth=2, linestyle='--')

    ax.axvline(x=df.loc[ultima_mencao, df_column], color='red', zorder=2, label='Menções honrosas ({0:0})'.format(
        df.loc[ultima_mencao, df_column]), linewidth=2, linestyle='--')
    ax.axvline(x=df.loc[ultima_medalha, df_column], color='purple', zorder=2, label='Medalhas ({0:0})'.format(
        df.loc[ultima_medalha, df_column]), linewidth=2, linestyle='--')

    ax.set_xlabel('Notas', size=15)
    ax.set_ylabel('Frequência', size=15)

    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, fontsize=12,
              loc='upper left', bbox_to_anchor=(0.85, 1))

    return


def boxplot(df, df_column, ax=None):
    """Gera boxplot com os dados de notas"""
    flierprops = dict(markerfacecolor='c', marker='o', markersize=10)
    meanlineprops = dict(linestyle='--', linewidth=2, color='orange')
    medianprops = dict(linestyle='--', linewidth=2, color='blue')

    ax.boxplot(df[df_column], vert=False, meanline=True, showmeans=True,
               notch=False, labels=[''], flierprops=flierprops,
               meanprops=meanlineprops, medianprops=medianprops, widths=0.95,
               patch_artist=True, boxprops=dict(facecolor='c', alpha=0.5))

    ax.yaxis.set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.grid(b=True, which='major', linestyle=':', linewidth=1.0)

# TODO: integrar legenda boxplot com histogram para quando houver outliers no boxplot


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct


def plot_pizza(values, labels, title, ax=None):
    """Padrão para gráficos em pizza
    :type title: string
    :param title: Título do gráfico
    :type labels: pandas dataframe column
    :param labels: labels para o gráfico
    :type values: pandas dataframe column
    """

    distance = 0.675
    angle = 90
    fontsize = 14
    color = 'white'

    patches, texts, autotexts = ax.pie(values, shadow=True,
                                       startangle=angle,
                                       autopct=make_autopct(values),
                                       pctdistance=distance)
    [i.set_fontsize(fontsize) for i in texts]
    [i.set_fontsize(fontsize - 1) for i in autotexts]
    [i.set_color(color) for i in autotexts]
    [i.set_weight('bold') for i in autotexts]

    ax.axis("equal")
    ax.set_title(title, size=fontsize + 4)
    ax.legend(patches, labels, fontsize=fontsize, bbox_to_anchor=(0.75, 1),
              loc='upper left')
