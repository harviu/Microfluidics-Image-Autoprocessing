from generate_values import calculate
from image_process import *
import os
import re
import csv
from multiprocessing import Pool
from datetime import datetime


def one_process(pair):
    key = pair[0]
    img = pair[1]
    gfp = img[:, :, :, 2]
    vals, chosens, mark = calculate(gfp)
    comment = '' if mark > 0.6 else '_*'
    row1 = [key + '_gfp' + str(comment), ] + vals

    rfp = img[:, :, :, 1]
    vals, chosens, mark = calculate(rfp)
    comment = '' if mark > 0.3 else '_*'
    row2 = [key + '_rfp' + str(comment), ] + vals

    return [row1, row2]


## Loop through nd2 files in nd2 directory
## For each nd2 file found, process it and write results to similarly-named csv file.
##
if __name__ == '__main__':
    nd2_at_end = re.compile("nd2$")
    nd2_dirname = '../nd2'
    output_dirname = '../output'
    nd2_dirname_encoded = os.fsencode(nd2_dirname)
    for filename_encoded in os.listdir(nd2_dirname_encoded):
        filename = filename_encoded.decode('utf-8')
        if nd2_at_end.search(filename):
            nd2_filename = nd2_dirname + '/' + filename
            sample_name = os.path.splitext(filename)[0]
            csv_filename = output_dirname + '/' + sample_name + '.csv'
            try:
                start = datetime.now()
                nd2_image = sum_z(full_nd2_read(nd2_filename))
                end = datetime.now()
                print(sample_name + " loaded, time used: "+str(end-start))

                start = datetime.now()
                cropped = cut_full_image(nd2_image)
                end = datetime.now()
                print(sample_name + " cropped, time used: "+str(end-start))

                start = datetime.now()
                p = Pool(8)
                rows = p.map(one_process, cropped.items())
                end = datetime.now()
                print(sample_name + " processed, time used: "+str(end-start))
                with open(csv_filename, 'w+', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    lines = []
                    for i in range(len(rows[0][0])):
                        lines.append([])
                    for row in rows:
                        for index in range(len(row[0])):
                            lines[index].append(row[0][index])
                            lines[index].append(row[1][index])
                    for line in lines:
                        csvwriter.writerow(line)
                print(sample_name + " finished processing")
            except:
                print(sample_name + " cannot be processed")
