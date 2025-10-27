from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route("/")
def admin_index():
    flag = open("/root/omds_its_a_flag.txt").read().strip()
    return render_template("admin.html", flag=flag)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python admin.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    app.run(host="0.0.0.0", port=port, debug=True)
