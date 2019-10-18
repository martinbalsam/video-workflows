import subprocess
import os
import datetime
import re
import csv
import argparse
import shutil

parser = argparse.ArgumentParser(description='create a csv file with all the useful metadata of videos within a folder')

parser.add_argument('path', type=str, help='name of the folder that we want to extract the metadata from')

args = parser.parse_args()

if not os.path.exists(args.path):
    raise ValueError('the path doesnt exists')


def num_to_lang(indx):
    if indx < 0 or indx >5:
        raise ValueError('index out of range, it must be between 0 and 5')
    else:
        if indx == 0:
            return "EN"
        if indx == 1:
            return "ES"
        if indx == 2:
            return "DE"
        if indx == 3:
            return "FR"
        if indx == 4:
            return "IT"
        if indx == 5:
            return "PT"


def str2scalar(time):
    """
    time is in the form dd:dd:dd.dd and it returns the number of centiseconds
    """
    if not time:
        return -10000000000000
    seconds = float(time[-5:])
    minutes = int(time[3:5])
    return minutes*60 + seconds


def time_delta(time1, time2):
    """
    time1 and time2 are in the form dd:dd:dd.dd
    """
    return abs(str2scalar(time1) - str2scalar(time2))


class Video(object):

    def __init__(self, path, filename):
        self.filename = filename
        self.setname = os.path.splitext(filename)[0][:-3]
        self.language = os.path.splitext(filename)[0][-2:]
        self.path = path
        self.duration = ''
        self.bitrate = ''
        self.fps = ''
        self.dimension = ''
        self.creation_date = ''
        self.codec = ''
        filepath = path+'/'+filename
        result = subprocess.Popen(["/usr/local/bin/ffprobe" , filepath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        for line in result.stdout.readlines():
            #print line
            if re.search('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line):
                if not self.creation_date:
                    self.creation_date += re.search('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line).group(1)
                else:
                    continue

            if re.search('Duration: (.*), ', line):
                self.duration += re.search('Duration: (\d{2}:\d{2}:\d{2}\.\d{2}), ', line).group(1)
            if re.search('Video: ([^\s]+) ', line):
                self.codec += re.search('Video: ([^\s]+) ', line).group(1)
            if re.search('bitrate: (.*) kb', line):
                self.bitrate += re.search('bitrate: (.*) kb', line).group(1)
            if re.search('\s([+-]?[0-9]*[.]?[0-9]+) fps', line):
                self.fps += re.search('\s([+-]?[0-9]*[.]?[0-9]+) fps', line).group(1)
            if re.search('([1-9][0-9]+x\d+)', line):
                self.dimension = re.search('([1-9][0-9]+x\d+)', line).group(1)
        if self.creation_date is '':
            try:
                self.creation_date = datetime.datetime.fromtimestamp(os.stat(path).st_birthtime).strftime("%d-%m-%Y")
            except OSError, ValueError:
                pass



    def printAttributes(self):
        attrs = vars(self)
        print ', '.join("%s: %s" % item for item in attrs.items())



now_string = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

"""
for path, dirs, files in os.walk(args.path):
    for filename in files:
        if filename[0]==".":
            continue
        else:
            print filename, getFps(filename)
            print("    ")

"""
"""
 '2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p'
"""
"""
for path, dirs, files in os.walk(args.path):
    for filename in files:
        metadata = Video(args.path, filename)
        if filename[0]==".":
            continue
        else:
            metadata.printAttributes()
"""

def logic_array_to_bool(arr):
    """
    takes as input an array of boolean and returns 1 if it contains one true, and 0, otherwise
    """
    count = 0
    for a in arr:
        if a:
            count+=1
    if count == 1:
        return 1
    else:
        return 0


class Set(object):
    def __init__(self, setname):
        self.setname = setname
        self.durations=["","","","","",""]
        self.log = ""


    def setDurationForLanguage(self, language, duration):
        if language == "EN":
            self.durations[0] += duration
        elif language == "ES":
            self.durations[1] += duration
        elif language == "DE":
            self.durations[2] += duration
        elif language == "FR":
            self.durations[3] += duration
        elif language == "IT":
            self.durations[4] += duration
        elif language == "PT":
            self.durations[5] += duration

    def print_sets(self):
        print " //////// "
        print self.setname
        print "EN: ", self.durations[0]
        print "ES: ", self.durations[1]
        print "DE: ", self.durations[2]
        print "FR: ", self.durations[3]
        print "IT: ", self.durations[4]
        print "PT: ", self.durations[5]
        self.quality_check()
        print "LOG: ", self.log


    def quality_check(self):

        empty_values = [False,False,False,False,False,False]
        duration_errors = [False,False,False,False,False,False]
        for indx, dur in enumerate(self.durations):
            if not dur:
                empty_values[indx] = True
            if not time_delta(dur,self.durations[0])<0.08:
                duration_errors[indx] = True
        empty_log_string = ''
        duration_log_string = ''
        for i in range(6):
            if empty_values[i]:
                empty_log_string += num_to_lang(i) + ' '
            if duration_errors[i] and not empty_values[i]:
                duration_log_string += num_to_lang(i) + ' '
        log_string = ''
        plurals1 = logic_array_to_bool(empty_values)
        if empty_log_string:
            log_string += empty_log_string + plurals1*"is" + (1-plurals1)*"are" + " missing!!!  "
        plurals2 = logic_array_to_bool(duration_errors)
        if duration_log_string:
            log_string += duration_log_string + plurals2*"has" + (1-plurals2)*"have" + " different duration from the EN version!!!   "
        if not log_string:
            return " -- ALL IS GOOD -- "
        else:
            return log_string


fold_root = os.path.basename(os.path.normpath(args.path))
fold_name = os.path.basename(os.path.normpath(args.path)) + "_quality_control"
fold_path = args.path +"/"+ fold_name


print fold_name


if not os.path.exists(fold_path):
    os.makedirs(fold_path)
else:
    shutil.rmtree(fold_path)
    os.makedirs(fold_path)
print fold_path
print os.path.exists(fold_path)

print fold_path + "/" + os.path.split(os.path.dirname(args.path))[1]  + "_metadata_" + now_string + ".csv"

with open(fold_path + "/" + fold_root  + "_metadata_" + now_string + ".csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['filename', 'duration', 'framerate', 'bitrate', 'dimension', 'creation date', 'codec'])
    videos = []
    sets = []
    sets_data = []
    for path, dirs, files in os.walk(args.path):
        for filename in files:
            if filename[0]==".":
                continue
            else:
                video = Video(path, filename)
                videos.append(video)
                if video.duration:
                    writer.writerow([video.filename, video.duration, video.fps + ' fps', video.bitrate, video.dimension, video.creation_date, video.codec])
                    if video.setname not in sets:
                        sets.append(video.setname)
                        yset = Set(video.setname)
                        yset.setDurationForLanguage(video.language, video.duration)
                        sets_data.append(yset)

                    else:
                        for index, yset in enumerate(sets):
                             if video.setname == yset:
                                sets_data[index].setDurationForLanguage(video.language,video.duration)
                else:
                    continue

with open(fold_path + "/" + fold_root  + "_quality-check_" + now_string + ".csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['set-name', 'EN', 'ES', 'DE', 'FR', 'IT', 'PT', 'log'])
    for yset in sets_data:
        writer.writerow([yset.setname ,yset.durations[0],yset.durations[1],yset.durations[2],yset.durations[3],yset.durations[4],yset.durations[5],yset.quality_check()])





