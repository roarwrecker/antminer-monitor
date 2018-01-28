
import ipaddress
from flask import request, redirect, url_for
from app import app

@app.route('/')
def root():
    request_ip = request.remote_addr
    if ipaddress.ip_address(unicode(request_ip)).is_loopback:
        return redirect(url_for('details'))
    return redirect(url_for('temperature'))
