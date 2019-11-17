import glob
import errno
import os
import re


path = '*.report'
files = glob.glob(path)
for name in files:
    try:
        with open(name) as f:
            if os.stat(name).st_size == 0:
                print('Empty Report')
            else:
                line = f.readline()
                session_id = line.split(' : ')
                outputfilename = re.sub('[^a-zA-Z0-9 \n\.]', '', session_id[1]).strip()+".txt"
                outputfile = open(outputfilename,'w')
                cnt = 1
                while line:
                    outputfile.write(line.strip()+'\n')
                    line = f.readline()
                    cnt += 1
                outputfile.close()
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise