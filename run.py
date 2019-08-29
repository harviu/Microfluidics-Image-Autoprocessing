from generate_values import calculate
from image_process import *
import os
import re
import csv
## Loop through nd2 files in nd2 directory
## For each nd2 file found, process it and write results to similarly-named csv file.
##
if __name__ == '__main__':
    nd2_at_end = re.compile("nd2$")
    nd2_dirname = '../nd2'
    nd2_dirname_encoded = os.fsencode(nd2_dirname)
    for filename_encoded in os.listdir(nd2_dirname_encoded):
        filename = filename_encoded.decode('utf-8')
        if nd2_at_end.search(filename):
            nd2_filename = nd2_dirname + '/' + filename
            sample_name = os.path.splitext(filename)[0]
            csv_filename = nd2_filename + '.csv'
            # print(sample_name)
            nd2_image = sum_z(full_nd2_read(nd2_filename))
            cropped = cut_full_image(nd2_image)
            # for (dirpath, dirnames, tiffnames) in os.walk("./result/"+sample_name+"/"):
            #     for tiffname in tiffnames:
            #         if tiffname.endswith('.tiff'): 
            #             img = tif_read(os.sep.join([dirpath, tiffname]))
            #             gfp = img[:,:,:,2]
            #             vals,chosens = calculate(img)
            #             # print (vals)
            #             with open(csv_filename, 'a+', newline='') as csvfile:
            #                 csvwriter = csv.writer(csvfile, delimiter=',',
            #                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #                 csvwriter.writerow(vals)
            for key in cropped:
                img = cropped[key]
                gfp = img[:,:,:,2]
                vals,chosens,mark = calculate(gfp)
                comment = '' if mark>0.6 else '_*'
                row1 = [key+'_gfp'+str(comment),] + vals
                
                rfp = img[:,:,:,1]
                vals,chosens,mark = calculate(rfp)
                comment = '' if mark>0.3 else '_*'
                row2 = [key+'_rfp'+str(comment),] + vals
                with open(csv_filename, 'a+', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow(row1)
                    csvwriter.writerow(row2)