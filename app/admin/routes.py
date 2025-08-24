from . import admin
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_migrate import Migrate
from app.models import db, Ator, Filme, Atuacao, Episodio, Genero, Usuario

# Formulário de novo episódio
@admin.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        numero = request.form["numero"]
        avaliacao = float(request.form["avaliacao"])
        filme_id = int(request.form["filme_id"])

        novo_episodio = Episodio(titulo=titulo, numero=numero, avaliacao=avaliacao, filme_id = filme_id)
        db.session.add(novo_episodio)
        db.session.commit()

        return redirect(url_for("main.series", filme_id=filme_id))
    
    filmes = Filme.query.all()
    return render_template("novo.html", filmes=filmes)

# Formulário de novo filme
@admin.route('/novo-filme', methods=['GET', 'POST'])
def novo_filme():
    generos = Genero.query.order_by(Genero.nome.asc()).all()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        temporada = request.form['temporada']
        data_lancamento_str = request.form['data_lancamento']
        data_lancamento = datetime.strptime(data_lancamento_str, "%Y-%m-%d").date()
        tipo = request.form['tipo']
        lancamento = request.form['lancamento'] == "True"

        trailer_url = request.form.get('trailer', '')
        
        genero_ids = request.form.getlist("generos")  
        genero_ids = [int(gid) for gid in genero_ids]  

        novo_filme = Filme(titulo=titulo, descricao=descricao, temporada =int(temporada), data_lancamento = data_lancamento, tipo=tipo, lancamento=lancamento, trailer=trailer_url)
        
        generos_selecionados = Genero.query.filter(Genero.id.in_(genero_ids)).all()
        for genero in generos_selecionados:
            novo_filme.generos.append(genero)

        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for('admin.novo'))

    return render_template("novo_filme.html", generos = generos)

# Formulário de novo ator
@admin.route('/novo-ator', methods=['GET', 'POST'])
def novo_ator():
    filmes = Filme.query.all()
    atores = Ator.query.all()

    if request.method == 'POST':
        acao = request.form.get("acao")

        if acao == "criar":
            nome = request.form["nome"]
            data_nascimento_str = request.form["data_nascimento"]
            data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()

            filmes_ids = request.form.getlist("filmes")
            personagem = request.form["personagem"]

            novo_ator = Ator(nome=nome, data_nascimento=data_nascimento)
            db.session.add(novo_ator) 
            
            
            for filme_id in filmes_ids:
                atuacao = Atuacao(ator=novo_ator, filme_id=int(filme_id), personagem=personagem)
                db.session.add(atuacao)

            db.session.commit()

            return redirect(url_for("admin.novo_ator"))

        elif acao == "adicionar_filme":
            ator_id = int(request.form["ator_existente"])
            ids_filmes = request.form.getlist("novos_filmes")
            personagem = request.form.get("personagem")

            for filme in ids_filmes:
                filme_id = int(filme)
                atuacao_existente = Atuacao.query.filter_by(ator_id=ator_id, filme_id=filme_id).first()

                if not atuacao_existente:
                    nova_atuacao = Atuacao(
                        ator_id=ator_id,
                        filme_id=filme_id,
                        personagem=personagem
                    )
                    db.session.add(nova_atuacao)

            db.session.commit()
            return redirect(url_for("admin.novo_filme"))

    return render_template("novo_ator.html", filmes=filmes, atores=atores)

# Formulário de novo genero
@admin.route('/novo-genero', methods=['GET', 'POST'])
def novo_genero():
    filmes = Filme.query.all()
    generos = Genero.query.order_by(Genero.nome.asc()).all()

    if request.method == 'POST':
        acao = request.form.get("acao")

        if acao == "criar":
            nome = request.form["nome"]

            filmes_ids = request.form.getlist("filmes")
            filmes_selecionados = Filme.query.filter(Filme.id.in_(filmes_ids)).all()

            novo_genero = Genero(nome = nome)
            novo_genero.filmes = filmes_selecionados
            db.session.add(novo_genero) 
            
            db.session.commit()

            return redirect(url_for("admin.novo_ator"))

        elif acao == "adicionar_genero":
            genero_id = int(request.form["genero_existente"])
            genero = Genero.query.get_or_404(genero_id)

            filmes_ids = request.form.getlist("novos_filmes")
            novos_filmes = Filme.query.filter(Filme.id.in_(filmes_ids)).all()

            for filme in novos_filmes:
                if filme not in genero.filmes:
                    genero.filmes.append(filme)

            db.session.commit()
            return redirect(url_for("admin.novo_genero"))

    return render_template("novo_genero.html", filmes=filmes, generos = generos)

# Rota para editar um filme existente
@admin.route('/editar-filme/<int:filme_id>', methods=['GET', 'POST'])
def editar_filme(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    generos_disponiveis = Genero.query.order_by(Genero.nome.asc()).all()

    if request.method == 'POST':
        # Atualiza os dados do filme com os valores do formulário
        filme.titulo = request.form['titulo']
        filme.descricao = request.form['descricao']
        
        temporada_str = request.form.get('temporada')
        filme.temporada = int(temporada_str) if temporada_str and temporada_str.isdigit() else None
        
        data_lancamento_str = request.form['data_lancamento']
        filme.data_lancamento = datetime.strptime(data_lancamento_str, "%Y-%m-%d").date()
        
        filme.tipo = request.form['tipo']
        filme.lancamento = request.form.get('lancamento') == "True"
        
        # Pega a nova URL do trailer
        filme.trailer = request.form.get('trailer', '')
        
        # Atualiza os gêneros
        genero_ids = request.form.getlist("generos")
        genero_ids = [int(gid) for gid in genero_ids]
        filme.generos = Genero.query.filter(Genero.id.in_(genero_ids)).all()

        db.session.commit()
        flash("Filme atualizado com sucesso!", "success")
        return redirect(url_for('admin.novo_filme')) # Você pode mudar o redirecionamento
    
    return render_template('editar_filme.html', filme=filme, generos=generos_disponiveis)

@admin.route('/lista-filmes')
def lista_filmes():
    filmes = Filme.query.order_by(Filme.titulo.asc()).all()
    return render_template('lista_editar.html', filmes=filmes)