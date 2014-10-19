"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home, methods=['GET'])

# Status page
app.add_url_rule('/status', 'status', view_func=views.status, methods=['GET'])

# API
app.add_url_rule('/api/sync', view_func=views.sync, methods=['POST'])
app.add_url_rule('/api/sync/stop', view_func=views.sync_stop, methods=['POST'])
app.add_url_rule('/api/sync/status', view_func=views.sync_status, methods=['GET'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
