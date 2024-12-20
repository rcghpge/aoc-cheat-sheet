import sys
import networkx as nx


def create_graph(grid: list[list[str]], w: int, h: int, with_cheats: bool) -> nx.Graph:
    """Create a graph representation of the grid."""
    g = nx.Graph()

    for y in range(h):
        for x in range(w):
            if not with_cheats and grid[y][x] == "#":
                continue

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                x2, y2 = x + dx, y + dy
                if x2 < 0 or x2 >= w or y2 < 0 or y2 >= h:
                    continue

                if not with_cheats and grid[y2][x2] == "#":
                    continue

                g.add_edge((x, y), (x2, y2))

    return g


def count_cheats(grid: list[list[str]], w: int, h: int, sx: int, sy: int, ex: int, ey: int, cheat_cutoff: int) -> int:
    """Count valid cheats that save at least 100 picoseconds."""
    g_normal = create_graph(grid, w, h, with_cheats=False)
    g_cheats = create_graph(grid, w, h, with_cheats=True)

    start_dists = nx.single_source_shortest_path_length(g_normal, (sx, sy))
    end_dists = nx.single_source_shortest_path_length(g_normal, (ex, ey))

    normal_distance = start_dists[(ex, ey)]

    out = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "#":
                continue

            cheat_dists = nx.single_source_shortest_path_length(g_cheats, (x, y), cutoff=cheat_cutoff)

            for (x2, y2), distance in cheat_dists.items():
                if grid[y2][x2] == "#":
                    continue

                cheat_distance = start_dists[(x, y)] + end_dists[(x2, y2)] + distance
                if normal_distance - cheat_distance >= 100:
                    out += 1

    return out


def main(file_path: str) -> None:
    """Main function to solve both Part 1 and Part 2."""
    with open(file_path, "r") as f:
        data = f.read().strip()

    grid = [list(line) for line in data.splitlines()]
    w = len(grid[0])
    h = len(grid)

    for y in range(h):
        for x in range(w):
            if grid[y][x] == "S":
                sx, sy = x, y
            elif grid[y][x] == "E":
                ex, ey = x, y

    # Part 1: Cheat cutoff = 2
    part_1_result = count_cheats(grid, w, h, sx, sy, ex, ey, cheat_cutoff=2)
    print(f"Part 1: {part_1_result}")

    # Part 2: Cheat cutoff = 20
    part_2_result = count_cheats(grid, w, h, sx, sy, ex, ey, cheat_cutoff=20)
    print(f"Part 2: {part_2_result}")


if __name__ == "__main__":
    file_path = "input.txt"
    main(file_path)

