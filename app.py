from flask import Flask, render_template, jsonify, request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq


app = Flask(__name__)
CORS(app)
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route("/review", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_2pi5LC col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" +box.div.div.div.a['href']
            productRes = requests.get(productLink)

            prod_html = bs(productRes.text, "html.parser")
            commentboxes = prod_html.find_all("div", {"class": "_2wzgFH"})
            reviews=[]
            for comment in commentboxes:
                try:
                    name = comment.find_all("p", {"class":"_2sc7ZR"})[0].text
                except:
                    name = "No Name"
                try:
                    ratings = comment.find_all("div", {"class":"_1BLPMq"})[0].text
                except:
                    ratings = "No Rating"
                try:
                    commentHeading = comment.find_all("p", {"class":"_2-N8zT"})[0].text
                except:
                    commentHeading = "No Comment Heading"
                try:
                    comm = comment.find_all("div", {"class":""})
                    custComment = comm[0].div.text
                except:
                    custComment = "No customer Comment"

                myDict = {"Product": searchString, "Name": name, "Rating": ratings, "CommentHead": commentHeading, "Comment": custComment}
                reviews.append(myDict)
            return render_template('results.html', reviews=reviews)
        except:
            return "Something is Wrong"      
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(port=8000,debug=True)