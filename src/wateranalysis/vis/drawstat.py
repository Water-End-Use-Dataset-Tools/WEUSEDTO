import pandas as pd
import matplotlib.pyplot as plt
import calendar
import seaborn as sns
import datetime as dt


def liters_distribution(df):
    plt.figure()
    plt.hist(df, color='blue', edgecolor='black',
             bins=int(50))
    sns.distplot(df, hist=True, kde=True,
                 bins=int(50), color='blue',
                 hist_kws={'edgecolor': 'black'})
    plt.show()

def mliters_distribution(dfs, names):
    plt.figure()
    plt.hist(dfs, edgecolor='black',   bins=int(50), density=True, label=names)
    plt.xlabel("liters")
    plt.ylabel("number of usages")
    plt.legend()
    plt.show()


# how many liters per day on each month
def wday_usage_bars(df):

    d_names = list(calendar.day_name)
    plt.figure()
    wday_usage = df.groupby('day_week')['count'].mean()
    d_axis = pd.Series({x: d_names[x] for x in wday_usage.index})
    plt.bar(d_axis.values, wday_usage.values)
    plt.show()


def hour_usage_month(df, fixture):
    m_names = list(calendar.month_abbr)
    plt.figure()
    available_months = df["month"].unique()
    for month in available_months:
        df_month = df[df["month"] == month]
        usages = df_month.groupby("hour")["month"].count()
        plt.plot(usages.index.values, usages.values, label=m_names[month])
    plt.xlabel("hour")
    plt.ylabel("number of usages")
    plt.title(fixture)
    plt.legend()
    plt.show()


def day_usage_month(df):
    d_names = list(calendar.day_name)
    m_names = list(calendar.month_abbr)
    plt.figure()
    available_months = df["month"].unique()
    for month in available_months:
        df_month = df[df["month"] == month]
        usages = df_month.groupby("day")["month"].count()
        plt.plot(usages.index, usages.values, label=m_names[month])
    plt.xticks(list(range(len(d_names))), d_names)
    plt.legend()
    plt.show()

def correlations(df, title):

    plt.figure()
    plt.title(title)
    ax = plt.subplot(3, 2, 1)
    ax.scatter(df["hour"], df["liters"]/1000)
    plt.xlabel("hour of day")
    plt.ylabel("liters")

    ax = plt.subplot(3, 2, 2)
    ax.scatter(df["duration"], df["liters"]/1000)
    plt.xlabel("duration")
    plt.ylabel("liters")

    ax = plt.subplot(3, 2, 3)
    z = []
    for x in df["datetime"]:
        z.append(dt.datetime.fromtimestamp(x).weekday())
    df["day_week"] = z
    ax.scatter(df["hour"], df["day_week"])
    plt.xlabel("hour of day")
    plt.ylabel("day of week")

    ax = plt.subplot(3, 2, 4)
    ax.scatter(df["day_week"], df["duration"])
    plt.xlabel("day of week")
    plt.ylabel("duration")

    ax = plt.subplot(3, 2, 5)
    temp = df.groupby("hour")["duration"].count()
    ax.scatter(temp.index.values, temp.values)
    plt.xlabel("hour")
    plt.ylabel("usages")

    ax = plt.subplot(3, 2, 6)
    temp = df.groupby("day_week")["duration"].count()
    ax.scatter(temp.index.values, temp.values)
    plt.xlabel("day of week")
    plt.ylabel("usages")
    plt.show()