import json

ranking_a = input() // [1,[2,3],4,[5,6,7],8,9,10]
ranking_b = input() // [3,[1,4],2,6,[5,7,8],[9,10]]

a = json.loads(ranking_a)
b = json.loads(ranking_b)

pos_a = {}
pos_b = {}

for idx, item in enumerate(a):
    if isinstance(item, list):
        for elem in item:
            pos_a[elem] = idx
    else:
        pos_a[item] = idx

for idx, item in enumerate(b):
    if isinstance(item, list):
        for elem in item:
            pos_b[elem] = idx
    else:
        pos_b[item] = idx

elements = sorted(set(pos_a.keys()) & set(pos_b.keys()))
contradictions = []

for i in range(len(elements)):
    for j in range(i + 1, len(elements)):
        e1, e2 = elements[i], elements[j]
        order_a = pos_a[e1] - pos_a[e2]
        order_b = pos_b[e1] - pos_b[e2]
        if order_a * order_b < 0:
            contradictions.append((e1, e2))

print(contradictions)
