from pprint import pprint


vakken = {
    "DU": {"begin":  9_00, "eind": 18_59},
    "AU": {"begin": 19_00, "eind": 20_59},
    "NU": {"begin": 21_00, "eind": 23_59},
}


afas_data = [
    {"tijd": {"begin": 10_30, "eind": 14_05}, "user": "1", "datum": "1/1/2000"},
    {"tijd": {"begin": 16_01, "eind": 22_40}, "user": "1", "datum": "1/1/2000"},
    {"tijd": {"begin":  9_05, "eind": 17_00}, "user": "2", "datum": "1/1/2000"},
]


store = {}

timestamps = "tijd"

start_str = "begin"
end_str = "eind"

for i in afas_data:

    # splitten van de uren
    for naam, uren in vakken.items():
        # check of de geschreven uren in dit vak zitten
        if i[timestamps][end_str] < uren[start_str] or i[timestamps][start_str] > uren[end_str]:
            continue

        store[start_str], store[end_str] = None, None

        # pak de benodigde uren
        if uren[start_str] < i[timestamps][start_str] < uren[end_str]:
            store[start_str] = i[timestamps][start_str]
        else:
            store[start_str] = uren[start_str]

        if uren[start_str] < i[timestamps][end_str] < uren[end_str]:
            store[end_str] = i[timestamps][end_str]
        else:
            store[end_str] = uren[end_str]

        key = f"user_{i['user']}_{i['datum']}_{naam}"
        value = {start_str: store[start_str], end_str: store[end_str]}

        if store.get(key):
            store[key].append(value)
        else:
            store[key] = [value]


pprint(afas_data)
print()
pprint(store)
