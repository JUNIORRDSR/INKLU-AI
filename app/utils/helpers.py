def format_response(data, message="Success", status_code=200):
    return {
        "status": status_code,
        "message": message,
        "data": data
    }

def validate_id(id_value):
    if not isinstance(id_value, int) or id_value <= 0:
        raise ValueError("Invalid ID: must be a positive integer.")

def paginate(query, page, per_page):
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return items, total

def handle_exception(e):
    return format_response(None, str(e), 400)