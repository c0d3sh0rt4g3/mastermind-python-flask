from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Define the number of digits in the code
code_length = 4

# Define the maximum number of attempts
max_attempts = 10

# Define the colors available for the code and the guesses
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

def generate_code():
    #Generate a random code.
    return [random.choice(colors) for _ in range(code_length)]


def check_guess(code, guess):
    """Check the guess against the code and return the number of correct colors and positions
    and the number of correct colors but incorrect positions."""
    correct_positions = 0
    correct_colors = 0
    code = code.copy()
    guess = guess.copy()
    for i in range(code_length):
        if guess[i] == code[i]:
            correct_positions += 1
    for i in range(code_length):
        if guess[i] is not None and guess[i] in code:
            correct_colors += 1
            code[code.index(guess[i])] = None
            guess[i] = None
    return correct_positions, correct_colors


@app.route('/', methods=['GET', 'POST'])
def index():
    #Display the game board and handle the user's guesses.
    if 'code' not in session:
        session['code'] = generate_code()
        session['attempts'] = 0
        session['history'] = []
    if request.method == 'POST':
        guess = request.form.getlist('guess[]')
        if guess:
            session['attempts'] += 1
            guess_result = check_guess(session['code'], guess)
            session['history'].append((guess, guess_result))
            if guess_result[0] == code_length:
                new_game()
                return render_template('win.html', attempts=session['attempts'])
            elif session['attempts'] >= max_attempts:
                new_game()
                return render_template('lose.html')
    return render_template('game.html', colors=colors, history=session['history'], max_attempts=max_attempts)

def new_game():
    # Generate new secret and rest session variables
    session['code'] = generate_code()
    session['attempts'] = 0
    session['history'] = []


if __name__ == '__main__':
    app.run(debug=True)
