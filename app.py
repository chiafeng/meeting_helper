#!/usr/bin/env python3
import os
from flask import Flask, request, render_template, jsonify

from audio2text import *
from keyword_extract import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

app_root = os.path.dirname(os.path.abspath(__file__))
# path for uploaded files
file_dir = app_root + "/files"

# first page
@app.route("/")
def index():
	# show html template
	return render_template("index.html")

@app.route("/process", methods=['GET'])
def process():
	dic = {"status": "processing...."}
	return jsonify(dic)

# result page when user upload their files
@app.route("/result", methods=['POST'])
def result():
	# check file_dir
	if not os.path.isdir(file_dir):
		os.mkdir(file_dir)

	# save uploaded file
	file = request.files.get("file")		# use getlist("file") to get multiple files
	dest = file_dir + "/" + file.filename
	print(dest)
	file.save(dest)

	# pass file path to my function
	page = service(dest)

	# return result on web page (HTML format)
	return page

# process the file here
def service(filepath):
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Test-4740e7bfcc1c.json"
	
	# upload file
	gcs_header = "gs://"
	target_bucket = "speech_test_kyuc"
	target_blob_name = os.path.basename(filepath)
	print("uploading...")
	upload_blob(target_bucket, filepath, target_blob_name)

	# transcribe to text
	gcs_link = gcs_header + target_bucket + '/' + target_blob_name
	print(gcs_link)
	print("transcribing to text...")
	import time
	start = time.time()
	text = transcribe_gcs(gcs_link)
	end = time.time()
	print("cost time: {}s".format(end - start))
	if len(text) == 0:
		print("Warn: No text from audio!!")
	print(text)

	# extract entity from text
	print("extracting entity...")
	entities = entities_text(text)

	# prepare data for wordcloud
	mapping = []
	entity_pool = set()
	js_list = "[]"
	if entities is not None:
		for entity in entities:
			# remove duplicates and single word
			if len(entity.name) > 1 and entity.name not in entity_pool:
				entity_pool.add(entity.name)
				mapping.append([entity.name, entity.salience * 100])
		js_list = repr(mapping)
	print(js_list)
	page_text = text.replace('\n', '<br/>')

	print("Done")

	# show html template
	return render_template("result.html", mapping=js_list, origin_text=page_text)
	
if __name__ == "__main__":
	# start up the web server
	app.run(host='0.0.0.0', port=80, debug=True)