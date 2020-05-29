import csv
import sys
import time
import dhash
from PIL import Image


def diff(h1, h2):
    return dhash.get_num_bits_different(h1, h2)


def processImage(csvfile):
    results = []
    start_time = 0
    dictHash = dict()
    for row in csvfile:
        if row.__len__():
            start_time = time.process_time()
            score = computeScore(dictHash, row)
            results.append([row[0], row[1], score, round(time.process_time() - start_time,3)])
    # print(dictHash)
    return results


def computeScore(dictHash, row):
    if row[0] not in dictHash.keys():
        dictHash[row[0]] = dhash.dhash_int(Image.open(row[0]))
    if row[1] not in dictHash.keys():
        dictHash[row[1]] = dhash.dhash_int(Image.open(row[1]))
    difference = diff(dictHash[row[0]], dictHash[row[1]])
    print(difference)
    score = round((difference / (8 * 8 * 2)), 2)
    return score

def main(argvs):

    if (argvs.__len__() <=1):
        sys.exit("Error-> That looks like a wrong file format. The supported file formats are csv and txt.")
    if (argvs[1].endswith(('.csv', '.txt'))):
        with open(argvs[1], encoding='utf-8-sig') as file:
            csvfile = csv.reader(file)
            result = processImage(csvfile)
            print(result)
            file.close()
        with open("comparison_result.csv", 'w', newline='') as newfile:
            thewriter = csv.writer(newfile)
            for i in range(0, result.__len__()):
                thewriter.writerow(result[i])
            newfile.close()
    else:
        sys.exit("Error-> That looks like a wrong file format. The supported file formats are csv and txt.")


if __name__ == '__main__':
    main(sys.argv)