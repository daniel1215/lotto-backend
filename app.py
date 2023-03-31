import random
import hashlib
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

def letter_to_number(letter):
    return ord(letter.upper()) - 64

def get_name_numerology(name):
    name_numerology = 0
    for letter in name:
        if letter.isalpha():
            name_numerology += letter_to_number(letter)
    return name_numerology % 9 + 1

def generate_lotto_numbers(name, dob, seed):
    random.seed(f'{name}{dob}{seed}')
    lotto_numbers = random.sample(range(1, 71), 5)
    special_number = random.randint(1, 25)
    return lotto_numbers, special_number

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    name = f"{data['firstName']} {data['lastName']}"
    dob = data['dateOfBirth']
    
    # Use the current time as an additional seed for randomness
    seed = time.time()
    lotto_numbers, special_number = generate_lotto_numbers(name, dob, seed)
    name_numerology = get_name_numerology(name)
    
    explanations = []
    for i, num in enumerate(lotto_numbers):
        if i == 0:
            explanations.append(
                f"{num} is chosen based on the mystical vibrations of your name, "
                f"which resonates with the energy of number {name_numerology}. "
                f"The {i + 1}th number generated is influenced by the cosmic alignment "
                f"on your date of birth, {dob}. "
                f"Numerology and the universe conspire to bring you this unique number."
            )
        else:
            explanations.append(
                f"{num} is chosen based on the interplay of cosmic forces and "
                f"the energies that surround you. The {i + 1}th number generated "
                f"reveals the hidden patterns of your life, as influenced by your date of birth, {dob}. "
                f"Embrace the magic of the universe as it unveils this significant number."
            )
    
    response = {
        'lottoNumbers': lotto_numbers,
        'specialNumber': special_number,
        'explanations': explanations
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)