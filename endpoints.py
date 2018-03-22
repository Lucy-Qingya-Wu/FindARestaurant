from restaurants import findARestaurant

from models import Base, Restaurant, engine

from flask import Flask, jsonify, request

from sqlalchemy.orm import sessionmaker


DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
	if request.method == 'GET':

		return getAllRestaurants()

	elif request.method == 'POST':

		location = request.args.get('location', '')
		mealType = request.args.get('mealType', '')

		return insertRestaurant(location, mealType)

@app.route("/restaurants/<int:id>", methods = ['GET', 'PUT', "DELETE"])
def restaurant_handler(id):
	restaurant = session.query(Restaurant).filter_by(id = id).one()

	if request.method == 'GET':
		return jsonify(restaurant=restaurant.serialize)

	elif request.method == 'PUT':
		name = request.args.get('name', '')
		address = request.args.get('address', '')
		image = request.args.get('image', '')

		print("name: ", name)
		print("address: ", address)
		print("image: ", image)

		return updateRestaurant(name, address, image, restaurant)


	elif request.method == 'DELETE':
		session.delete(restaurant)
		session.commit()

		return "Removed restaurant with id %s" % id





def updateRestaurant(name, address, image, restaurant):
	print("name: ", name)
	print("address: ", address)
	print("image: ", image)

	if len(name) > 0:
		restaurant.restaurant_name = name
	if len(address) > 0:
		restaurant.restaurant_address = address
	if len(image) > 0:
		restaurant.restaurant_image = image

	session.commit()
	return jsonify(restaurant=restaurant.serialize)



def getAllRestaurants():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants=[i.serialize for i in restaurants])

def insertRestaurant(location, mealType):

	result = findARestaurant(mealType, location)

	if result:

		restaurant=Restaurant(restaurant_name=result["name"], restaurant_image=result["image"], restaurant_address=result["address"])
		session.add(restaurant)
		session.commit()

		return jsonify(restaurant=restaurant.serialize)

	return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)