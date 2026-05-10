import os, uuid, subprocess, requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
DOWNLOAD_DIR = "/tmp/acgolden"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
@app.route("/")
def health():
    return jsonify({"status": "AC Golden running"})
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL"}), 400
    video_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{video_id}.mp4"
    subprocess.run(["yt-dlp", "-o", output_path, url], timeout=120)
    return send_file(output_path, mimetype="video/mp4", as_attachment=True, download_name="clean.mp4")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000))
