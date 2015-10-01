#!/usr/bin/env python
#
# Copyright 2014 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import os
import re
import shlex
import socket
import subprocess
import time

import flask


app = flask.Flask(__name__, static_folder='static')
traceroute_bin = "/bin/traceroute-suid"


@app.route("/")
def icanhazafunction():
    if 'icanhazptr' in flask.request.host:
        # The request is for *.icanhazptr.com
        try:
            output = socket.gethostbyaddr(flask.request.remote_addr)
            result = output[0]
        except:
            result = flask.request.remote_addr
    elif 'icanhazepoch' in flask.request.host:
        epoch_time = int(time.time())
        result = epoch_time
    elif 'icanhaztrace' in flask.request.host:
        # The request is for *.icanhaztraceroute.com
        valid_ip = False
        try:
            socket.inet_pton(socket.AF_INET, flask.request.remote_addr)
            valid_ip = True
        except socket.error:
            pass
        try:
            socket.inet_pton(socket.AF_INET6, flask.request.remote_addr)
            valid_ip = True
        except socket.error:
            pass
        if valid_ip:
            if 'icanhaztraceroute' in flask.request.host:
                tracecmd = shlex.split("%s -q 1 -f 2 -w 1 %s" %
                    (traceroute_bin, flask.request.remote_addr))
            else:
                tracecmd = shlex.split("%s -q 1 -f 2 -w 1 -n %s" %
                    (traceroute_bin, flask.request.remote_addr))
            result = subprocess.Popen(tracecmd,
                stdout=subprocess.PIPE).communicate()[0].strip()
        else:
            result = flask.request.remote_addr
    elif 'icanhazproxy' in flask.request.host:
        proxy_headers = ['via', 'x-forwarded-for', 'forwarded', 'client-ip',
            'useragent_via', 'proxy_connection', 'xproxy_connection',
            'http_pc_remote_addr', 'http_client_ip',
            'http_x_appengine_country']
        found_headers = {}
        for header in proxy_headers:
            value = flask.request.headers.get(header, None)
            if value:
                found_headers[header] = value.strip()
        if len(found_headers) > 0:
            result = json.dumps(found_headers)
        else:
            return flask.Response(""), 204
    else:
        # The request is for *.icanhazip.com or something we don't recognize
        result = flask.request.remote_addr
    return flask.Response("%s\n" % result, mimetype="text/plain")


@app.route('/crossdomain.xml')
@app.route('/humans.txt')
@app.route('/robots.txt')
def static_from_root():
    return flask.send_from_directory(app.static_folder, flask.request.path[1:])


if __name__ == "__main__":
    app.run()
