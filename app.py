from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)

# Ensure persistent data directory exists
base_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

db_path = os.path.join(data_dir, "visits.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128), nullable=False)
    reversed_ip = db.Column(db.String(128), nullable=False)
    ts = db.Column(db.DateTime, default=datetime.utcnow)

def extract_client_ip(flask_request):
    xff = flask_request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    real_ip = flask_request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    return flask_request.remote_addr or "unknown"

def reverse_ip(ip):
    if not ip or ip.lower() == "unknown":
        return ip
    m = re.search(r"(?:(?:\:\:ffff\:)?)(\d{1,3}(?:\.\d{1,3}){3})$", ip)
    if m:
        ipv4 = m.group(1)
        return '.'.join(reversed(ipv4.split('.')))
    if '.' in ip:
        return '.'.join(reversed(ip.split('.')))
    if ':' in ip:
        return ':'.join(reversed(ip.split(':')))
    return ip

# Ensure tables are created at startup
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    client_ip = extract_client_ip(request)
    reversed_ip_str = reverse_ip(client_ip)
    v = Visit(ip=client_ip, reversed_ip=reversed_ip_str)
    db.session.add(v)
    db.session.commit()
    visits = Visit.query.order_by(Visit.ts.desc()).limit(50).all()
    return render_template("index.html", ip=client_ip, reversed_ip=reversed_ip_str, visits=visits)

@app.route("/clear", methods=["POST"])
def clear():
    Visit.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/healthz")
def healthz():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
