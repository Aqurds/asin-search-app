import csv
from datetime import datetime
from io import StringIO
from flask import Flask, render_template, stream_with_context, make_response, request, redirect, url_for
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import pymongo
import urllib


mongo = pymongo.MongoClient('mongodb+srv://dbaqurds:' + urllib.parse.quote_plus('2252010baby@') + '@aqurds-ylkvj.mongodb.net/test?retryWrites=true', connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, maxPoolSize=1, connect=False)
db = pymongo.database.Database(mongo, 'dbqaurds')

app = Flask(__name__)


# Home route
@app.route('/')
def home():
    message = ""
    if request.args:
        message = request.args['message']
    return render_template('index.html', message=message)


# Display route
@app.route('/result/', methods=["GET", "POST"])
def display():
    asin_query_from_search_page = ''
    asin_query_from_home_page = ''
    main_asin = ''
    site = ''
    re_asin_one = ''
    re_asin_two = ''
    re_asin_three = ''
    main_asin_result = ''
    re_asin_one_result = ''
    re_asin_two_result = ''
    re_asin_three_result = ''

    if request.method == "GET":
        # search query code for result page search form
        if "asin_search_from_result_page" in request.args:
            if request.args["asin_search_from_result_page"]:
                asin_query_from_search_page = request.args["asin_search_from_result_page"]
                #query the database with the searched asin and show the result in result page
                col = pymongo.collection.Collection(db, 'asin_list_scrapped_done')
                result = list(col.find({'main_asin': asin_query_from_search_page}))
                # if the searched asin in our database, then show result, else redirect to the result page with alert message
                if result:
                    # as the asin is in our database, then start query
                    asin_list = result.pop(0)
                    main_asin = asin_list['main_asin']
                    site = asin_list['site']
                    re_asin_one = asin_list['related_asin_one']
                    if len(asin_list) > 4:
                        re_asin_two = asin_list['related_asin_two']
                    if len(asin_list) == 6:
                        re_asin_three = asin_list['related_asin_three']
                    # now i got all asins from asin list from our database, now I will query for each asin in our asin_result database to get all the details for each asin
                    col = pymongo.collection.Collection(db, 'asin_scraped_result')
                    main_asin_result = list(col.find({'asin': main_asin})).pop(0)
                    re_asin_one_result = list(col.find({'asin': re_asin_one})).pop(0)
                    if re_asin_two:
                        re_asin_two_result = list(col.find({'asin': re_asin_two})).pop(0)
                    if re_asin_three:
                        re_asin_three_result = list(col.find({'asin': re_asin_three})).pop(0)

                else:
                    # no result found with searched asin, redirect to result page with alert message
                    message = "No result found with your searched ASIN! Please try another one!"
                    return redirect(url_for('display', message = message))
            # If the form sent as empty, then it will redirect to result page with alert message
            else:
                message = "Please, fill the search box with a valid ASIN!"
                return redirect(url_for('display', message = message))

         # search query for asin comes from add box related asin add box
        if "main_asin_add_form_one" in request.args:
             main_asin = request.args['main_asin_add_form_one']
             if "re_asin_one_add_form_one" in request.args:
                 re_asin_one = request.args['re_asin_one_add_form_one']
             if "re_asin_two_add_form_one" in request.args:
                 re_asin_two = request.args['re_asin_two_add_form_one']
             if "re_asin_three_add_form_one" in request.args:
                 re_asin_three = request.args['re_asin_three_add_form_one']
             col = pymongo.collection.Collection(db, 'asin_scraped_result')
             main_asin_result = list(col.find({'asin': main_asin})).pop(0)
             re_asin_one_result = list(col.find({'asin': re_asin_one})).pop(0)
             if re_asin_two:
                 re_asin_two_result = list(col.find({'asin': re_asin_two})).pop(0)
             if re_asin_three:
                 re_asin_three_result = list(col.find({'asin': re_asin_three})).pop(0)

        # search query for asin comes from edit box
        if "main_asin_from_edit_box_one" in request.args:
            main_asin = request.args['main_asin_from_edit_box_one']
            if "re_asin_one_from_edit_box_one" in request.args:
                re_asin_one = request.args['re_asin_one_from_edit_box_one']
            if "re_asin_two_from_edit_box_one" in request.args:
                re_asin_two = request.args['re_asin_two_from_edit_box_one']
            if "re_asin_three_from_edit_box_one" in request.args:
                re_asin_three = request.args['re_asin_three_from_edit_box_one']
            col = pymongo.collection.Collection(db, 'asin_scraped_result')
            main_asin_result = list(col.find({'asin': main_asin})).pop(0)
            re_asin_one_result = list(col.find({'asin': re_asin_one})).pop(0)
            if re_asin_two:
                re_asin_two_result = list(col.find({'asin': re_asin_two})).pop(0)
            if re_asin_three:
                re_asin_three_result = list(col.find({'asin': re_asin_three})).pop(0)



         # # search query for asin comes from add box related asin add box
         # if "main_asin_add_form_one" in request.args:
         #     main_asin = request.args['main_asin_add_form_one']
         #     if "re_asin_one_add_form_one" in request.args:
         #         re_asin_one = request.args['re_asin_one_add_form_one']
         #     if "re_asin_two_add_form_one" in request.args:
         #         re_asin_two = request.args['re_asin_two_add_form_one']
         #     if "re_asin_three_add_form_one" in request.args:
         #         re_asin_three = request.args['re_asin_three_add_form_one']
         #     col = pymongo.collection.Collection(db, 'asin_scraped_result')
         #     main_asin_result = list(col.find({'asin': main_asin})).pop(0)
         #     re_asin_one_result = list(col.find({'asin': re_asin_one})).pop(0)
         #     if re_asin_two:
         #         re_asin_two_result = list(col.find({'asin': re_asin_two})).pop(0)
         #     if re_asin_three:
         #         re_asin_three_result = list(col.find({'asin': re_asin_three})).pop(0)


    if request.method == 'POST':
        # # search query code for result page search form
        # if request.form.get("asin_search_from_result_page"):
        #     if request.form.get("asin_search_from_result_page"):
        #         asin_query_from_search_page = request.form.get("asin_search_from_result_page")
        #         #query the database with the searched asin and show the result in result page
        #         col = pymongo.collection.Collection(db, 'asin_list_scrapped_done')
        #         result = list(col.find({'main_asin': asin_query_from_search_page}))
        #         # if the searched asin in our database, then show result, else redirect to the result page with alert message
        #         if result:
        #             # as the asin is in our database, then start query
        #             asin_list = result.pop(0)
        #             main_asin = asin_list['main_asin']
        #             site = asin_list['site']
        #             re_asin_one = asin_list['related_asin_one']
        #             if len(asin_list) > 4:
        #                 re_asin_two = asin_list['related_asin_two']
        #             if len(asin_list) == 6:
        #                 re_asin_three = asin_list['related_asin_three']
        #             # now i got all asins from asin list from our database, now I will query for each asin in our asin_result database to get all the details for each asin
        #             col = pymongo.collection.Collection(db, 'asin_scraped_result')
        #             main_asin_result = list(col.find({'asin': main_asin})).pop(0)
        #             re_asin_one_result = list(col.find({'asin': re_asin_one})).pop(0)
        #             if re_asin_two:
        #                 re_asin_two_result = list(col.find({'asin': re_asin_two})).pop(0)
        #             if re_asin_three:
        #                 re_asin_three_result = list(col.find({'asin': re_asin_three})).pop(0)
        #
        #         else:
        #             # no result found with searched asin, redirect to result page with alert message
        #             message = "No result found with your searched ASIN! Please try another one!"
        #             return redirect(url_for('display', message = message))
        #     # If the form sent as empty, then it will redirect to result page with alert message
        #     else:
        #         message = "Please, fill the search box with a valid ASIN!"
        #         return redirect(url_for('display', message = message))



        # search query code for home page search form
        if request.form.get("asin_search_from_home_page"):
            asin_query_from_home_page = request.form.get("asin_search_from_home_page")
            #query the database with the searched asin and show the result in result page
            col = pymongo.collection.Collection(db, 'asin_list_scrapped_done')
            result = list(col.find({'main_asin': asin_query_from_home_page}))
            # if the searched asin in our database, then show result, else redirect to the result page with alert message
            if result:
                # as the asin is in our database, then start query
                asin_list = result.pop(0)
                main_asin = asin_list['main_asin']
                site = asin_list['site']
                re_asin_one = asin_list['related_asin_one']
                if len(asin_list) > 4:
                    re_asin_two = asin_list['related_asin_two']
                if len(asin_list) == 6:
                    re_asin_three = asin_list['related_asin_three']
                # now i got all asins from asin list from our database, now I will query for each asin in our asin_result database to get all the details for each asin
                col = pymongo.collection.Collection(db, 'asin_scraped_result')
                main_asin_result = list(col.find({'asin': main_asin})).pop(0)
                re_asin_one_result = list(col.find({'asin': re_asin_one})).pop(0)
                if re_asin_two:
                    re_asin_two_result = list(col.find({'asin': re_asin_two})).pop(0)
                if re_asin_three:
                    re_asin_three_result = list(col.find({'asin': re_asin_three})).pop(0)

            else:
                # no result found with searched asin, redirect to home page with alert message
                message = "No result found with your searched ASIN! Please try another one!"
                return redirect(url_for('home', message = message))

        # If the form sent as empty, then it will redirect to home page with alert message
        else:
            message = "Please, fill the search box with a valid ASIN!"
            return redirect(url_for('home', message = message))

    message = ""
    if request.args:
        if "message" in request.args:
            message = request.args['message']

    return render_template('result.html', main_asin = main_asin, site = site, re_asin_one = re_asin_one, re_asin_two = re_asin_two, re_asin_three = re_asin_three, main_asin_result=main_asin_result, re_asin_one_result=re_asin_one_result, re_asin_two_result=re_asin_two_result, re_asin_three_result=re_asin_three_result, message=message)


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
    if request.method == "post":
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


    return redirect(url_for('display'))








# example data, this could come from wherever you are storing logs
# log = [
#     ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298'),
#     ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298'),
#     ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298'),
#     ('B01NAWKYZ0', 'com', '$19.99', 198, 4.9, '#298')
# ]

@app.route('/dl/', methods=["GET", "POST"])
def download_asin_report():
    if request.method == "POST":
        main_asin = request.form.get('main_asin_for_download')
        re_asin_one = ''
        if request.form.get('re_asin_one_for_download'):
            re_asin_one = request.form.get('re_asin_one_for_download')
        re_asin_two = ''
        if request.form.get('re_asin_two_for_download'):
            re_asin_two = request.form.get('re_asin_two_for_download')
        re_asin_three = ''
        if request.form.get('re_asin_three_for_download'):
            re_asin_three = request.form.get('re_asin_three_for_download')
        result = []

        col = pymongo.collection.Collection(db, 'asin_scraped_result')
        result.append(list(col.find({'asin': main_asin})))
        if re_asin_one:
            result.append(list(col.find({'asin': re_asin_one})))
        if re_asin_two:
            result.append(list(col.find({'asin': re_asin_two})))
        if re_asin_three:
            result.append(list(col.find({'asin': re_asin_three})))

        # return render_template('data.html', main_asin=result)
        def generate():
            # get the form data with request object


            data = StringIO()
            w = csv.writer(data)

            # write header
            w.writerow(('Asin', 'Price', 'Reviews', 'Rating', 'Rank'))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

            # write each log item
            for item in result:
                for val in item:
                    w.writerow((
                        val['asin'],
                        val['price'],
                        val['number_of_comments'],
                        val['ratings'],
                        val['ranking']
                    ))
                    yield data.getvalue()
                    data.seek(0)
                    data.truncate(0)

            # for item in log:
            #     w.writerow((
            #         item[0],
            #         item[1],
            #         item[2],
            #         item[3],
            #         item[4],
            #         item[5]
            #     ))
            #     yield data.getvalue()
            #     data.seek(0)
            #     data.truncate(0)

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
