from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = None
    for item in data:
        if item.get("id") == id:
            picture = item
            break

    if picture is None:
        return jsonify({"error": "Picture not found"}), 404

    return jsonify(picture), 200
    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()

    # Validate required fields
    # if not new_picture or "id" not in new_picture or "url" not in new_picture:
    #     return jsonify({"error": "Missing 'id' or 'url' field"}), 400

    # Check for duplicate ID using a basic for loop
    for item in data:
        if item.get("id") == new_picture["id"]:
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    # Add the new picture
    data.append(new_picture)

    # Save updated data to the JSON file
    # with open(json_url, "w") as f:
    #     json.dump(data, f, indent=2)

    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_data = request.get_json()

    # Find the picture with the given ID using a for loop
    for index in range(len(data)):
        if data[index].get("id") == id:
            # Update the existing picture data with new values
            data[index].update(updated_data)

            # Save the updated list to the JSON file
            # with open(json_url, "w") as f:
            #     json.dump(data, f, indent=2)

            return jsonify(data[index]), 200

    # If picture not found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
# def delete_picture(id):
def delete_picture(id):
    for index in range(len(data)):
        if data[index].get("id") == id:
            # Remove the picture from the list
            del data[index]

            # Save updated data back to the JSON file
            with open(json_url, "w") as f:
                json.dump(data, f, indent=2)

            # Return empty body with 204 No Content
            return "", 204

    # Picture not found
    return jsonify({"message": "picture not found"}), 404
