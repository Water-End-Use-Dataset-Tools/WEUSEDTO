"""
timeseries.statistics
=======================================
This module define  models for describing  statistically the frequency of fixture usage.
"""

import json
import pandas as pd
import logging


class GlobalUsage:
    """
    This class define  a statistical distribution that is the same each day of the year.
    It define the probability distribution that a person open the fixture n times, the probability that that usage
    happens at a certain hour, the average duration and the average number of liters  of a usage.
    """
    daily_usage = None
    time_distribution = None
    average_secs = 0
    average_liters = 0

    def __init__(self, df, df1, df2):
        """
        The constructor needs three parameters.
        :param df: the number of usage per day of the year
        :param df1: the original time-series of measured water flow
        :param df2: the list of usage vectors
        """
        self.df = df
        self.df1 = df1
        self.df2 = df2
        self.average_secs = 0
        self.average_liters = 0

    def compute_frequency(self):
        """
        Tis method compute the ratio between the number of days with n  usages and the total number of days
        :return: an array that contains this ratio for each  n value (according to the actual occurred usages)
        """
        utilizzi_max = self.df['utilizzi'].max()
        nr = len(self.df)

        daily_usage = {}
        for i in range(0, utilizzi_max + 1):
            df1 = self.df[self.df['utilizzi'] == i]
            nr1 = len(df1.index)
            temp = round(nr1 / nr, 2)
            daily_usage[i] = temp
            self.daily_usage = daily_usage
        return daily_usage

    def compute_times(self):
        """
        This method compute the ratio between the number of usages occured at a certain hour and the total
        number of occurrences.
        :return: an array with such ration for each hour of the day
        """
        self.df1['tempo'] = pd.to_datetime(self.df1['tempo'].astype(int), unit='s')

        cont = 0
        vet_conteggi = []
        fascia_oraria = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10',
                         '10-11',
                         '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21',
                         '21-22',
                         '22-23', '23-00']
        for i in range(0, 24):  # ORE
            if i < 23:
                df2 = self.df1[(self.df1['tempo'].dt.hour >= i) & (self.df1['tempo'].dt.hour < i + 1)]
            elif i == 23:
                df2 = self.df1[self.df1['tempo'].dt.hour >= i]
            nr1, nc1 = df2.shape
            for elemento in range(0, nr1):
                if (self.df1.iloc[elemento, 1] == 0) and (self.df1.iloc[elemento + 1, 1] != 0):
                    cont += 1
            vet_conteggi.append(cont)
            cont = 0
        data = {'fascia oraria': fascia_oraria,
                '#utilizzi': vet_conteggi}
        df3 = pd.DataFrame(data)

        dim = len(df3)
        num_utilizzi = df3['#utilizzi'].sum()
        time_distribution = []
        for j in range(0, dim):
            temp = df3.iloc[j, 1] / num_utilizzi
            time_distribution.append(temp)
            self.time_distribution = time_distribution
        return time_distribution

    def compute_average(self):
        """
        Compute the average duration and the average amount of consumed water per usage
        :return: average duration, average consumption
        """
        dim = len(self.df2)
        # Calcolo durata media
        average_secs = (self.df2['durata_utilizzo'].sum()) / dim
        # Calcolo media consumi
        average_liters = (self.df2['litri'].sum()) / dim

        self.average_secs = average_secs
        self.average_liters = average_liters
        return self.average_secs, self.average_liters


class MonthlyUsage:
    """
    This class define  a statistical distribution that is the same each day of a specific month.
    It define the probability distribution that a person open the fixture n times in a day of a month,
    the probability that that usage  occurs at a certain hour,
    the average duration and the average number of liters  of a usage in a dey of specific month.
    """
    daily_usage = None
    time_distribution = None
    average_secs = 0
    average_liters = 0

    def __init__(self, df, df1, df2, month):
        """
        The constructor needs three parameters.

        :param df: The number of usages per each day of the year
        :param df1: The original timeseries of  water flow measures
        :param df2: The timeseries with vector of properties of each usage
        :param month: The month we want to model
        """
        self.df = df
        self.df1 = df1
        self.df2 = df2
        self.average_secs = 0
        self.average_liters = 0
        self.month = month

    def compute_frequency(self):
        """
        Tis method compute the ratio between the number of days with n  usages and the total number of days
        :return: an array that contains this ratio for each  n value (according to the actual occurred usages)
        """
        self.df = self.df[self.df['mese'] == self.month]
        utilizzi_max = self.df['utilizzi'].max()
        utilizzi_totali = self.df['utilizzi'].sum()
        nr = len(self.df)

        daily_usage = {}
        for i in range(0, utilizzi_max + 1):
            df1 = self.df[self.df['utilizzi'] == i]
            nr1 = len(df1.index)
            temp = round(nr1 / nr, 2)
            daily_usage[i] = temp
            self.daily_usage = daily_usage
        return daily_usage

    def compute_times(self):
        """
        This method compute the ratio between the number of usages occured at a certain hour and the total
        number of occurrences.
        :return: an array with such ration for each hour of the day
        """
        self.df1['tempo'] = pd.to_datetime(self.df1['tempo'], unit='s')
        self.df1 = self.df1[self.df1['tempo'].dt.month == self.month]
        cont = 0
        vet_conteggi = []
        fascia_oraria = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10',
                         '10-11',
                         '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21',
                         '21-22',
                         '22-23', '23-00']
        for i in range(0, 24):  # ORE
            if i < 23:
                df2 = self.df1[(self.df1['tempo'].dt.hour >= i) & (self.df1['tempo'].dt.hour < i + 1)]
            elif i == 23:
                df2 = self.df1[self.df1['tempo'].dt.hour >= i]
            for elemento in range(0, len(df2)-1):
                if (df2.iloc[elemento, 1] == 0) and (df2.iloc[elemento + 1, 1] != 0):
                    cont += 1
            vet_conteggi.append(cont)
            cont = 0
        data = {'fascia oraria': fascia_oraria,
                '#utilizzi': vet_conteggi}
        df3 = pd.DataFrame(data)

        dim = len(df3)
        num_utilizzi = df3['#utilizzi'].sum()
        time_distribution = []
        for j in range(0, dim):
            temp = df3.iloc[j, 1] / num_utilizzi
            time_distribution.append(temp)
            self.time_distribution = time_distribution
        return time_distribution

    def compute_average(self):
        """
        Compute the average duration and the average amount of consumed water per usage in a day of a specific month
        :return: average duration, average consumption
        """
        df1 = self.df2[self.df2['mese'] == self.month]
        dim = len(df1)
        # Calcoliamo durata media
        average_secs = (df1['durata_utilizzo'].sum()) / dim
        # Calcoliamo media consumi
        average_liters = (df1['litri'].sum()) / dim

        self.average_secs = average_secs
        self.average_liters = average_liters
        return self.average_secs, average_liters


class WeeklyUsage:
    """
        This class define  a statistical distribution of fixture usage a specific week-day.
        It define the probability distribution that a person open the fixture n times in a day of the week,
        the probability that that usage  occurs at a certain hour,
        the average duration and the average number of liters  of a usage in a dey of specific day-week.
    """
    daily_usage = None
    time_distribution = None
    average_secs = 0
    average_liters = 0

    def __init__(self, df, df1, df2, day_week):
        """
        The constructor needs three parameters.
         :param df: The number of usages per each day of the year
        :param df1: The original timeseries of  water flow measures
        :param df2: The timeseries with vector of properties of each usage
        :param day_week: the day of the week [0-6]
        """
        self.df = df
        self.df1 = df1
        self.df2 = df2
        self.average_secs = 0
        self.average_liters = 0
        self.day_week = day_week

    def compute_frequency(self):
        """
        Tis method compute the ratio between the number of days with n  usages and the total number of days
        :return: an array that contains this ratio for each  n value (according to the actual occurred usages)
        """
        self.df = self.df[self.df['day_week'] == self.day_week]
        utilizzi_max = self.df['utilizzi'].max()
        nr = len(self.df)

        daily_usage = {}
        for i in range(0, utilizzi_max + 1):
            df1 = self.df[self.df['utilizzi'] == i]
            nr1 = len(df1.index)
            #    print(nr1)
            temp = round(nr1 / nr, 2)
            daily_usage[i] = temp
            self.daily_usage = daily_usage
        return daily_usage

    def compute_times(self):
        """
        This method compute the ratio between the number of usages occured at a certain hour and the total
        number of occurrences.
        :return: an array with such ration for each hour of the day
        """
        self.df1['tempo'] = pd.to_datetime(self.df1['tempo'], unit='s')
        self.df1['giorno'] = self.df1['tempo'].dt.day_name()

        self.df1['giorno'].replace('Monday', 0, inplace=True)
        self.df1['giorno'].replace('Tuesday', 1, inplace=True)
        self.df1['giorno'].replace('Wednesday', 2, inplace=True)
        self.df1['giorno'].replace('Thursday', 3, inplace=True)
        self.df1['giorno'].replace('Friday', 4, inplace=True)
        self.df1['giorno'].replace('Saturday', 5, inplace=True)
        self.df1['giorno'].replace('Sunday', 6, inplace=True)

        self.df1 = self.df1[self.df1['giorno'] == self.day_week]

        cont = 0
        vet_conteggi = []
        fascia_oraria = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10',
                         '10-11',
                         '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21',
                         '21-22',
                         '22-23', '23-00']
        for i in range(0, 24):  # ORE
            if i < 23:
                df2 = self.df1[(self.df1['tempo'].dt.hour >= i) & (self.df1['tempo'].dt.hour < i + 1)]
            elif i == 23:
                df2 = self.df1[self.df1['tempo'].dt.hour >= i]
            #  nr1, nc1 = df2.shape
            for elemento in range(0, len(df2)-1):
                if (df2.iloc[elemento, 1] == 0) and (df2.iloc[elemento + 1, 1] != 0):
                    cont += 1
            vet_conteggi.append(cont)
            cont = 0
        data = {'fascia oraria': fascia_oraria,
                '#utilizzi': vet_conteggi}
        df3 = pd.DataFrame(data)

        dim = len(df3)
        num_utilizzi = df3['#utilizzi'].sum()
        time_distribution = []
        for j in range(0, dim):
            temp = df3.iloc[j, 1] / num_utilizzi
            time_distribution.append(temp)
            self.time_distribution = time_distribution
        return time_distribution

    def compute_average(self):
        """
        Compute the average duration and the average amount of consumed water per usage in a day of a specific month
        :return: average duration, average consumption
        """
        df1 = self.df2[self.df2['giorno'] == self.day_week]
        dim = len(df1)
        average_secs = 0
        average_liters = 0
        if dim > 0:
            # Calcoliamo durata media
            average_secs = (df1['durata_utilizzo'].sum()) / dim
            # Calcoliamo media consumi
            average_liters = (df1['litri'].sum()) / dim

        self.average_secs = average_secs
        self.average_liters = average_liters
        return average_secs, average_liters


class ModelBuilder:
    """
    This class i    out_data_dir = None is used to build the desired model
    """

    def __init__(self,  fixture, type, path="./data"):
        """
        The constructor of the class needs:
        :param fixture:  the name of the fixture
        :param type: the type of the moodel [global, monthly, weekly]
        :param path: the path of the folder containing the data file for the fixture
        """
        self.path = path + '/'
        self.utenza = fixture
        self.tipo = type

    def build_model(self):
        """
        Instantiate the model according to the type and the fixture.
        :return: The instantiated Model
        """
        df, df1, df2 = self.get_dataframe()

        if self.tipo == "global":
            obj_global = GlobalUsage(df, df1, df2)
            daily_usage = obj_global.compute_frequency()
            time_distribution = obj_global.compute_times()
            average_secs, average_liters = obj_global.compute_average()
            signal = self.model2json_global(daily_usage, time_distribution, average_secs, average_liters, self.utenza)
            if signal:
                logging.info('Modello generato.')

        elif self.tipo == "monthly":
            data = []
            for i in range(3, 11):
                obj_monthly = MonthlyUsage(df, df1, df2, i)
                daily_usage = obj_monthly.compute_frequency()
                time_distribution = obj_monthly.compute_times()
                average_secs, average_liters = obj_monthly.compute_average()
                data.append(self.model_monthly(daily_usage, time_distribution, average_secs, average_liters, i))
            signal = self.model2json_monthly(data, self.utenza)
            if signal:
                logging.info('Modello generato.')

        elif self.tipo == "weekly":
            data = []
            for i in range(0, 7):
                obj_weekly = WeeklyUsage(df, df1, df2, i)
                daily_usage = obj_weekly.compute_frequency()
                time_distribution = obj_weekly.compute_times()
                average_secs, average_liters = obj_weekly.compute_average()
                data.append(self.model_weekly(daily_usage, time_distribution, average_secs, average_liters, i))
            signal = self.model2json_weekly(data, self.utenza)
            if signal:
                logging.info('Modello generato.')

    def model2json_global(self, daily_usage, time_distribution, average_secs, average_liters, utenza):
        model = {"type": "global",
                 "parameters":
                     {
                         "daily_usage": daily_usage,
                         "time_distribution": time_distribution,
                         "average_secs": average_secs,
                         "average_liters": average_liters
                     }
                 }

        with open(self.path + "global_" + utenza + ".json", 'w') as outfile:
            json.dump(model, outfile, sort_keys=False, indent=4)

        return True


    def model_monthly(self, daily_usage, time_distribution, average_secs, average_liters, month):
        model = {"month": month,
                 "parameters":
                     {
                         "daily_usage": daily_usage,
                         "time_distribution": time_distribution,
                         "average_secs": average_secs,
                         "average_liters": average_liters,
                     }
                 }
        return model

    def model2json_monthly(self, data, utenza):
        modello = {"model": "monthly",
                   "month": data
                   }

        with open(self.path + "monthly_" + utenza + ".json", 'w') as outfile:
            json.dump(modello, outfile, sort_keys=False, indent=4)

        return True

    def model_weekly(self, daily_usage, time_distribution, average_secs, average_liters, weekday):
        model = {"weekday": weekday,
                 "parameters":
                     {
                         "daily_usage": daily_usage,
                         "time_distribution": time_distribution,
                         "average_secs": average_secs,
                         "average_liters": average_liters,
                     }
                 }
        return model

    def model2json_weekly(self, data, utenza):
        modello = {"model": "weekday",
                   "weekday": data
                   }

        with open(self.path + "weekly_" + utenza + ".json", 'w') as outfile:
            json.dump(modello, outfile, sort_keys=False, indent=4)

        return True

    def get_dataframe(self, csv_sep=' '):
        df = pd.read_csv(self.path + self.utenza + '_num_usage.csv', sep=csv_sep, header=None,
                         names=['mese', 'giorno', 'utilizzi', 'day_week'])
        df1 = pd.read_csv('./data/feed_' + self.utenza + '.MYD.csv', sep=csv_sep, header=None, names=['tempo', 'flusso'])
        df2 = pd.read_csv(self.path + self.utenza + '_usage.csv', sep=csv_sep, header=None,
                          names=['tempo_inizio', 'durata_utilizzo',
                                 'litri', 'mese', 'ora', 'giorno'])
        return df, df1, df2
