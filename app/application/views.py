"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
must be passed *username* as the argument.

"""
import json
import logging

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from decorators import login_required, admin_required

# Flask-Cache configured to use App Engine Memcache API
from application import app
from flask_cache import Cache
cache = Cache(app)

# Google API client
import httplib2
from apiclient.discovery import build
from oauth2client.appengine import AppAssertionCredentials

# BigQuery API Settings
BQ_SCOPE = 'https://www.googleapis.com/auth/bigquery'
BQ_PROJECT = 'skilled-acolyte-729'
BQ_DATASET = 'Flowreader'
BQ_TABLEID = 'data'

def home():
  return redirect(url_for('status'))

class serializable(object):
  def json(self):
    return json.dumps(self.__dict__)

class Data(serializable):
  rows = None
  done = None

  @property
  def todo(self):
    return None if self.done is None else self.rows - self.done

def getBigQueryService(scope=BQ_SCOPE):
  """Create a new API service for interacting with BigQuery
  """
  credentials = AppAssertionCredentials(scope=scope)
  http = credentials.authorize(httplib2.Http())
  return build('bigquery', 'v2', http=http)

@cache.cached(timeout=60*10)
def getRows():
  bq = getBigQueryService()
  td = bq.tables().get(projectId=BQ_PROJECT, datasetId=BQ_DATASET, tableId=BQ_TABLEID).execute()
  # logging.info(td.keys())
  return td['numRows']

@login_required
def status():
  data = Data()
  data.rows = getRows()
  return render_template('status.html', users=users, data=data)

@login_required
def sync_status():
  return ''


@admin_required
def sync():
  return ''


@admin_required
def sync_stop():
  return ''


def warmup():
  """App Engine warmup handler
  See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

  """
  return ''
