import sys
import getopt

import csv
import os
import subprocess
import shutil


def extract_frame(video,timepos,folder):
    # millis = timepos
    # millis = (float(millis)/1000)
    # seconds=(int(timepos)/1000)%60
    # seconds = int(seconds)
    # minutes=(millis/(1000*60))%60
    # minutes = int(minutes)
    # hours=(millis/(1000*60*60))%24
 
    # time = "%d:%d:%f" % (hours, minutes, seconds+millis)   

    os.mkdir('./test/{folder}'.format(folder=folder))
    command = "ffmpeg -ss '{timepos}ms' -i {video} -frames:v 1 ./test/{folder}/{video}_{timepos}.png ".format(video=video, folder=folder, timepos=timepos)
    print(command)
    # subprocess.call(command,shell=True)    

if __name__ == '__main__':

    # Get full command-line arguments
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "v:c"
    long_options = ["video=", "csv="]
    arguments, values = getopt.getopt(
        argument_list, short_options, long_options)
    
    #default params
    video = ''
    csv_path = ''

    print('***************** Parameters *****************')
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--video"):            
            video = current_value
        elif current_argument in ("-c", "--csv"):            
            csv_path = current_value

    if (video == ''):
        print('Missed video argument. \n')
        exit()
    if (csv_path == ''):
        print('Missed csv argument.')
        exit()

    # Read CSV file
    with open(csv_path) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    tmp= './test/'
    for filename in os.listdir(tmp):
        file_path = os.path.join(tmp, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    for item in data_read:        
        extract_frame(video, item[0], item[1])



