import csv
from datetime import datetime
from io import StringIO
from flask import Flask, render_template, stream_with_context, make_response, request
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import pymongo
import urllib


mongo = pymongo.MongoClient('mongodb+srv://dbaqurds:' + urllib.parse.quote_plus('2252010baby@') + '@aqurds-ylkvj.mongodb.net/test?retryWrites=true', maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'dbqaurds')

app = Flask(__name__)


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Display route
@app.route('/result/')
def display():
    return render_template('result.html')


# data route for testing data in this app
@app.route('/data/')
def data():
    col = pymongo.collection.Collection(db, 'connect_mongo')
    result = col.find()
    col.insert({'asin': 'B01C89GCHU', 'site': 'com', 'price': '$19.99'})

    return render_template('data.html', dataresult=result)


# File upload route
@app.route('/upload_batch/', methods=["POST"])
def upload_batch():
    f = request.files['asin_file']
    if not f:
        return "No file"

    stream = StringIO(f.stream.read().decode("ISO-8859-1"), newline=None)
    csv_input = csv.reader(stream)

    for row in csv_input:
        # print(row)
        # result.append(row)
        col = pymongo.collection.Collection(db, 'asin_list_scrapped_done')
        if len(row[4]):
            col.insert({'main_asin': row[0], 'site': row[1], 'related_asin_one': row[2], 'related_asin_two': row[3], 'related_asin_three': row[4]})
        elif len(row[3]) and len(row[4]) == 0:
            col.insert({'main_asin': row[0], 'site': row[1], 'related_asin_one': row[2], 'related_asin_two': row[3]})
        else:
            col.insert({'main_asin': row[0], 'site': row[1], 'related_asin_one': row[2]})

    return render_template('data.html')



# Upload single asin route
@app.route('/upload_single_asin/', methods=["GET", "POST"])
def upload_single():
    main_asin = request.form['main_asin']
    site = request.form['site']
    re_asin_one = request.form['re_asin_one']
    re_asin_two = request.form['re_asin_two']
    re_asin_three = request.form['re_asin_three']

    col = pymongo.collection.Collection(db, 'asin_waiting_for_scrape')

    if len(re_asin_three):
        col.insert({'main_asin': main_asin, 'site': site, 'related_asin_one': re_asin_one, 'related_asin_two': re_asin_two, 'related_asin_three': re_asin_three})
    elif len(re_asin_two) and len(re_asin_three) == 0:
        col.insert({'main_asin': main_asin, 'site': site, 'related_asin_one': re_asin_one, 'related_asin_two': re_asin_two})
    else:
        col.insert({'main_asin': main_asin, 'site': site, 'related_asin_one': re_asin_one})


    return render_template('data.html',)








# example data, this could come from wherever you are storing logs
log = [
    ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298'),
    ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298'),
    ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298'),
    ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298')
]

@app.route('/dl/', methods=["GET", "POST"])
def download_asin_report():
    def generate():
        # get the form data with request object
        main_asin = request.form['main_asin_for_download']
        re_asin_one = request.form['re_asin_one_for_download']
        re_asin_two = request.form['re_asin_two_for_download']
        re_asin_three = request.form['re_asin_three_for_download']


        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('Asin', 'Site', 'Price', 'Reviews', 'Rating', 'Rank'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for item in log:
            w.writerow((
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5]
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='AsinReport.csv')

    # stream the response as the data is generated
    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )




if __name__ == '__main__':
    app.run(debug = True)
