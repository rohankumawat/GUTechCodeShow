from collections import defaultdict, deque

# Parse the login attempts from the file
with open('keylog.txt', 'r') as f:
    attempts = [line.strip() for line in f]

# Construct the graph
graph = defaultdict(list)
in_degree = defaultdict(int)
for attempt in attempts:
    for i, digit in enumerate(attempt):
        for other_digit in attempt[i+1:]:
            if other_digit not in graph[digit]:
                graph[digit].append(other_digit)
                in_degree[other_digit] += 1

# Perform the topological sort
queue = deque([digit for digit in graph if in_degree[digit] == 0])
result = []
while queue:
    digit = queue.popleft()
    result.append(digit)
    for other_digit in graph[digit]:
        in_degree[other_digit] -= 1
        if in_degree[other_digit] == 0:
            queue.append(other_digit)

# Print the passcode as a string
passcode = ''.join(result)
print(passcode)