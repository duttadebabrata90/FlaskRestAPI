from flask import Flask, jsonify, request

from SourceCode.database import post_movies, post_person, get_all_movies, clean_neo4j_db
app = Flask(__name__)

stores = [
    {
        'name': 'My store 1',
        'item': [
            {
                'name': 'my item 1',
                'price': 300
            }
        ]
    }
]


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'item': []
        }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
                }
            store['item'] = new_item
            return jsonify(new_item)
    return jsonify({'message': 'Store not found'})


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['item'])
    return jsonify({'message': 'Item not found for the store {}'.format(name)})


@app.route('/postdata', methods=['POST'])
def post_data_to_neo4j():
    count_movie = post_movies()
    count_person = post_person()
    return jsonify({'message': '{} Movie and {} Person Data posted successfully'.format(count_movie, count_movie)})


@app.route('/movies')
def get_movies():
    movies = get_all_movies()
    return jsonify({'movies': movies})


@app.route('/cleandb', methods=['DELETE'])
def clean_db():
    clean_neo4j_db()
    return jsonify({'message': 'Clean Database !!'})


app.run(port=5000, debug=True)
