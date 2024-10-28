from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

books = []


@app.route("/")
def home():
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        photo = request.files["photo"]
        if photo:
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
            photo.save(photo_path)
            books.append({"title": title, "author": author, "photo": photo.filename})
        return redirect(url_for("home"))
    return render_template("add_book.html")


@app.route("/delete/<int:book_id>")
def delete_book(book_id):
    if 0 <= book_id < len(books):
        del books[book_id]
    return redirect(url_for("home"))


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
