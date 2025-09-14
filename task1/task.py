import pandas as pd

def reader(path):
    data = pd.read_csv(path, header=None)

    names = sorted(set(data[0]).union(set(data[1])))
    result = pd.DataFrame(0, index=names, columns=names)

    for x, y in data.itertuples(index=False):
        result.loc[x, y] = 1

    return result

matrix = reader("analiz1.csv")
print(matrix)
