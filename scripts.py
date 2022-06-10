GENERAL_LTE = {
    1.4: [(5, 0), (6, 0)],
    3: [(4, 0), (15, 0)],
    5: [(8, 0), (25, 0)],
    10: [(12, 0), (50, 0)],
    15: [(16, 0), (75, 0)],
    20: [(18, 0), (100, 0)],
}


def main():
    eee = GENERAL_LTE[10][0]
    # print(GENERAL_LTE[10][0])
    print(nameof(eee))


if __name__ == '__main__':
    main()
