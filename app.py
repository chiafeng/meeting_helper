#!/usr/bin/env python3
import os
from flask import Flask, request, render_template

app = Flask(__name__)

app_root = os.path.dirname(os.path.abspath(__file__))
# path for uploaded files
file_dir = app_root + "/files"

# first page
@app.route("/")
def index():
	# show html template
	return render_template("index.html")

# result page when user upload their files
@app.route("/result", methods=['POST'])
def result():
	# check file_dir
	if not os.path.isdir(file_dir):
		os.mkdir(file_dir)

	# save uploaded file
	file = request.files.get("file")		# use getlist("file") to get multiple files
	dest = file_dir + "/" + file.filename
	#print(dest)
	file.save(dest)

	# pass file path to my function
	res = myfun(dest)

	# return result on web page (HTML format)
	return res

# process the file here
def myfun(filepath):
	return "Your file is at " + filepath

if __name__ == "__main__":
	# start up the web server
	app.run(port=8080, debug=True)