# Turkish Sub Generator

This is a short program I wrote for my dad. It takes a video in english and tries it's best to generate Turkish subtitles for it.

The code is messy. This wasn't intended to be used by other people. I wrote it so long ago even I forget how it works.

You'll need IBM Watson credentials for transcription and Google Cloud credentials for translation if you want to use it (good luck). Put the IBM Watson credentials in a file named `speech_credentials.env`. I think Watson generates it for you, but just in case, it should look something like this:

```
SPEECH_TO_TEXT_APIKEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SPEECH_TO_TEXT_IAM_APIKEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SPEECH_TO_TEXT_URL=https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/your-instance-here
SPEECH_TO_TEXT_AUTH_TYPE=iam
```

I'm pretty sure Google also generates the credentials for you. Put them in `google-credentials.json`.

Good luck. If you're stuck you can open an issue I guess, but there is no guarantee I will respond because I did this project a while ago and I'm not really offering support. It's just on GitHub for documentation purposes.
