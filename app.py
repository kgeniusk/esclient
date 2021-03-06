from elasticsearch import Elasticsearch
from config import CERT_FINGERPRINT, ELASTIC_PASSWORD, ELASTIC_USER, ELASTIC_HOST
from flask import Flask, request, render_template


app = Flask(__name__)

client = Elasticsearch(
    hosts=ELASTIC_HOST,
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/search')
def search():

    # doc = {
    #     'title': 'How to reset SSO password',
    #     'content': 'First visit the URL kmd.dealer-portal.net and click forgot password button!',
    #     'timestamp': dt.datetime.now()
    # }

    keyword = request.form['keyword']
    if keyword != '':
        r = client.search(index='mysales-handbuch',
                          query={"query_string": {'query': f'{keyword}'}},
                          highlight={'order': 'score', 'require_field_match': False, 'fields': {
                            'heading 1': {}, 'heading 2': {}, 'heading 3': {}, 'content': {}
                          }})
        hits = r.body.get('hits').get('hits')
        if hits:
            return render_template('hits.html', hits=hits, keyword=keyword)
    return 'No results'
