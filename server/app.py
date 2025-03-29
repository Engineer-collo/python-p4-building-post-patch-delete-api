#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

#Home route
@app.route('/')
def index():
    return "Index for Game/Review/User API"

#POST a new review
@app.route("/reviews", methods=["POST"])
def post_a_new_review():
    data = request.json
    new_review = Review(
    score=data.get("score"),
    comment=data.get("comment"),
    game_id=data.get("game_id"),
    user_id=data.get("user_id"),
)


    db.session.add(new_review)
    db.session.commit()

    review_dict = new_review.to_dict()

    response = make_response(jsonify(review_dict) ,201)
    return response

#PATCH a review
@app.route("/reviews/<int:review_id>", methods=["PATCH"])
def update_a_review(review_id): 
    review = Review.query.get(review_id)
    if not review:
        return make_response(jsonify({"error" : f"Review ID {review_id} not found"}), 404)
    else:
        data = request.json
        # Update only provided fields
        if "score" in data:
            review.score = data["score"]
        if "comment" in data:
            review.comment = data["comment"]
        if "game_id" in data:
            review.game_id = data["game_id"]
        if "user_id" in data:
            review.user_id = data["user_id"]

    #save the canges
    db.session.commit()

    return make_response(jsonify(review.to_dict()), 200)




#GET all games
@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

#GET a game by id
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

#GET all reviews
@app.route('/reviews')
def reviews():

    reviews = []
    for review in Review.query.all():
        review_dict = review.to_dict()
        reviews.append(review_dict)

    response = make_response(
        reviews,
        200
    )

    return response

#GET a review by id 
@app.route("/reviews/<int:review_id>")
def get_a_review_by_id(review_id):
    review = Review.query.get(review_id)
    if not review:
        response = make_response(jsonify({"error" : f"Review ID {review_id} not found"}), 404)
    else:
        review_dict = review.to_dict()
        response = make_response(jsonify(review_dict), 200)
    
    return response


#GET all users
@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

#DELETE a review.
@app.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_a_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        response = make_response(jsonify({"error" : f"Review ID {review_id} not found"}), 404)
    else:
        db.session.delete(review)
        db.session.commit()
        response = make_response(jsonify({"message" : "Review deleted successfully"}), 200)
    
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
