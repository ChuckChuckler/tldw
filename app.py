from flask import Flask, jsonify, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi as ytapi
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyDwc7y7YOWaBlSopVLwRXmayN0jKGpvGVE")

app=Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/summarize", methods=["POST", "GET"])
def summarize():
    if not request.json:
        print("no request")
    elif "data" not in request.json:
        print("no data found")
    else:
        global model
        url = str(request.json["data"])
        url = url.replace("https://www.youtube.com/watch?v=", "")
        transcripts = ytapi.get_transcript(url)
        accTranscript = ""
        for i in transcripts:
            accTranscript += i["text"] + " "

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        safety_settings : list[str] = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]
        response = model.generate_content(
            [f"Given the following transcript: {accTranscript}, generate a short 8-10 sentence summary of the text."], 
            safety_settings=safety_settings
       )
        print(response)
        return jsonify({"message":"euge", "summary":response.text})


app.run(host="0.0.0.0", port=8080, debug=True)