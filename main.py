from flask import Flask, redirect, url_for, render_template, request
from google import generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

lista_produtos = [
    {
        'nome': 'Prato para vaso',
        'imagem': 'img/produtos/pote_flor.svg',
        'preco': '30.00',
        'favorito': False,
        'peso': '150g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '20cm x 20cm x 2cm',
        'tags': ['jardim', 'decoração', 'vasos'],
        'descricao': 'Prato para vaso de plantas, ideal para manter a água e evitar sujeira em sua casa.'
    },
    {
        'nome': 'Caixa empilhável',
        'imagem': 'img/produtos/caixa_empilhavel.svg',
        'preco': '50.00',
        'favorito': False,
        'peso': '400g',
        'material': 'PETG',
        'densidade': '30%',
        'dimensoes': '30cm x 20cm x 15cm',
        'tags': ['organização', 'caixas', 'armazenamento'],
        'descricao': 'Caixa empilhável resistente, ideal para organizar e armazenar objetos.'
    },
    {
        'nome': 'Dispenser de pilhas',
        'imagem': 'img/produtos/dispenser_pilha.png',
        'preco': '25.00',
        'favorito': False,
        'peso': '120g',
        'material': 'ABS',
        'densidade': '20%',
        'dimensoes': '10cm x 5cm x 5cm',
        'tags': ['organização', 'eletrônicos'],
        'descricao': 'Dispenser prático para armazenar e organizar pilhas AA e AAA.'
    },
    {
        'nome': 'Funil',
        'imagem': 'img/produtos/funil.png',
        'preco': '20.00',
        'favorito': False,
        'peso': '80g',
        'material': 'PLA',
        'densidade': '15%',
        'dimensoes': '15cm x 10cm x 10cm',
        'tags': ['cozinha', 'utensílios'],
        'descricao': 'Funil de plástico resistente, perfeito para transferência de líquidos na cozinha.'
    },
    {
        'nome': 'Garfo',
        'imagem': 'img/produtos/garfo.png',
        'preco': '15.00',
        'favorito': False,
        'peso': '30g',
        'material': 'PLA',
        'densidade': '10%',
        'dimensoes': '18cm x 3cm x 1cm',
        'tags': ['cozinha', 'utensílios'],
        'descricao': 'Garfo impresso em 3D, ideal para uso diário ou em piqueniques.'
    },
    {
        'nome': 'Mesas e cadeiras',
        'imagem': 'img/produtos/mesas_cadeiras.png',
        'preco': '100.00',
        'favorito': False,
        'peso': '1200g',
        'material': 'ABS',
        'densidade': '40%',
        'dimensoes': '60cm x 60cm x 80cm',
        'tags': ['móveis', 'decoração'],
        'descricao': 'Conjunto de mesa e cadeiras, perfeito para decoração de interiores e espaços compactos.'
    },
    {
        'nome': 'Porta lápis',
        'imagem': 'img/produtos/porta_lapis.png',
        'preco': '18.00',
        'favorito': False,
        'peso': '70g',
        'material': 'PETG',
        'densidade': '20%',
        'dimensoes': '10cm x 10cm x 12cm',
        'tags': ['escritório', 'organização'],
        'descricao': 'Porta lápis moderno para organizar sua mesa de escritório com estilo.'
    },
    {
        'nome': 'Shuriken',
        'imagem': 'img/produtos/shuriken.png',
        'preco': '10.00',
        'favorito': False,
        'peso': '50g',
        'material': 'PLA',
        'densidade': '25%',
        'dimensoes': '12cm x 12cm x 1cm',
        'tags': ['brinquedos', 'decoração'],
        'descricao': 'Shuriken decorativa, ideal para fãs de cultura oriental e artes marciais.'
    },
    {
        'nome': 'Elefante',
        'imagem': 'img/produtos/elefante.png',
        'preco': '40.00',
        'favorito': False,
        'peso': '200g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '15cm x 10cm x 10cm',
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Miniatura de elefante impresso em 3D, ótimo para decoração e colecionadores.'
    },
    {
        'nome': 'Sapo',
        'imagem': 'img/produtos/sapo.png',
        'preco': '35.00',
        'favorito': False,
        'peso': '150g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '10cm x 10cm x 8cm',
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Sapo decorativo impresso em 3D, ideal para coleções ou decoração temática.'
    },
    {
        'nome': 'Gato',
        'imagem': 'img/produtos/gato.png',
        'preco': '38.00',
        'favorito': False,
        'peso': '170g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '12cm x 8cm x 10cm',
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Figura de gato impresso em 3D, um toque especial para sua decoração.'
    },
    {
        'nome': 'Chave de boca ajustável',
        'imagem': 'img/produtos/chave_de_boca_ajustavel.png',
        'preco': '22.00',
        'favorito': False,
        'peso': '100g',
        'material': 'ABS',
        'densidade': '25%',
        'dimensoes': '20cm x 5cm x 2cm',
        'tags': ['ferramentas', 'utilidades'],
        'descricao': 'Chave de boca ajustável funcional, ideal para pequenos reparos.'
    },
    {
        'nome': 'Tubarão articulado',
        'imagem': 'img/produtos/tubarao_articulado.png',
        'preco': '50.00',
        'favorito': False,
        'peso': '300g',
        'material': 'PETG',
        'densidade': '20%',
        'dimensoes': '30cm x 10cm x 5cm',
        'tags': ['brinquedos', 'decoração'],
        'descricao': 'Modelo de tubarão articulado, perfeito para decoração e coleções.'
    },
    {
        'nome': 'Mini catapulta',
        'imagem': 'img/produtos/mini_catapulta.png',
        'preco': '45.00',
        'favorito': False,
        'peso': '250g',
        'material': 'PLA',
        'densidade': '30%',
        'dimensoes': '15cm x 10cm x 8cm',
        'tags': ['brinquedos', 'engenharia'],
        'descricao': 'Mini catapulta funcional, excelente para entusiastas de engenharia.'
    },
    {
        'nome': 'Suporte para celular',
        'imagem': 'img/produtos/suporte_para_celular.png',
        'preco': '25.00',
        'favorito': False,
        'peso': '80g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '10cm x 8cm x 5cm',
        'tags': ['utilidades', 'escritório'],
        'descricao': 'Suporte para celular prático e moderno, ideal para mesas de escritório.'
    },
    {
        'nome': 'Coelho',
        'imagem': 'img/produtos/coelho.png',
        'preco': '32.00',
        'favorito': False,
        'peso': '180g',
        'material': 'PLA',
        'densidade': '15%',
        'dimensoes': '12cm x 8cm x 10cm',
        'estoque': 14,
        'tags': ['decoração', 'brinquedos']
    },
    {
        'nome': 'Foguete',
        'imagem': 'img/produtos/foguete.png',
        'preco': '55.00',
        'favorito': False,
        'peso': '400g',
        'material': 'ABS',
        'densidade': '25%',
        'dimensoes': '25cm x 8cm x 8cm',
        'estoque': 4,
        'tags': ['brinquedos', 'decoração']
    },
    {
        'nome': 'Anel de gato',
        'imagem': 'img/produtos/anel_de_gato.png',
        'preco': '12.00',
        'favorito': False,
        'peso': '20g',
        'material': 'PLA',
        'densidade': '10%',
        'dimensoes': '3cm x 3cm x 0.5cm',
        'estoque': 40,
        'tags': ['acessórios', 'moda']
    }
]


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search')
def search():
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    genai.configure(api_key=os.getenv('API'))
    context = f'Voce é um ajudante de uma loja que vente produtos impressos em 3D chamada MacLabs, o catalogo da empresa é: {lista_produtos}, responda as perguntas do usuario de forma generosa'
    prompt = request.args.get('prompt')
    input_ia = f'{context}: {prompt}'
    output = model.generate_content(input_ia)
    return {'message': output.text}


if __name__ == '__main__':
    app.run(debug=True)
