from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Define the number of digits in the code
CODE_LENGTH = 4

# Define the maximum number of attempts
MAX_ATTEMPTS = 10

# Define the colors available for the code and the guesses
COLORS = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']


def generate_code():
    """Generate a random code."""
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def check_guess(code, guess):
    """Check the guess against the code and return the number of correct colors and positions
    and the number of correct colors but incorrect positions."""
    correct_positions = 0
    correct_colors = 0
    code_copy = code.copy()
    guess_copy = guess.copy()
    for i in range(CODE_LENGTH):
        if guess_copy[i] == code_copy[i]:
            correct_positions += 1
            code_copy[i] = None
            guess_copy[i] = None
    for i in range(CODE_LENGTH):
        if guess_copy[i] is not None and guess_copy[i] in code_copy:
            correct_colors += 1
            code_copy[code_copy.index(guess_copy[i])] = None
            guess_copy[i] = None
    return correct_positions, correct_colors


@app.route('/', methods=['GET', 'POST'])
def index():
    """Display the game board and handle the user's guesses."""
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
            if guess_result[0] == CODE_LENGTH:
                # Código adivinado correctamente
                # Generar un nuevo código secreto y reiniciar las variables de sesión
                session['code'] = generate_code()
                session['attempts'] = 0
                session['history'] = []
                return render_template('win.html', attempts=session['attempts'])
            elif session['attempts'] >= MAX_ATTEMPTS:
                
                # Se acabaron los intentos
                # Generar un nuevo código secreto y reiniciar las variables de sesión
                session['code'] = generate_code()
                session['attempts'] = 0
                session['history'] = []
                return render_template('lose.html')
    return render_template('game.html', colors=COLORS, history=session['history'], max_attempts=MAX_ATTEMPTS)


if __name__ == '__main__':
    app.run(debug=True)
