# Поскольку строки только 2, то будет быстрее (и понятнее) сравнивать 2 ранжировки поэлементно 

from typing import List, Set, Tuple, Dict, Union
from collections import defaultdict

# Парсит строку ранжировки в список кластеров
def parse_ranking(ranking_str: str) -> List[Set[int]]:
    ranking_str = ranking_str.strip()
    if ranking_str.startswith('{') and ranking_str.endswith('}'):
        ranking_str = ranking_str[1:-1]
    
    clusters = []
    depth = 0
    current = ""
    
    for char in ranking_str:
        if char == '{':
            depth += 1
            if depth == 1:
                current = ""
        elif char == '}':
            depth -= 1
            if depth == 0:
                numbers = []
                for part in current.split(','):
                    part = part.strip()
                    if part:
                        numbers.append(int(part))
                if numbers:
                    clusters.append(set(numbers))
                current = ""
        elif char == ',' and depth == 0:
            if current.strip():
                clusters.append({int(current.strip())})
                current = ""
        elif depth > 0:
            current += char
        else:
            current += char
    
    if current.strip():
        clusters.append({int(current.strip())})
    
    return clusters

# Создает словарь: объект -> его ранг в ранжировке.
def get_position_map(ranking: List[Set[int]]) -> Dict[int, int]:
    position_map = {}
    for rank, cluster in enumerate(ranking):
        for obj in cluster:
            position_map[obj] = rank
    return position_map


# Находит ядро противоречий
def find_contradiction_core(ranking_a_str: str, ranking_b_str: str) -> Set[Tuple[int, int]]:
    ranking_a = parse_ranking(ranking_a_str)
    ranking_b = parse_ranking(ranking_b_str)
    
    pos_a = get_position_map(ranking_a)
    pos_b = get_position_map(ranking_b)
    
    all_objects = set(pos_a.keys()) | set(pos_b.keys())
    
    contradictions = set()
    
    for i in all_objects:
        for j in all_objects:
            if i >= j:
                continue
            
            # Проверка, что оба объекта есть в обеих ранжировках
            if i not in pos_a or j not in pos_a or i not in pos_b or j not in pos_b:
                continue
            
            rank_a_i = pos_a[i]
            rank_a_j = pos_a[j]
            
            rank_b_i = pos_b[i]
            rank_b_j = pos_b[j]
            
            # Проверка противоречия между 2 объектами
            is_contradiction = False
            
            if rank_a_i < rank_a_j and rank_b_i > rank_b_j:
                is_contradiction = True
            elif rank_a_i > rank_a_j and rank_b_i < rank_b_j:
                is_contradiction = True
            
            if is_contradiction:
                contradictions.add((min(i, j), max(i, j)))
    
    return contradictions

# Постройка согласованной ранжировки
def build_consensus_ranking(ranking_a_str: str, ranking_b_str: str) -> str:
    ranking_a = parse_ranking(ranking_a_str)
    ranking_b = parse_ranking(ranking_b_str)
    
    pos_a = get_position_map(ranking_a)
    pos_b = get_position_map(ranking_b)
    
    all_objects = set(pos_a.keys()) | set(pos_b.keys())
    
    contradictions = find_contradiction_core(ranking_a_str, ranking_b_str)
    
    parent = {obj: obj for obj in all_objects}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y
    
    for i, j in contradictions:
        union(i, j)
    
    for cluster_a in ranking_a:
        if len(cluster_a) > 1:
            cluster_list = list(cluster_a)
            for k in range(1, len(cluster_list)):
                union(cluster_list[0], cluster_list[k])
    
    for cluster_b in ranking_b:
        if len(cluster_b) > 1:
            cluster_list = list(cluster_b)
            for k in range(1, len(cluster_list)):
                union(cluster_list[0], cluster_list[k])
    
    clusters_map = defaultdict(set)
    for obj in all_objects:
        root = find(obj)
        clusters_map[root].add(obj)
    
    clusters = list(clusters_map.values())
    
    # Определение порядка между кластерами
    def compare_clusters(cluster1, cluster2):
        for obj1 in cluster1:
            for obj2 in cluster2:
                if obj1 in pos_a and obj2 in pos_a and obj1 in pos_b and obj2 in pos_b:
                    if pos_a[obj1] < pos_a[obj2] and pos_b[obj1] < pos_b[obj2]:
                        return True
                    if pos_a[obj1] > pos_a[obj2] and pos_b[obj1] > pos_b[obj2]:
                        return False
        
        # Если нет явного согласованного порядка, используем среднюю позицию
        avg_pos1 = sum(pos_a.get(obj, 0) + pos_b.get(obj, 0) for obj in cluster1) / len(cluster1)
        avg_pos2 = sum(pos_a.get(obj, 0) + pos_b.get(obj, 0) for obj in cluster2) / len(cluster2)
        return avg_pos1 < avg_pos2
    
    # Сортировка кластеров
    from functools import cmp_to_key
    
    def cluster_comparator(c1, c2):
        if compare_clusters(c1, c2):
            return -1
        elif compare_clusters(c2, c1):
            return 1
        return 0
    
    sorted_clusters = sorted(clusters, key=cmp_to_key(cluster_comparator))
    
    # Формирование результата
    result_parts = []
    for cluster in sorted_clusters:
        sorted_cluster = sorted(cluster)
        if len(sorted_cluster) == 1:
            result_parts.append(str(sorted_cluster[0]))
        else:
            result_parts.append("{" + ", ".join(map(str, sorted_cluster)) + "}")
    
    return "{" + ", ".join(result_parts) + "}"


ranking_a = "{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}"
ranking_b = "{3, 1, 2, 4, 6, 5, 7, 8, 9, 10}"

print("Ранжировка A:", ranking_a)
print("Ранжировка B:", ranking_b)
print()

# Находим ядро противоречий
core = find_contradiction_core(ranking_a, ranking_b)
print("Ядро противоречий:")
print(sorted(core))
print()

# Строим согласованную ранжировку
consensus = build_consensus_ranking(ranking_a, ranking_b)
print("Согласованная кластерная ранжировка:")
print(consensus)
print()

# Дополнительный пример с кластерами
print("=" * 50)
ranking_a2 = "{1, 2, 3, {4, 5}, {6, 7}, 8, 9}"
ranking_b2 = "{{1, 3}, 2, 4, {5, 7}, 6, 8, 9}"

print("Ранжировка A:", ranking_a2)
print("Ранжировка B:", ranking_b2)
print()

core2 = find_contradiction_core(ranking_a2, ranking_b2)
print("Ядро противоречий:")
print(sorted(core2))
print()

consensus2 = build_consensus_ranking(ranking_a2, ranking_b2)
print("Согласованная кластерная ранжировка:")
print(consensus2)
