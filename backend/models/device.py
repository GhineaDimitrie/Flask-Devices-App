def device_serializer(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": device["name"],
        "status": device["status"]
    }