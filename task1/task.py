import pandas as pd
from typing import Tuple, List

def classes(s: str) -> Tuple[
        List[List[bool]],
        List[List[bool]],
        List[List[bool]],
        List[List[bool]],
        List[List[bool]]]:

    df = pd.read_csv(s, sep=" ", header=None).astype(int)

    max_val = max(df.iloc[:, 0].max(), df.iloc[:, 1].max())

    r1 = [[False for _ in range(max_val + 1)] for _ in range(max_val + 1)]
    r2 = [[False for _ in range(max_val + 1)] for _ in range(max_val + 1)]
    r3 = [[False for _ in range(max_val + 1)] for _ in range(max_val + 1)]
    r4 = [[False for _ in range(max_val + 1)] for _ in range(max_val + 1)]
    r5 = [[False for _ in range(max_val + 1)] for _ in range(max_val + 1)]

    exist = set()
    children = {}  # parent -> list of children
    parents = {}   # child -> parent

        # Заполнение r1, r2
    for i in range(len(df)):
        x = int(df.iloc[i, 0])
        y = int(df.iloc[i, 1])

        if x == y:
            raise Exception("Граф указывает сам на себя!")

        r1[x][y] = True
        r2[y][x] = True

        exist.add(x)
        exist.add(y)

        if x not in children:
            children[x] = []
        children[x].append(y)
        parents[y] = x

    # r3
    for node in exist:
        visited = set()
        queue = [(node, 1)]

        while queue:
            current, dist = queue.pop(0)
            if current in children:
                for child in children[current]:
                    if child not in visited:
                        visited.add(child)
                        if dist > 1:
                            r3[node][child] = True
                        queue.append((child, dist + 1))

    # r4
    for i in range(max_val + 1):
        for j in range(max_val + 1):
            if r3[i][j]:
                r4[j][i] = True

    # r5
    for node in exist:
        if node in parents:
            parent = parents[node]
            if parent in children:
                for sibling in children[parent]:
                    if sibling != node:
                        r5[node][sibling] = True

    return [r1, r2, r3, r4, r5]

classes("./ult.csv")
