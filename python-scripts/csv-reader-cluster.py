import csv
import glob
import os
import argparse


parser = argparse.ArgumentParser(description='create a html page with videos from a directory')

parser.add_argument('path', type=str, help='name of the folder that we want to get the video from')

args = parser.parse_args()

if not os.path.exists(args.path):
    raise ValueError('the path doesnt exists')


dirpath = args.path


'''
when debigging use:
'''

#dirpath = os.getcwd()





html_file_name = os.path.basename(os.path.normpath(dirpath)) + "_video_page.html"
file_path = dirpath +"/"+ html_file_name


try:
    os.remove(html_file_name)
except OSError:
    pass


list_csv_files = glob.glob(dirpath+'/*.csv')  #lists all the .csv files in the current path

print list_csv_files

if len(list_csv_files) is not 1:
    raise ValueError("ERROR, wrong number of csv files in the current folder. There should ONLY BE ONE!") 
else:
    csvfilename = list_csv_files[0]

videoid_list =[]
amount_spent_list = []
ctr_list = []
awt_list = []
awt_3sec_list = []
awt_10sec_list = []
result_rate_list =[]
engagement_rate_facebook_list = []
engagement_rate_social_list = []
engagement_rate_list = []


def get_index_from_key(a, key):
    try:
        return a.index(key)
    except ValueError:
        return -1

with open(csvfilename) as csvfile:

    reader = csv.DictReader((l.lower() for l in csvfile))
    i=0
    for row in reader:
        #print row['Ad name']
    #print reader[0]
        videoid_list.append(row['ad name'])
        amount_spent_list.append(row['amount spent (eur)'])
        ctr_list.append(row['ctr (link click-through rate)'])
        awt_list.append(row['video average watch time'])
        result_rate_list.append(row['result rate'])
        engagement_rate_list.append(row['engagement rate ranking'])

        try:
            awt_3sec_list.append(row['3 sec / video plays'])
        except (NameError, KeyError):
            pass

        try:
            awt_10sec_list.append(row['10 sec / video plays'])
        except (NameError, KeyError):
            pass

        try:
            engagement_rate_facebook_list.append(row['engagement rate (facebook)'])
        except (NameError, KeyError):
            pass

        try:
            engagement_rate_social_list.append(row['engagement rate (social media)'])
        except (NameError, KeyError):
            pass


def id_to_index(id):
    return videoid_list.index(id)

def amount_spent(id):
    if id not in videoid_list:
        return ""
    else:
        amount_float_list =[]
        for i in amount_spent_list:
            try:
                amount_float_list.append(float(i))
            except ValueError:
                amount_float_list.append(0.0)


        try:
            amount = float(amount_spent_list[id_to_index(id)])

            if amount == max(amount_float_list):
                return "<td bgcolor='#ffbf80'><b><u>"+str(round(amount,2))+" &euro;</b></u> </td>"
            else:
                return "<td>" + str(amount) + " &euro; </td>"
            

        except (ValueError, IndexError) as e:
            return ""

def ctr(id):
    if id not in videoid_list:
        return ""
    else:
        ctr_float_list =[]
        for i in ctr_list:
            try:
                ctr_float_list.append(float(i))
            except ValueError:
                ctr_float_list.append(0.0)


        try:
            ctr_val = float(ctr_list[id_to_index(id)])

            if ctr_val == max(ctr_float_list):
                return "<td bgcolor='#e6ffe6'><b><u>"+str(round(ctr_val,3))+" %</b></u>"
            else:
                return "<td>" + str(round(ctr_val,3)) + " % </td>"
            

        except (ValueError, IndexError) as e:
            return ""


        
def awt(id):
    if id not in videoid_list:
        return ""
    else:
        awt_int_list =[]
        for i in awt_list:
            try:
                awt_int_list.append(int(i))
            except ValueError:
                awt_int_list.append(0)


        try:
            awt_val = int(awt_list[id_to_index(id)])

            if awt_val == max(awt_int_list):
                return "<td bgcolor='#e6ffe6'><b><u>"+str(awt_val)+" sec</b></u>"
            else:
                return "<td>" + str(awt_val) + " sec </td>"
            

        except (ValueError, IndexError) as e:
            return ""
        
def result_rate(id):
    if id not in videoid_list:
        return ""
    else:
        result_float_list =[]
        for i in result_rate_list:
            try:
                result_float_list.append(float(i))
            except ValueError:
                result_float_list.append(0.0)


        try:
            result_val = float(result_rate_list[id_to_index(id)])

            if result_val == max(result_float_list):
                return "<td bgcolor='#e6ffe6'><b><u>"+str(round(result_val,3))+" %</b></u>"
            else:
                return "<td>" + str(round(result_val,3)) + " % </td>"
            

        except (ValueError, IndexError) as e:
            return ""

        
def engagement_rate(id):
    if id not in videoid_list:
        return ""
    else:
        return engagement_rate_list[id_to_index(id)]

def awt_3sec(id):
    if id not in videoid_list:
        return ""
    else:
        awt_3sec_float_list =[]
        for i in awt_3sec_list:
            try:
                awt_3sec_float_list.append(float(i))
            except ValueError:
                awt_3sec_float_list.append(0.0)


        try:
            awt_3sec_val = float(awt_3sec_list[id_to_index(id)])

            if awt_3sec_val == max(awt_3sec_float_list):
                return "<td bgcolor='#b3d1ff'><b><u>"+str(round(awt_3sec_val,3))+" %</b></u>"
            else:
                return "<td>" + str(round(awt_3sec_val,3)) + " % </td>"
            

        except (ValueError, IndexError) as e:
            return ""

def awt_10sec(id):
    if id not in videoid_list:
        return ""
    else:
        awt_10sec_float_list =[]
        for i in awt_10sec_list:
            try:
                awt_10sec_float_list.append(float(i))
            except ValueError:
                awt_10sec_float_list.append(0.0)


        try:
            awt_10sec_val = float(awt_10sec_list[id_to_index(id)])

            if awt_10sec_val == max(awt_10sec_float_list):
                return "<td bgcolor='#b3d1ff'><b><u>"+str(round(awt_10sec_val,3))+" %</b></u>"
            else:
                return "<td>" + str(round(awt_10sec_val,3)) + " % </td>"
            

        except (ValueError, IndexError) as e:
            return ""

def engagement_rate_facebook(id):
    if id not in videoid_list:
        return ""
    else:
        engagement_rate_facebook_float_list =[]
        for i in engagement_rate_facebook_list:
            try:
                engagement_rate_facebook_float_list.append(float(i))
            except ValueError:
                engagement_rate_facebook_float_list.append(0.0)


        try:
            engagement_rate_facebook_val = float(engagement_rate_facebook_list[id_to_index(id)])

            if engagement_rate_facebook_val == max(engagement_rate_facebook_float_list):
                return "<td bgcolor='#ffffb3'><b><u>"+str(round(engagement_rate_facebook_val,3))+" %</b></u>"
            else:
                return "<td>" + str(round(engagement_rate_facebook_val,3)) + " % </td>"
            

        except (ValueError, IndexError)as e:
            return ""

def engagement_rate_social(id):
    if id not in videoid_list:
        return ""
    else:
        engagement_rate_social_float_list =[]
        for i in engagement_rate_social_list:
            try:
                engagement_rate_social_float_list.append(float(i))
            except ValueError:
                engagement_rate_social_float_list.append(0.0)


        try:
            engagement_rate_social_val = float(engagement_rate_social_list[id_to_index(id)])

            if engagement_rate_social_val == max(engagement_rate_social_float_list):
                return "<td bgcolor='#ffffb3'><b><u>"+str(round(engagement_rate_social_val,6))+" %</b></u>"
            else:
                return "<td>" + str(round(engagement_rate_social_val,6)) + " % </td>"
            

        except (ValueError, IndexError) as e:
            return ""


if len(videoid_list) is not len(set(videoid_list)):
    raise ValueError("the csv file contains more than one entry for the same 'Ad Name'")


videoid_list_from_cwd = []
for video_id_filename in os.listdir(dirpath):
    videoid_list_from_cwd.append(os.path.splitext(video_id_filename)[0])

for videoid in videoid_list:
    if videoid not in [v.lower() for v in videoid_list_from_cwd]:
        raise ValueError("the csv file contains some AdName for video not in the folder. Maybe it's the wrong CSV?")


table_head = """
  <!DOCTYPE html><html><head><meta charset="utf-8"><title>""" + html_file_name + """
  </title>

<style>

html *
{
   font-size: 1.04em !important;
   color: #000 !important;
   font-family: Arial !important;
}

table {
    border-collapse: collapse;
    }

tr {
    border-bottom: 1px solid;
    }

tr.spaceAbove>td {
  padding-top: 3em;
}

b.high-green {
    background-color: #e6ffe6;
}

.blank_row
{
    height: 10px !important; /* overwrites any other rules */
    background-color: #C8C8C8;
}

  </style>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
<table>
"""

table_html_list =["<tr><td>Video</td>",                 #0
"<tr><td>ID</td>",                                      #1
"<tr><td>Amount Spent</td>",                            #2
"<tr class='blank_row'><td colspan='42'></td></tr>",     #3 blank line
"<tr><td>CTR</td>",                                     #4
"<tr><td>Avg. watch time</td>",                         #5
"<tr><td>Result rt</td>",                               #6
"<tr class='blank_row'><td colspan='42'></td></tr>",     #7 blank line
"<tr><td>Engagement rt <br> Facebook</td>",             #8
"<tr><td>Engagement rt <br> Social media</td>",         #9
"<tr><td>Engagement rt</td>",                           #10
"<tr class='blank_row'><td colspan='42'></td></tr>",     #11 blank line
"<tr><td>3 sec video play</td>",                        #12
"<tr><td>10 sec video play</td>"                        #13
]


for video_file in sorted(os.listdir(dirpath)):
    if video_file.endswith(".mp4"):
        table_html_list[0]+="""<td><video width="480" height="480" autoplay controls muted loop>
        <source src="
        """ + video_file + """
        " type="video/mp4">
        </video> </td>"""
        video_id = os.path.splitext(video_file)[0]
        table_html_list[1]+="<td><b>"+video_id+"</b></td>"
        table_html_list[2]+=amount_spent(video_id.lower())
        table_html_list[4]+=ctr(video_id.lower())
        table_html_list[5]+=awt(video_id.lower()) #amount watch time
        table_html_list[6]+=result_rate(video_id.lower())
        table_html_list[10]+="<td>"+engagement_rate(video_id.lower())+"</td>"
        table_html_list[12]+=awt_3sec(video_id.lower())
        table_html_list[13]+=awt_10sec(video_id.lower())
        table_html_list[8]+=engagement_rate_facebook(video_id.lower())
        table_html_list[9]+=engagement_rate_social(video_id.lower())





table_tail = """</table>
</body>
</html>
"""

table_body=""

for row in table_html_list:
    table_body+=row+"</tr>"


html_str =table_head+table_body+table_tail




html_file= open(file_path,"w")
html_file.truncate(0)
html_file.write(html_str)
html_file.close()

