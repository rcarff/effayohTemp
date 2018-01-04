"""
Compare item definition and standards between data sheets.

This script compares the item definitions and standards published for
the FAO detailed trade matrix and food balance sheets data. The script
counts the number of items defined for each data set and prints for each
data set all the items that belong only to that data set, and then
the script prints all the items that belong to both data sets.
"""


import os
import csv


class CompareError(Exception): pass


def main():

    dtm_items_file = os.path.join(
        "faostat",
        "detailed-trade-matrix",
        "definitions-and-standards",
        "item-2-27-2017.csv"
    )

    fbs_items_file = os.path.join(
        "faostat",
        "food-balance-sheets",
        "definitions-and-standards",
        "item-3-2-2017.csv"
    )

    dtm_items = {}

    with open(dtm_items_file) as fh:
        dtm_reader = csv.DictReader(fh)
        for row in dtm_reader:
            item_code = row["Item Code"]
            if item_code in dtm_items:
                raise CompareError("Duplicate item code definition.")
            dtm_items[item_code] = (row["Item"], row["Description"])

    fbs_items = {}

    with open(fbs_items_file) as fh:
        fbs_reader = csv.DictReader(fh)
        for row in fbs_reader:
            item_code = row["Item Code"]
            if item_code in fbs_items:
                raise CompareError("Duplicate item code definition.")
            fbs_items[item_code] = (row["Item"], row["Description"])

    common_keys = dtm_items.keys() & fbs_items.keys()

    for key in common_keys:
        if dtm_items[key] != fbs_items[key]:
            print(("Item Code {key} defined in both definitions "
                   "and standards, however, they differ in their "
                   "name and description.").format(key=key))
            print("Detailed trade matrix definition:", dtm_items[key])
            print("Food balance sheets definition:", fbs_items[key])

    print("Item Codes in common between the detailed",
          "trade matrix and food balance sheet:\n")

    print("Item Codes unique to the food balance sheet:\n")

    for key in fbs_items:
        if not key in common_keys:
            print(key, fbs_items[key])
    else:
        print()

    print("Item Codes unique to the detailed trade matrix:\n")

    for key in dtm_items:
        if not key in common_keys:
            print(key, dtm_items[key])


if __name__ == "__main__":
    main()
