import sys
from itertools import combinations
from typing import Dict
from prettytable import PrettyTable

filename = sys.argv[1]
fileobject = open(filename, "r")
lines = fileobject.readlines()
total_no_trans = 0
support_of_all_item_set = {}
min_supp = int(sys.argv[2])
min_conf = int(sys.argv[3])

all_trans_support = {}  # type: Dict[str, int]
all_selected_trans_support = {}  # type: Dict[str, int]
all_selected_trans = []

print("file name ", filename)
print("Support", min_supp)
print("Confidence", min_conf)
print("========= Input Transactions ===========")
print()


def get_frequent_set(selected_set, rejected_set, all_trans, n):
    global all_selected_trans
    comb = combinations(selected_set, n)
    c2 = dict()
    for i in comb:
        set_i = set(i)
        for j in all_trans:
            if set_i.issubset(j):
                if i in c2:
                    c2[i] += 1
                else:
                    c2[i] = 1
    c2 = {key: value for key, value in c2.items()}
    all_trans_support.update(c2)
    selected_set = []
    rejected_set = []

    for key, value in c2.items():
        if (value / total_no_trans) * 100 >= min_supp:
            selected_set.append(key)
        # t.add_row([key, value])
        else:
            rejected_set.append(key)
    if selected_set:
        t = PrettyTable(['Item sets', 'Frequency'])
        for i in selected_set:
            t.add_row([i, c2.get(i)])
        print()
        print("Frequent set for k=", n)

        all_selected_trans = all_selected_trans + selected_set
        #  print("reject list for k= ", n, rejected_set)
        print(t)
    return selected_set, rejected_set


c1 = dict()
all_trans = []
for line in lines:
    line = line.replace("\n", "")
    print(line)
    words = line.split(", ")
    total_no_trans += 1
    seen = set()
    for word in words:
        if word in c1:
            c1[word] += 1
        else:
            c1[word] = 1
        seen.add(word)
    all_trans.append(seen)
c1 = {key: value for key, value in c1.items()}
all_trans_support.update(c1)
selected_set = []
rejected_set = []
print("---------------------------------------")
print()
print("Total number of transactions: ", total_no_trans)

t = PrettyTable(['Item sets ', 'Frequency'])
for key, value in c1.items():
    # print(key, ' :: ', value)
    if (value / total_no_trans) * 100 >= min_supp:
        selected_set.append(key)
        t.add_row([key, value])
    else:
        rejected_set.append(key)
# print("Frequent set for k=1", selected_set)
# print("reject list k=1 ", rejected_set)
print()
print("Frequent sets for k= 1")
print(t)

size = 2
while True:
    selected_set_1, rejected_set_1 = get_frequent_set(selected_set, rejected_set, all_trans, size)
    if not selected_set_1:
        break
    rejected_set = selected_set_1
    frequent_set = rejected_set_1
    size += 1
print()
print("========== List of all frequent item sets and support levels ============ ")
t = PrettyTable(['Frequent Item sets', 'Support in (%)'])
for support in all_selected_trans:
    Support_itemset = round(all_trans_support.get(support) / total_no_trans * 100)
    t.add_row([support, Support_itemset])
print(t)

print()
print("=========== Association and Confidence levels ==============")
t = PrettyTable(['Selected sets', 'Predecessor', 'Result', 'Support in (%)', 'Confidence in (%)'])

for x in all_selected_trans:
    size_of_item_set = len(x)
    itemset = set(x)

    while size_of_item_set - 1 > 0:
        comb = combinations(x, size_of_item_set - 1)
        for i in comb:
            left_side_items = i
            right_side_items = tuple(itemset - set(i))

            item_conf = round(round(all_trans_support.get(x) / total_no_trans * 100) * 100 / round(
                all_trans_support.get(left_side_items[0]) / total_no_trans * 100), 2)
            if item_conf >= min_conf:
                # print(left_side_items, "=>", right_side_items, round(all_trans_support.get(x) / total_no_trans * 100), round(item_conf), "Selected")
                t.add_row([left_side_items + right_side_items, left_side_items, right_side_items,
                           round(all_trans_support.get(x) / total_no_trans * 100), round(item_conf)])

            # else:
            # print(left_side_items, "=>", right_side_items, round(all_trans_support.get(x) / total_no_trans * 100), round(item_conf), "Rejected")

        size_of_item_set -= 1
print(t)
