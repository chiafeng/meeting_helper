#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for async
batch processing.

Example usage:
    python transcribe_async.py resources/audio.raw
    python transcribe_async.py gs://cloud-samples-tests/speech/vr.flac
"""

import argparse
import io
import datetime
import pprint

from google.cloud import storage

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    full_text = ""
    try:
        client = speech.SpeechClient()

        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='en-US')
            #language_code='cmn-Hant-TW')

        operation = client.long_running_recognize(config, audio)

        print('Waiting for operation to complete...')
        response = operation.result(timeout=600)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.

        all_section = []
        for result in response.results:
            try:
                # The first alternative is the most likely one for this portion.
                all_section.append(result.alternatives[0].transcript)
                #print(u'{}'.format(result.alternatives[0].transcript))
                #print('Confidence: {}'.format(result.alternatives[0].confidence))
            except IndexError:
                # no alternatives inside
                print("Warn: no alternatives in this result")

        full_text = '\n'.join(all_section)

    except Exception as e:
        print(e)

    return full_text
# [END speech_transcribe_async_gcs]


if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        #transcribe_file(args.path)
    """
    gcs_header = "gs://"
    target_bucket = "speech_test_kyuc"
    target_blob_name = "2016_mono.wav"
    upload_blob(target_bucket, target_blob_name, target_blob_name)
    transcribe_gcs(gcs_header + target_bucket + '/' + target_blob_name)
