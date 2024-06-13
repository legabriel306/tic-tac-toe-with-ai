from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

RANKINGS_FILE = 'rankings.json'

def read_rankings():
    if not os.path.exists(RANKINGS_FILE):
        return []
    with open(RANKINGS_FILE, 'r') as file:
        return json.load(file)

def write_rankings(rankings):
    with open(RANKINGS_FILE, 'w') as file:
        json.dump(rankings, file, indent=4)

@app.route('/ranking', methods=['GET'])
def get_ranking():
    rankings = read_rankings()
    return jsonify(rankings)

@app.route('/ranking', methods=['POST'])
def post_game_result():
    data = request.json
    jogador1 = data.get('jogador1')
    jogador2 = data.get('jogador2')
    vencedor = data.get('vencedor')

    if not all([jogador1, jogador2, vencedor]):
        return jsonify({'error': 'Dados incompletos'}), 400

    rankings = read_rankings()

    for player in [jogador1, jogador2]:
        if player not in [r['name'] for r in rankings]:
            if player != 'NONE':
                rankings.append({'name': player, 'score': 0})

    for player in rankings:
        if player['name'] == vencedor and vencedor != 'NONE':
            player['score'] += 1

    write_rankings(rankings)
    return jsonify({'message': 'Resultado registrado com sucesso'})

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    jogador = data.get('jogador')
    score = data.get('score')

    if not all([jogador, score]):
        return jsonify({'error': 'Dados incompletos'}), 400

    rankings = read_rankings()
    for player in rankings:
        if player['name'] == jogador:
            player['score'] = score
            break
    else:
        rankings.append({'name': jogador, 'score': score})

    write_rankings(rankings)
    return jsonify({'message': 'Pontuação atualizada com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
