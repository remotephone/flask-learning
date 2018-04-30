from flask import Flask
app = Flask(__name__)

#The url takes a value under user and assigns it to <username> variable.
@app.route('/user/<username>')
def show_user_profile(username):
    # Show the username for the user
    return 'User %s' % username

# Same as we did for user but we're doing it for a post ID
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id