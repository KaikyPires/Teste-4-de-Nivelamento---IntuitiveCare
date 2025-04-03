from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '')
    file_path = r"C:\Users\Kaiky Pires\Downloads\Relatorio_cadop.csv"

    if not os.path.exists(file_path):

        return jsonify({"error": "Arquivo CSV não encontrado no caminho especificado."}), 404

    try:

        df = pd.read_csv(file_path, delimiter=';')

        df = df.applymap(str)

        resultados = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

        if resultados.empty:

            return jsonify([]), 200

        resultados_json = resultados.to_dict(orient='records')

        return jsonify(resultados_json), 200

    except pd.errors.EmptyDataError:
        return jsonify({"error": "O arquivo CSV está vazio ou não contém dados válidos."}), 500
    except pd.errors.ParserError:
        return jsonify({"error": "Erro ao ler o arquivo CSV. Verifique o delimitador ou a estrutura do arquivo."}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
