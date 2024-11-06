from chalice import Chalice

app = Chalice(app_name='grader')


@app.route('/')
def index():
    return {'hello': 'grader'}

@app.route('/grader', methods=['POST'])
def grade_submission():
    payload = app.current_request.json_body
    # We'll echo the json body back to the user in a 'user' key.
    # print(payload)
    print(payload['bucket'])
    print(payload['web'])
    print(payload['api'])
    return {'user': payload}
