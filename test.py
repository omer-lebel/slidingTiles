from searchAI import Node
from heuristic import col_conflict, row_conflict

def test_row_conflict():
    print("------------ test of row conflict: ------------")

    print("0 row conflict test:")
    print("\t pass" if row_conflict(Node((0, 1, 2, 3, 4, 5, 6, 7, 8))) == 0 else "failed")

    print("- 1 row conflict test:")
    print("\t pass" if row_conflict( Node((0, 2, 1, 3, 4, 5, 6, 7, 8))) == 1 else "failed")

    print("- 2 row conflict at the same line:")
    print("\t pass" if row_conflict(Node((0, 1, 2, 5, 3, 4, 6, 7, 8))) == 2 else "failed")

    print("3 row conflict at the same line (inverse col):")
    print("pass" if row_conflict(Node((0, 1, 2, 3, 4, 5, 8, 7, 6))) == 3 else "failed")

    print("- inverse row but not at the target col:")
    print("pass" if row_conflict(Node((5, 4, 3, 0, 1, 2, 6, 7, 8))) == 0 else "failed")

    print("- max row conflict:")
    print("pass" if row_conflict(Node((2, 1, 0, 5, 4, 3, 8, 7, 6))) == 7 else "failed")


def test_col_conflict():
    print("------------ test of row conflict: ------------")

    print("0 col conflict test:")
    print("pass" if col_conflict(Node((0, 1, 2, 3, 4, 5, 6, 7, 8))) == 0 else "failed")

    print("1 col conflict test:")
    print("pass" if col_conflict( Node((6, 1, 2, 0, 4, 5, 3, 7, 8))) == 1 else "failed")

    print("2 col conflict at the same line:")
    print("pass" if col_conflict(Node((0, 7, 2, 3, 1, 5, 6, 4, 8))) == 2 else "failed")

    print("3 col conflict at the same line (inverse col):")
    print("pass" if col_conflict(Node((0, 1, 8, 3, 4, 5, 6, 7, 2))) == 3 else "failed")

    print("inverse col but not at the target col:")
    print("pass" if col_conflict(Node((0, 8, 7, 3, 5, 4, 6, 2, 1))) == 0 else "failed")

    print("max col conflict:")
    print("pass" if col_conflict(Node((6, 7, 8, 3, 4, 5, 0, 1, 2))) == 7 else "failed")


# def liner_conflict_test(node):
#     real_dis = bfs(SlidingPuzzle(node.state))[0].path_cost
#     mn = heuristic.manhattan_distance(node)
#     row = heuristic.row_conflict(node)
#     col = heuristic.col_conflict(node)
#     # print(f"row conflict: {row}, col conflict: {col}")
#     liner = mn + row + col
#     a = liner + node.path_cost
#     print(f"{node}\t\t Manhattan: {mn} \t LinearConflict:{liner} \t A_star: {a} \t Real:{real_dis}")
#     return liner