from flask import Flask, render_template, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)
REPORT_PATH = "/app/reports"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    report_id = str(uuid.uuid4())
    report_file = f"{REPORT_PATH}/{report_id}.txt"
    
    try:
        # Run nuclei scan via Docker
        cmd = f"docker exec nuclei nuclei -u {url} -t /root/nuclei-templates/subdomain-finder.yaml -o {report_file}"
        subprocess.run(cmd, shell=True, check=True, timeout=300)
        
        return {"status": "success", "report_id": report_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/report/<report_id>')
def get_report(report_id):
    return send_file(f"{REPORT_PATH}/{report_id}.txt", mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
