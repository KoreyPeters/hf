"""
gcloud config set project human-flourishing-4
gcloud builds submit --tag gcr.io/human-flourishing-4/supabase-webhooks && gcloud run deploy supabase-webhooks --platform managed --region us-central1 --image gcr.io/human-flourishing-4/supabase-webhooks --update-secrets=SECRETS=us-central1-prod:latest

"""

import os
import re
from functools import wraps

import pendulum
from flask import Flask
from flask import request as flask_request
from google.protobuf import timestamp_pb2

app = Flask("v--dsm")


class Environment:
    def __init__(self, secrets=None):
        self.data = {}
        if secrets:
            items = re.split("\n| ", secrets)
            for item in items:
                k, v = item.split("=", 1)
                self.data[k.strip()] = v.strip()

    def get(self, key, default=None):
        value = self.data.get(key, default)
        if value:
            return value
        else:
            return os.environ.get(key, default)


ENV = Environment(os.environ.get("SECRETS"))


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = flask_request.headers.get("Authorization")
        if token and token == ENV.get("CLOUD_RUN_APIKEY"):
            return f(*args, **kwargs)
        return {}, 401

    return decorated_function


@app.route("/activity-webhook", methods=["POST"])
@token_required
def activity_webhook():
    data = flask_request.get_json()
    print(data)
    return {}


@app.route("/survey-response", methods=["POST"])
@token_required
def survey_response_supabase_webhook():
    """
    This function call will create a Cloud Task to update the score of the surveyed entity.

    The Cloud Task will be deferred to the top of the hour. All Cloud Task names will have this timestamp in
    them to "debounce" multiple survey responses since the Cloud Task queue will reject tasks with duplicate
    IDs.
    """
    next_run = (pendulum.now("UTC") + pendulum.duration(hours=1)).start_of("hour")
    delay_seconds = (next_run - pendulum.now("UTC")).seconds

    url = f"https://hf-cncfwwwe3q-uc.a.run.app/survey-response"
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(next_run)
    # try:
    #     task_client.create_task(
    #         request={
    #             "parent": task_client.queue_path(project_name, region, queue),
    #             "task": {
    #                 "http_request": {
    #                     "http_method": tasks_v2.HttpMethod.POST,
    #                     "url": url,
    #                     "headers": {"Content-Type": "application/json"},
    #                     "body": json.dumps(data, cls=DateEncoder).encode(),
    #                     "oidc_token": {
    #                         "audience": url,
    #                         "service_account_email": service_account_email,
    #                     },
    #                 },
    #                 "name": task_client.task_path(
    #                     project_name, region, queue, task_name
    #                 ),
    #                 "schedule_time": timestamp,
    #             },
    #         }
    #     )
    # except google.api_core.exceptions.AlreadyExists:
    #     print(f"That task already existed. Skipping... {task_name}")
    return {}


@app.route("/update-entity-score", methods=["POST"])
@token_required
def update_entity_score():
    """
    This function call will query Supabase for all SurveyResponse rows that refer to this Entity.

    It will then calculate a new value for the Entity and store it to Supabase.
    """
    return {}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
