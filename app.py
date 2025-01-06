from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cnpj = request.form["cnpj"]
        cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")  # Remove caracteres especiais
        

        if len(cnpj) != 14:  # Verifica se o CNPJ tem 14 dígitos
            return render_template("index.html", error="CNPJ inválido. Deve ter 14 números.")

        url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            
            # Extrair dados relevantes
            result = {
                "nome_fantasia": data["estabelecimento"]["nome_fantasia"],
                "razao_social": data["razao_social"],
                "capital_social": data["capital_social"],
                "socios": [socio["nome"] for socio in data["socios"]],
                "emails": data["estabelecimento"]["email"] if data["estabelecimento"]["email"] else "Não disponível",
                "telefones": [
                                f"({data['estabelecimento']['ddd1']}) {data['estabelecimento']['telefone1']}" if data['estabelecimento']['telefone1'] else "Não Disponível",
                                f"({data['estabelecimento']['ddd2']}) {data['estabelecimento']['telefone2']}" if data['estabelecimento']['telefone2'] else None
                        ],
                "endereco": f"{data['estabelecimento']['tipo_logradouro']} {data['estabelecimento']['logradouro']}, {data['estabelecimento']['numero']} - {data['estabelecimento']['bairro']} - {data['estabelecimento']['cidade']['nome']}/{data['estabelecimento']['estado']['sigla']}",
                "cnaes": [
                        f"{atividade['subclasse']} - {atividade['descricao']}" for atividade in data["estabelecimento"]["atividades_secundarias"]
                        ],

            }
            # Filtra valores None antes de passar para o template
        if 'telefones' in result:
            result['telefones'] = [telefone for telefone in result['telefones'] if telefone]

            return render_template("index.html", result=result)

        else:
            return render_template("index.html", error="CNPJ não encontrado ou inválido.")
    
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
