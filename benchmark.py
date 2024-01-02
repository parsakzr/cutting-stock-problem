from stock import Stock, Sheet
from algorithm import bin_packing_BLF
from visualization import VisualSheet
import os
import timeit
import json

DATASET_DIR = "Original_Hopper_Turton/"
OUTPUT_DIR = "output/"


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    testcases = os.listdir(DATASET_DIR)
    testcases.sort()

    for testcase in testcases:
        print(f"----{testcase}----")
        with open(DATASET_DIR + testcase, "r") as f:
            num_stocks = int(f.readline().strip())
            sheet = Sheet(*map(int, f.readline().strip().split(" ")))
            for i in range(num_stocks):
                line = f.readline()
                sheet.addStock(Stock(*map(int, line.strip().split())))

            # start packing
            start = timeit.default_timer()
            bin_packing_BLF(sheet)
            elapsedTime = timeit.default_timer() - start
            stats = sheet.getStats()
            stats["packing_time"] = elapsedTime
            print(f"Stats: {sheet.getStats()}")
            if not os.path.exists(OUTPUT_DIR + testcase):
                os.mkdir(OUTPUT_DIR + testcase)

            path = OUTPUT_DIR + testcase + "/"
            # export the sheet.txt
            sheet.exportSheet(path + "sheet.txt")

            # export the stats.json
            with open(path + "stats.json", "w") as f:
                f.write(json.dumps(stats, indent=4))

            # draw the sheet
            visual_sheet = VisualSheet(sheet)
            visual_sheet.draw(unpacked=False, save=True, filename=path + "sheet.png")
            visual_sheet.draw(unpacked=True, save=False, filename=path + "unpacked.png")

            del sheet

        f.close()
