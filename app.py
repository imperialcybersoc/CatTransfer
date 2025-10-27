from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import sys
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = os.environ.get("LOG_DIR")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "super_duper_secret_dev_log.txt")

sys.stdout = open(LOG_FILE, "a")
sys.stderr = open(LOG_FILE, "a")

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(handler)


app = Flask(__name__)
app.debug = True
app.secret_key = "very_very_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 6.7 * 1024 * 1024  # 6.7 MB
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "zip", "mp4", "doc", "docx"}
IMG_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_uploaded_files():
    files = []
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
            if os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
                files.append(filename)
    return files

@app.route("/")
def index():
    uploaded_files = get_uploaded_files()
    return render_template("index.html", uploaded_files=uploaded_files)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file selected", "error")
        return redirect(url_for("index"))
    
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("index"))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        if os.path.exists(filepath):
            flash(f"File already exists: {filename}", "error")
            return redirect(url_for("index"))
        
        file.save(filepath)
        flash(f"File uploaded successfully!", "success")
        
        return redirect(url_for("view_file", file=f"uploads/{filename}"))
    
    return redirect(url_for("index"))

@app.route("/serve")
def serve_file():
    file_path = request.args.get("file_path", "")
    try:
        return send_file(file_path)
    except:
        return "File not found", 404

@app.route("/view")
def view_file():
    file_path = request.args.get("file", "")
    file_content = ""
    error = ""
    is_image = is_binary = False
    
    if file_path:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in IMG_EXTENSIONS:
            is_image = True
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                is_binary = True
                with open(file_path, "rb") as f:
                    file_content = f.read()

                    hex_lines = []
                    for i in range(0, min(len(file_content), 512), 16):
                        hex_part = " ".join(f"{b:02x}" for b in file_content[i:i+16])
                        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in file_content[i:i+16])
                        hex_lines.append(f"{i:08x}  {hex_part:<48}  {ascii_part}")
                    file_content = "\n".join(hex_lines)
                    if len(file_content) >= 512:
                        file_content += "\n\n... (showing first 512 bytes)"
    
    uploaded_files = get_uploaded_files()
    return render_template("view.html", 
                         uploaded_files=uploaded_files,
                         file_content=file_content,
                         error=error,
                         file_path=file_path,
                         is_image=is_image,
                         is_binary=is_binary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
