import csv
import os
import argparse


parser = argparse.ArgumentParser(description='create a html page with videos from a directory')

parser.add_argument('path', type=str, help='name of the folder that we want to get the video from')

args = parser.parse_args()

if not os.path.exists(args.path):
    raise ValueError('the path doesnt exists')

html_file_name = os.path.basename(os.path.normpath(args.path)) + "_video_page.html"
file_path = args.path +"/"+ html_file_name



html_str = """
  <!DOCTYPE html><html><head><meta charset="utf-8"><title>""" + html_file_name + """
  </title><link rel="stylesheet" type="text/css" href="css/main.css"><meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
"""

table = "<table boreder=0>"
first_row ="<tr>"
second_row = "<tr>"


for video_file in os.listdir(args.path):
    if video_file.endswith(".mp4"):

        first_row+="""<td><video width="480" height="480" autoplay controls muted loop>
        <source src="
        """ + video_file + """
        " type="video/mp4">
        </video> </td>"""
        second_row+="<td>"+video_file+"</td>"




end = """</table>
</body>
</html>
"""

html_str +=table+first_row+second_row+end

html_file_name = os.path.basename(os.path.normpath(args.path)) + "_video_page.html"
file_path = args.path +"/"+ html_file_name


html_file= open(file_path,"w")
html_file.truncate(0)
html_file.write(html_str)
html_file.close()