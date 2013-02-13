# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR
# PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.

"""
Shared support for integration tests.
"""

import json
import logging
from multiprocessing import Process
import requests
from requests.exceptions import RequestException
from unittest import TestCase

import flask


class FakeYammerServer(object):
    """
    A Flask-based web server that simulates the Yammer API by returning
    static JSON data that has a similar structure to the real API's responses.

    The server runs on port 5000.
    """

    def __init__(self):
        """
        Creates the server and defines the various routes.
        """
        self._server = flask.Flask("FakeYammerServer")
        self._silence_logger()

        @self._server.route("/up")
        def up():
            """
            Not part of the Yammer API: This route is polled by the main
            process to determine when the server process is ready.
            """
            return "Server is up"

        @self._server.route("/oauth2/access_token.json")
        def access_token():
            return """{"access_token": {"token": "valid_token"}}"""

        @self._server.route("/api/v1/messages.json", methods=["GET"])
        def messages():
            return self._message_list_json(
                count=3,
                first_id=1,
            )

        @self._server.route("/api/v1/messages.json", methods=["POST"])
        def post_message():
            return self._message_list_json(
                count=1,
                first_id=4,
                body=flask.request.args.get("body"),
            )

        @self._server.route("/api/v1/messages/<id>.json", methods=["DELETE"])
        def delete_message(id):
            return " "

        @self._server.route(
            "/api/v1/messages/liked_by/current.json",
            methods=["POST", "DELETE"],
        )
        def like_or_unlike_message():
            if "message_id" in flask.request.args:
                return " "
            else:
                return " ", 400

        @self._server.route("/api/v1/users.json", methods=["GET"])
        def users():
            return self._user_list_json(count=3, first_id=1)

        @self._server.route("/api/v1/users.json", methods=["POST"])
        def create_user():
            return self._user_json(
                user_id=4,
                first_name=flask.request.args.get("first_name"),
                last_name=flask.request.args.get("last_name"),
            )

        @self._server.route("/api/v1/users/current.json", methods=["GET"])
        def current_user():
            return self._user_json(
                user_id=1,
                first_name="Joe",
                last_name="Bloggs",
            )

        @self._server.route("/api/v1/users/<user_id>.json", methods=["GET"])
        def user(user_id):
            return self._user_json(
                user_id=int(user_id),
                first_name="John",
                last_name="Doe",
            )

        @self._server.route("/api/v1/users/<user_id>.json", methods=["PUT"])
        def update_user(user_id):
            return " "

        @self._server.route("/api/v1/users/<user_id>.json", methods=["DELETE"])
        def delete_user(user_id):
            return " "

    def run_as_process(self):
        """
        Spawns the fake Yammer API server in a new process. Does not return
        until the server is ready to handle requests.
        """
        self._process = Process(target=self._server.run)
        self._process.start()
        self._poll_until_server_responds()

    def stop_process(self):
        """
        Stops the fake Yammer API server's process.
        """
        if hasattr(self, "_process"):
            self._process.terminate()
            self._process.join()

    def _message_list_json(self, count=1, first_id=1, body="Hello world"):
        id_range = xrange(first_id, first_id + count)
        messages = [self._message_dict(msg_id, body) for msg_id in id_range]
        return json.dumps({
            "messages": messages,
            "references": [],
            "meta": [],
        })

    def _message_dict(self, msg_id, body):
        return {
            "id": msg_id,
            "body": {
                "plain": body,
                "parsed": body,
                "rich": body,
            }
        }

    def _user_list_json(self, count=1, first_id=1,
                        first_name="John", last_name="Doe"):
        id_range = xrange(first_id, first_id + count)
        users = [self._user_dict(user_id, first_name, last_name) for user_id in id_range]
        return json.dumps(users)

    def _user_json(self, *args, **kwargs):
        return json.dumps(self._user_dict(*args, **kwargs))

    def _user_dict(self, user_id, first_name, last_name):
        return {
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": "%s %s" % (first_name, last_name),
        }

    def _poll_until_server_responds(self):
        try:
            requests.get("http://localhost:5000/up", timeout=0.1)
        except RequestException:
            self._poll_until_server_responds()

    def _silence_logger(self):
        # The info messages from the Flask server are generate by
        # Werkzeug. Increasing its log level silences them.
        logging.getLogger("werkzeug").setLevel(logging.ERROR)


class TestCaseWithFakeYammerServer(TestCase):
    """
    A TestCase that sets up and tears down a FakeYammerServer.

    Subclasses that need to define their own setUp and tearDown methods
    must call the superclass implementations.
    """
    def setUp(self):
        try:
            self._fake_yammer_server = FakeYammerServer()
            self._fake_yammer_server.run_as_process()
        except:
            if hasattr(self, "_fake_yammer_server"):
                self._fake_yammer_server.stop()
            raise

    def tearDown(self):
        self._fake_yammer_server.stop_process()
