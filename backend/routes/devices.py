from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from models.device import device_serializer
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MONGO_URI, MONGO_DB_NAME

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db["devices"]

devices_bp = Blueprint("devices", __name__)

@devices_bp.route("/", methods=["GET"])
def get_devices():
    devices = list(collection.find())
    return jsonify([device_serializer(d) for d in devices])

@devices_bp.route("/", methods=["POST"])
def add_device():
    data = request.get_json()
    new_device = {
        "name": data["name"],
        "status": "off"
    }
    result = collection.insert_one(new_device)
    new_device["_id"] = result.inserted_id
    return jsonify(device_serializer(new_device)), 201

@devices_bp.route("/<device_id>", methods=["PUT"])
def toggle_device(device_id):
    device = collection.find_one({"_id": ObjectId(device_id)})
    new_status = "off" if device["status"] == "on" else "on"
    collection.update_one(
        {"_id": ObjectId(device_id)},
        {"$set": {"status": new_status}}
    )
    updated = collection.find_one({"_id": ObjectId(device_id)})
    return jsonify(device_serializer(updated))

@devices_bp.route("/<device_id>", methods=["DELETE"])
def delete_device(device_id):
    collection.delete_one({"_id": ObjectId(device_id)})
    return jsonify({"message": "Device deleted"}), 200