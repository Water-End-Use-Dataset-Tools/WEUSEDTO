import argparse
import json
import random
import pandas as pd
import time

### Modifica di new_profile_geerator.py
random.seed(time.time())

class ProfileGenerator:

    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path

    def global_model(self, fixture, n_users):
        with open(self.in_path + '/global_' + fixture + '.json') as json_file:
            json_model = json.load(json_file)
            n_usages = json_model["parameters"]["daily_usage"]

        id_utente = []
        id_utilizzo = []
        ora_utilizzo = []
        min_utilizzo = []
        for i in range(0, n_users):
            random.seed()
            r = random.uniform(0, 1)

            probability = 0
            for key, value in n_usages.items():
                probability += value
                if probability >= r:

                    print("l'utente ", i, "usa ", key, "volte l'utenza")
                    time_dis = json_model["parameters"]["time_distribution"]
                    for k in range(int(key)):
                        r = random.uniform(0, 1)
                        minutes = random.randrange(60)
                        while minutes in min_utilizzo:
                            minutes = random.randrange(60)
                        min_utilizzo.append(minutes)

                        j = 0
                        probability = time_dis[j]
                        while r > probability:
                            j += 1
                            probability += time_dis[j]
                            #orario = str(j) + ':' + str(min)

                        # print("utilizzo ", k, "alle ore", j)
                        id_utente.append(i)
                        id_utilizzo.append(k)
                        ora_utilizzo.append(j)
                    break

        df = pd.DataFrame(list(zip(id_utente, id_utilizzo, ora_utilizzo, min_utilizzo)),
                          columns=['id_utente', 'id_utilizzo', 'ora_utilizzo', 'minuti'])
        df.to_csv(self.out_path + '/utilizzi_global_' + fixture + '.csv', index=False, header=1, sep=' ')

    def monthly_model(self, fixture, month, n_users):

        with open(self.in_path + '/monthly_' + fixture + '.json') as json_file:
            json_model = json.load(json_file)
            i = 0
            for i in range(len(json_model["month"])):
                if json_model["month"][i]["month"] == month:
                    n_usages = json_model["month"][i]["parameters"]["daily_usage"]
                    month = json_model["month"][i]["month"]
            if i == len(json_model["month"]):
                return -1

        month_index = i
        id_utente = []
        id_utilizzo = []
        ora_utilizzo = []
        min_utilizzo = []
        mese_utilizzo = []
        for i in range(0, n_users):
            random.seed()
            r = random.uniform(0, 1)

            probability = 0
            for key, value in n_usages.items():
                probability += value
                if probability >= r:

                    print("l'utente ", i, "usa ", key, "volte l'utenza")
                    time_dis = json_model["month"][month_index]["parameters"]["time_distribution"]
                    for k in range(int(key)):
                        r = random.uniform(0, 1)

                        minutes = random.randrange(60)
                        while minutes in min_utilizzo:
                            minutes = random.randrange(60)
                        min_utilizzo.append(minutes)

                        j = 0
                        probability = time_dis[j]
                        while r > probability:
                            j += 1
                            probability += time_dis[j]
                            #orario = str(j) + ':' + str(min)

                        # print("utilizzo ", k, "il mese", month, "alle ore", j)
                        id_utente.append(i)
                        id_utilizzo.append(k)
                        ora_utilizzo.append(j)
                        mese_utilizzo.append(month)
                    break

        df = pd.DataFrame(list(zip(id_utente, id_utilizzo, mese_utilizzo, ora_utilizzo, min_utilizzo)),
                          columns=['id_utente', 'id_utilizzo', 'mese_utilizzo', 'ora_utilizzo', 'minuti'])
        df.to_csv(self.out_path + '/utilizzi_monthly_' + str(month) + "_" + fixture + '.csv', index=False, header=1, sep=' ')

    def weekly_model(self, fixture, weekday, n_users):

        with open(self.in_path + '/weekly_' + fixture + '.json') as json_file:
            json_model = json.load(json_file)
            i = 0
            for i in range(len(json_model["weekday"])):
                if json_model["weekday"][i]["weekday"] == weekday:
                    n_usages = json_model["weekday"][i]["parameters"]["daily_usage"]
                    giorno = json_model["weekday"][i]["weekday"]
            if i == len(json_model["weekday"]):
                return -1

        weekday_index = i
        id_utente = []
        id_utilizzo = []
        giorno_utilizzo = []
        ora_utilizzo = []
        for i in range(0, n_users):
            random.seed()
            r = random.uniform(0, 1)

            probability = 0
            for key, value in n_usages.items():
                probability += value
                if probability >= r:

                    print("l'utente ", i, "usa ", key, "volte l'utenza")
                    time_dis = json_model["weekday"][weekday_index]["parameters"]["time_distribution"]
                    for k in range(int(key)):
                        random.seed()
                        r = random.uniform(0, 1)
                        # min = random.randrange(60)  # I minuti e le ore possono anche ripetersi
                        j = 0
                        probability = time_dis[j]
                        while r > probability:
                            j += 1
                            probability += time_dis[j]
                            # orario = str(j) + ':' + str(min)

                        # print("utilizzo ", k, "il giorno", giorno, "alle ore", j)
                        id_utente.append(i)
                        id_utilizzo.append(k)
                        giorno_utilizzo.append(giorno)
                        ora_utilizzo.append(j)
                    break
        df = pd.DataFrame(list(zip(id_utente, id_utilizzo, giorno_utilizzo, ora_utilizzo)),
                          columns=['id_utente', 'id_utilizzo', 'giorno_utilizzo', 'ora di utilizzo'])
        df.to_csv(self.out_path + '/utilizzi_weekly_' + str(giorno) + "_" + fixture + '.csv', index=False, header=1, sep=' ')


if __name__ == "__main__":
    mg = ProfileGenerator("./data", "./data/simulation")
    # GLOBAL
    fixture = 'washbasin'
    mg.global_model(fixture,  10)
    mg.monthly_model(fixture, 8,  10)
