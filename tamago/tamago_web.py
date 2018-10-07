import logging
import flask
from threading import Thread
from waitress import serve

LOG = logging.getLogger(__name__)
app = flask.Flask('Tamgao-web')

@app.after_request
def web_logger(response):
    """
    log_the_status_code - prints logging status after every request
    param obj response: the response from a route for logging
    """
    LOG.info('%s %s %s %s', flask.request.remote_addr, flask.request.method,
                    flask.request.full_path, response.status)
    return response

@app.route('/')
def home():
    return flask.render_template('home.html')
    #return "I'm alive"

def run():
  #app.run(host='0.0.0.0',port=8080)
  LOG.info('RUNNING TAMAGO WEB')
  serve(app, port=8080, host='0.0.0.0')

def keep_alive():
    t = Thread(target=run)
    t.start()
