import json
import logging
import os
import smtplib
import subprocess
from datetime import datetime
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler
from pathlib import Path

import mysql.connector
import psutil
import requests

# ==============================
# CONFIGURATION
# ==============================

HTTPD_SERVICE = "httpd"
APP_SERVICE = "monapp"
DB_SERVICE = "mariadb"

APP_URL = "http://127.0.0.1/health"

MAX_RESTART = 3
CPU_THRESHOLD = 85
RAM_THRESHOLD = 85


# ==============================
# PATHS
# ==============================

BASE_DIR = Path(__file__).resolve().parent

LOG_DIR = BASE_DIR / "log" / "monitoring"
STATE_DIR = BASE_DIR / "state"

LOG_FILE = LOG_DIR / "monitoring.log"
STATE_FILE = STATE_DIR / "monitoring_state.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# LOGGER
# ==============================

logger = logging.getLogger("monitoring")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=14)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)


# ==============================
# ENV VARIABLES
# ==============================

# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
# EMAIL_SENDER = os.getenv("EMAIL_SENDER")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# ==============================
# STATE MANAGEMENT
# ==============================


def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


# ==============================
# SYSTEM CHECKS
# ==============================


def check_systemd(service):
    result = subprocess.run(
        ["systemctl", "is-active", service], capture_output=True, text=True
    )
    return result.stdout.strip()


def restart_service(service, state, issues):
    count = state.get(service, 0)

    if count >= MAX_RESTART:
        msg = f"{service} DOWN - limite restart atteinte ({MAX_RESTART})"
        issues.append(msg)
        logger.error(msg)
        return

    subprocess.run(["systemctl", "restart", service])
    state[service] = count + 1

    msg = f"{service} redémarré ({state[service]}/{MAX_RESTART})"
    issues.append(msg)
    logger.warning(msg)


# ==============================
# HTTP CHECK
# ==============================


def check_http():
    try:
        r = requests.get(APP_URL, timeout=5)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Erreur endpoint health: {e}")
        return False


# ==============================
# DATABASE CHECK
# ==============================


def check_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=5,
        )
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Connexion MariaDB échouée: {e}")
        return False


# ==============================
# SYSTEM RESOURCES
# ==============================


def check_resources(issues):
    cpu = psutil.cpu_percent(interval=2)
    ram = psutil.virtual_memory().percent

    if cpu > CPU_THRESHOLD:
        msg = f"CPU élevé : {cpu}%"
        issues.append(msg)
        logger.warning(msg)

    if ram > RAM_THRESHOLD:
        msg = f"RAM élevée : {ram}%"
        issues.append(msg)
        logger.warning(msg)

    return cpu, ram


# ==============================
# EMAIL
# ==============================

# def send_mail(subject, content):
#     try:
#         msg = EmailMessage()
#         msg["Subject"] = subject
#         msg["From"] = EMAIL_SENDER
#         msg["To"] = EMAIL_RECEIVER
#         msg.set_content(content)

#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#             server.send_message(msg)

#         logger.info("Email envoyé")

#     except Exception as e:
#         logger.error(f"Erreur envoi email: {e}")


# ==============================
# MAIN
# ==============================


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = load_state()
    issues = []

    logger.info("===== Début monitoring =====")

    # # Apache
    # if check_systemd(HTTPD_SERVICE) != "active":
    #     restart_service(HTTPD_SERVICE, state, issues)
    # else:
    #     state[HTTPD_SERVICE] = 0

    # Application
    # if check_systemd(APP_SERVICE) != "active":
    #     restart_service(APP_SERVICE, state, issues)
    # else:
    #     state[APP_SERVICE] = 0

    # MariaDB service
    # if check_systemd(DB_SERVICE) != "active":
    #     restart_service(DB_SERVICE, state, issues)
    # else:
    #     state[DB_SERVICE] = 0

    # DB check
    if not check_db_connection():
        issues.append("Connexion MariaDB impossible")

    # Endpoint check
    if not check_http():
        issues.append("Endpoint /health KO")

    # CPU / RAM
    cpu, ram = check_resources(issues)

    save_state(state)

    if issues:
        subject = "🚨 INCIDENT PRODUCTION"

        content = f"""
Date : {now}

Problèmes détectés :
{chr(10).join(issues)}

CPU : {cpu}%
RAM : {ram}%
"""

        logger.error("Incident détecté")

    else:
        subject = "✅ Rapport quotidien production"

        content = f"""
Date : {now}

Tous les services sont opérationnels.

CPU : {cpu}%
RAM : {ram}%
"""

        logger.info("Tous les services OK")

    # send_mail(subject, content)
    print(content)

    logger.info("===== Fin monitoring =====")


if __name__ == "__main__":
    main()
