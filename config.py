import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Params:
    temp_dir: str
    logs_path: str
    temporary_html_doc: str
    temporary_json_all_press: str
    headers: dict
    pause_before_request: float
    errors_during_work: list
    results_path: str
    time_start_script: str
    document_types: dict
    chrome_driver_path: str
    username: str
    password: str


base_dir = Path(__file__).resolve().parent

temp_dir = os.path.join(base_dir, "Temp")
logs_path = os.path.join(base_dir, "logs")
temporary_html_doc = os.path.join(temp_dir, "temporary_html_doc.html")
temporary_json_all_press = os.path.join(temp_dir, "temporary_json_all_press.json")
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}
pause_before_request = 0.1
errors_during_work = []
results_path = os.path.join(base_dir, "results")
time_start_script = datetime.now().isoformat()
document_types = {
    "PRESS_RELEASE": "https://www.eestipank.ee/press/majanduskommentaarid/",
}
chrome_driver_path = os.path.join(base_dir, "Selenium_Driver\chromedriver.exe")
username = os.getenv('username')
password = os.getenv('password')

params = Params(temp_dir, logs_path, temporary_html_doc, temporary_json_all_press, headers, pause_before_request,
                errors_during_work, results_path, time_start_script, document_types, chrome_driver_path, username,
                password)


