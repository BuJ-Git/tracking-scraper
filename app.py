from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/track')
def track():
    carrier = request.args.get('carrier')
    tracking_number = request.args.get('tracking')

    if not carrier or not tracking_number:
        return 'Missing required parameters', 400

    if carrier == 'dpd':
        url = f"https://extranet.dpd.de/status/en_DE/parcel/{tracking_number}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        status = soup.select_one('.dpd-status__text')
        return status.text.strip() if status else 'DPD status not found'

    elif carrier == 'gls':
        postcode = request.args.get('postcode')
        if not postcode:
            return 'Postcode required for GLS', 400
        url = f"https://www.gls-pakete.de/en/reach-parcel-tracking?trackingNumber={tracking_number}&postCode={postcode}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        status = soup.select_one('.status-bubble__title')
        return status.text.strip() if status else 'GLS status not found'

    return 'Invalid carrier', 400
