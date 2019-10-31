import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
from pandas.plotting import register_matplotlib_converters

# necessário de acordo com um futureWarning do Pandas quando lida com datas em eixos
register_matplotlib_converters()


def plot_param_date(ax=None):
    """Parâmetros para o plot de inscrições por data"""
    linewidth = 1
    fontsize = 14
    angle = 30

    ax.grid(b=True, which='major', linestyle='--', linewidth=linewidth)
    ax.grid(b=True, which='minor', axis='x',
            linestyle='-.', linewidth=linewidth)
    ax.tick_params(which='both', labelsize=fontsize)
    plt.xticks(rotation=angle)


def plot_date(dates, count, labels, deadlines, names, ax=None):
    """Plot de inscrições por data.
    :type names: lista de strings
    :param names: nome na legenda do gráfico.
    :type deadlines: list
    :param deadlines: lista com deadlines em strings na forma yyyy-mm-dd
    :type count: lista de pandas dataframes
    :param count: contagem de inscrições por data
    :type dates: pandas series
    :param dates: série de dados em formato de data
    :type labels: lista ['x', 'y', 'title']
    """
    plot_param_date(ax)

    linewidth = 3
    fontsize = 15

    for i in range(len(count)):
        ax.plot(dates, count[i], linewidth=linewidth, label=names[i])

    myFmt = mdates.DateFormatter("%d-%m")

    ax.set_xlabel(labels[0], size=fontsize)
    ax.set_ylabel(labels[1], size=fontsize)
    ax.set_title(labels[2], size=fontsize + 3)

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=2, interval=1))
    ax.xaxis.set_major_formatter(myFmt)
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    colors = ['red', 'green', 'blue', 'purple']

    for date in range(len(deadlines)):
        ax.axvline(x=deadlines[date],
                   zorder=2,
                   color=colors[date],
                   label='{0}° deadline'.format(date + 1),
                   linestyle='--', linewidth=linewidth - 1)

    ax.legend(fontsize=fontsize, loc='upper left', bbox_to_anchor=(1, 1))
    # plt.show()


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
