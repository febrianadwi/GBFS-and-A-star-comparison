import heapq
import time

# Fungsi untuk mencetak board dengan rapi
def print_board(board):
    for row in board:
        print(" ".join(str(x) for x in row))
    print()

# Fungsi untuk mencari posisi 0 (kosong)
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return (i, j)

# Mengecek apakah 2 state sama
def is_goal(state):
    return state == [[1,2,3],[4,5,6],[7,8,0]]

# Generate kemungkinan langkah dari satu state
def get_neighbors(state):
    neighbors = []
    x, y = find_zero(state)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# Heuristic: misplaced tiles
def h_misplaced(state):
    goal = [[1,2,3],[4,5,6],[7,8,0]]
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count

# Convert 2D list to tuple (immutable) for hashing
def to_tuple(state):
    return tuple(tuple(row) for row in state)

# GBFS menggunakan hanya h(n)
def greedy_bfs(start):
    visited = set()
    pq = [(h_misplaced(start), start, [])]  # (priority, current_state, path)
    while pq:
        _, current, path = heapq.heappop(pq)
        if is_goal(current):
            return path + [current]
        visited.add(to_tuple(current))
        for neighbor in get_neighbors(current):
            if to_tuple(neighbor) not in visited:
                heapq.heappush(pq, (h_misplaced(neighbor), neighbor, path + [current]))
    return []

# A* menggunakan f(n) = g(n) + h(n)
def a_star(start):
    visited = set()
    pq = [(h_misplaced(start), 0, start, [])]  # (f, g, state, path)
    while pq:
        f, g, current, path = heapq.heappop(pq)
        if is_goal(current):
            return path + [current]
        visited.add(to_tuple(current))
        for neighbor in get_neighbors(current):
            if to_tuple(neighbor) not in visited:
                new_g = g + 1
                heapq.heappush(pq, (new_g + h_misplaced(neighbor), new_g, neighbor, path + [current]))
    return []

def run_algorithm(algorithm, name, start_state):
    print(f"Running {name}...\nStart state:")
    print_board(start_state)
    start_time = time.time()
    result = algorithm(start_state)
    end_time = time.time()
    print(f"{name} completed in {(end_time - start_time) * 1000:.2f} ms")
    print(f"Steps: {len(result) - 1}")
    print(f"Final path:")
    for step in result:
        print_board(step)

# Contoh state awal
start1 = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
start2 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
start3 = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]  # lebih kompleks

run_algorithm(greedy_bfs, "GBFS", start1)
run_algorithm(a_star, "A*", start1)

run_algorithm(greedy_bfs, "GBFS", start2)
run_algorithm(a_star, "A*", start2)

run_algorithm(greedy_bfs, "GBFS", start3)
run_algorithm(a_star, "A*", start3)
