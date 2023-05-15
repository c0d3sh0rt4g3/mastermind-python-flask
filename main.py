from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'

secret_length = 4

max_attempts = 10

colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
colors_dict = {'red' : "#ff0000",
               'blue' : "#0000ff",}

def generate_secret():
    #Generate a random secret.
    return [random.choice(colors) for _ in range(secret_length)]


def check_guess(secret, guess):
    """Check the guess against the secret and return the number of correct colors and positions
    and the number of correct colors but incorrect positions."""
    correct_positions = 0
    correct_colors = 0
    secret = secret.copy()
    guess = guess.copy()
    for i in range(secret_length):
        if guess[i] == secret[i]:
            correct_positions += 1
    for i in range(secret_length):
        if guess[i] is not None and guess[i] in secret:
            correct_colors += 1
            secret[secret.index(guess[i])] = None
            guess[i] = None
    return correct_positions, correct_colors


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'secret' not in session:
        session['secret'] = generate_secret()
        session['attempts'] = 0
        session['history'] = []
    if request.method == 'POST':
        guess = request.form.getlist('guess[]')
        if guess:
            session['attempts'] += 1
            guess_result = check_guess(session['secret'], guess)
            session['history'].append((guess, guess_result))
            if guess_result[0] == secret_length:
                new_game()
                return render_template('win.html', attempts=session['attempts'])
            elif session['attempts'] >= max_attempts:
                new_game()
                return render_template('lose.html')
    return render_template('game.html', colors=colors_dict, history=session['history'], max_attempts=max_attempts)

def new_game():
    # Generate new secret and rest session variables
    session['secret'] = generate_secret()
    session['attempts'] = 0
    session['history'] = []


if __name__ == '__main__':
    app.run(debug=True)
