from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
#http://127.0.0.1:5000/add_author?name=Ali&specialisation=AI
#curl -X POST -H "Content-Type: application/json" -d '{"name":"Ted","specialisation":"it"}' http://127.0.0.1:5000/authors
"""
curl -X POST -H "Content-Type: application/json" -d '{"name":"Ted","specialisation":"it"}' http://127.0.0.1:5000/authors

curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Ted\",\"specialisation\":\"it\"}" http://127.0.0.1:5000/authors


curl -X PUT -H "Content-Type: application/json"  -d "{\"name\":\"Ted Updated\",\"specialisation\":\"AI\"}"  http://127.0.0.1:5000/authors/1
     
curl -X DELETE http://127.0.0.1:5000/authors/1

"""


app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

""" 
API_TOKEN = "YOUR_SECRET_TOKEN_HERE"

def require_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
"""


# -------------------- MODEL --------------------
class Authors(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialisation = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Author {self.name}>"

with app.app_context():
    db.create_all()
# -------------------- SCHEMA --------------------
class AuthorsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Authors
        load_instance = True
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    specialisation = fields.Str(required=True)

author_schema = AuthorsSchema()
authors_schema = AuthorsSchema(many=True)

# -------------------- ROUTES --------------------


@app.route("/", methods=["GET"])
def index():
   # return "Hello, World!"

    get_authors = Authors.query.all()
    author_schema = AuthorsSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}), 200)
@app.route("/authors", methods=["GET"])
def get_authors():
    authors = Authors.query.all()
    return jsonify({"authors": authors_schema.dump(authors)})

@app.route("/authors/<int:id>", methods=["GET"])
def get_author_by_id(id):
    author = Authors.query.get_or_404(id)
    return jsonify({"author": author_schema.dump(author)})

@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json(force=True)
    new_author = author_schema.load(data)
    new_author.create()
    return jsonify({"author": author_schema.dump(new_author)}), 201

@app.route("/authors/<int:id>", methods=["PUT"])
def update_author(id):
    author = Authors.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        author.name = data["name"]
    if "specialisation" in data:
        author.specialisation = data["specialisation"]

    db.session.commit()
    return jsonify({"author": author_schema.dump(author)})

@app.route("/authors/<int:id>", methods=["DELETE"])
def delete_author(id):
    author = Authors.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return make_response("", 204)

# -------------------- MAIN --------------------
if __name__ == "__main__":
    print("Starting the server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

