from flask import Flask, Response, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__, template_folder='templates')

#CONFIGURAÇÔES DO BANCO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bancoempresas'

db = SQLAlchemy(app)



#======================================
# CRIANDO MAPEAMENTO COM  AS TABELAS NO BANCO MYSQL 
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    porte = db.Column(db.String(100))
    faturamento = db.Column(db.String(100))

    #================================
	#TESTANDO COM UM METODO DIFERENTE
    def __init__(self, nome, porte, faturamento):
        self.nome = nome
        self.porte = porte
        self.faturamento = faturamento
        

#CRIANDO ROTA PARA templates html

@app.route('/')
def index():
    empresas = Empresa.query.all()
    return render_template( 'index.html', empresas=empresas)



#CRIANDO ROTA  PARA abrir empresa

@app.route('/open', methods=['GET','POST'])
def open():
    if request.method == 'POST':
        empresa = Empresa(request.form['nome'], request.form['porte'], request.form['faturamento'])
        db.session.add(empresa)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('open.html')


#==============================
#CRIANDO ROTA PARA VOLTAR AO ('/')

@app.route('/')
def voltar():
    return render_template('index.html')


#============================
#CRIANDO ROTA  PARA baixar empresa

@app.route('/baixar/<int:id>')
def baixar(id):
    empresa = Empresa.query.get(id)
    db.session.delete(empresa)
    db.session.commit()
    return redirect(url_for('index'))
    

#============================
#CRIANDO ROTA  PARA editar empresa

@app.route('/edit/<int:id>' , methods=['GET', 'POST'])
def edit(id):
    empresa = Empresa.query.get(id)
    if request.method == 'POST':
        empresa.nome  = request.form['nome']
        empresa.porte  = request.form['porte']
        empresa.faturamento  = request.form['faturamento']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', empresa=empresa)


#========================================
#rodar servidor
if __name__ == '__main__':
	app.run(debug=True, port=3000)