from sanic import Sanic, response

app = Sanic(name="contacts_app")

# Create some test data for our catalog in the form of a list of contact.
contacts = [
    {
        'username': "yingshaoxo",
        'friends': ["god", "angles"]
    },
    {
        'username': "A",
        'friends': ["A's friend 1", "A's friend 2"]
    },
    {
        'username': "B",
        'friends': ["B's friend 1", "B's friend 2"]
    },
]


@app.route('/', methods=['GET'])
async def home(request):
    return response.html('''<h1>awesome people do awesome things.</h1>''')


@app.route('/api/v1/contacts/all', methods=['GET'])
async def api_all(request):
    return response.json(contacts)


@app.route('/api/v1/contacts', methods=['GET'])
async def api_username(request):
    # Check if an username was provided as part of the URL.
    # If username is provided, assign it to a variable.
    # If no username is provided, display an error in the browser.
    if 'username' in request.args:
        username = str(request.args['username'][0])
    else:
        return response.text("Error: No username field provided. Please specify an username.")

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested username.
    # Username are unique, but other fields might return many results.
    for contact in contacts:
        if contact['username'] == username:
            results.append(contact)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return response.json(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
