# cloudmersive_voicerecognition_api_client
Speech APIs enable you to recognize speech and convert it to text using advanced machine learning, and also to convert text to speech.

This Python package provides a native API client for [Cloudmersive Voice Recognition](https://cloudmersive.com/voice-recognition-and-speech-api)

- API version: v1
- Package version: 4.0.1
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import cloudmersive_voicerecognition_api_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import cloudmersive_voicerecognition_api_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import cloudmersive_voicerecognition_api_client
from cloudmersive_voicerecognition_api_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Apikey
configuration = cloudmersive_voicerecognition_api_client.Configuration()
configuration.api_key['Apikey'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Apikey'] = 'Bearer'

# create an instance of the API class
api_instance = cloudmersive_voicerecognition_api_client.RecognizeApi(cloudmersive_voicerecognition_api_client.ApiClient(configuration))
speech_file = '/path/to/file.txt' # file | Speech file to perform the operation on.  Common file formats such as WAV, MP3 are supported.

try:
    # Recognize audio input as text using machine learning
    api_response = api_instance.recognize_file(speech_file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RecognizeApi->recognize_file: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.cloudmersive.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*RecognizeApi* | [**recognize_file**](docs/RecognizeApi.md#recognize_file) | **POST** /speech/recognize/file | Recognize audio input as text using machine learning
*SpeakApi* | [**speak_post**](docs/SpeakApi.md#speak_post) | **POST** /speech/speak/text/basicVoice/{format} | Perform text-to-speech on a string
*SpeakApi* | [**speak_text_to_speech**](docs/SpeakApi.md#speak_text_to_speech) | **POST** /speech/speak/text/voice/basic/audio | Perform text-to-speech on a string


## Documentation For Models

 - [SpeechRecognitionResult](docs/SpeechRecognitionResult.md)
 - [TextToSpeechRequest](docs/TextToSpeechRequest.md)


## Documentation For Authorization


## Apikey

- **Type**: API key
- **API key parameter name**: Apikey
- **Location**: HTTP header


## Author



