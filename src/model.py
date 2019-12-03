def common_response(success: bool, data, hint: str = ''):
    if success:
        return {'message': 'success', 'hint': hint, 'response': data}

    else:
        return {'message': 'error', 'hint': hint, 'response': data}
