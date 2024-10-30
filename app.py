import os
import json
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
DATA_FILE = "books.json"
IMAGE_SIZE = (270, 180)  # Set the desired image size


def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_books(books):
    with open(DATA_FILE, "w") as file:
        json.dump(books, file)


books = load_books()


@app.route("/")
def home():
    sorted_books = sorted(books, key=lambda x: x["title"])
    return render_template("index.html", books=sorted_books)


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        photo = request.files["photo"]
        if photo:
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
            image = Image.open(photo)
            image = image.resize(IMAGE_SIZE)
            image.save(photo_path)
            books.append({"title": title, "author": author, "photo": photo.filename})
            save_books(books)
        return redirect(url_for("home"))
    return render_template("add_book.html")


@app.route("/delete/<int:book_id>")
def delete_book(book_id):
    if 0 <= book_id < len(books):
        del books[book_id]
        save_books(books)
    return redirect(url_for("home"))


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
