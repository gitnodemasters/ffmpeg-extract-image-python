import sys
import getopt

import shutil
import os
import subprocess
import glob



def extract_frames(video,timespan, dest):
    files = glob.glob('{dest}/*'.format(dest=dest))
    for f in files:
        os.remove(f)
    # command = "ffmpeg -i {video} -r {timespan} {dest}/%d.png".format(video=video, timespan=timespan, dest=dest)
    # command = "ffmpeg -i {video} -vf fps={timespan} {dest}/%d.png".format(video=video, timespan=timespan, dest=dest)
    len = get_length(video)
    step = timespan
    while(1):
        command = "ffmpeg -ss '{timespan}ms' -i {video} -frames:v 1 {dest}/{video}_{timespan}.png ".format(video=video, dest=dest, timespan=timespan)
        subprocess.call(command,shell=True)
        timespan = str(int(timespan) + int(step))
        if ( float(timespan) > len ): break
    print(command)
    
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)*1000

if __name__ == '__main__':

    # Get full command-line arguments
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "v:i:d"
    long_options = ["video=", "interval=", "dest="]
    arguments, values = getopt.getopt(
        argument_list, short_options, long_options)
    
    #default params
    video = ''
    timespan = ''
    dest = ''

    print('***************** Parameters *****************')
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--video"):            
            video = current_value
        elif current_argument in ("-i", "--interval"):            
            timespan = current_value
        elif current_argument in ("-d", "--dest"):            
            dest = current_value

    if (video == ''):
        print('Missed video argument. \n')
        exit()
    if (timespan == ''):
        print('Missed interval argument.')
        exit()
    if (dest == ''):
        print('Missed destination argument.')
        exit()
    
    extract_frames(video, timespan, dest)


