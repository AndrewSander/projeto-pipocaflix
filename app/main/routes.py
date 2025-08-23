from . import main
from flask import render_template, request, redirect, url_for, session, flash, jsonify # type: ignore
from app.models import db, Filme, Usuario, Ator
from flask_login import login_required, current_user, login_user, logout_user # type: ignore
from app.models import db, Filme, Usuario, Ator, Atuacao, Avaliacao, Genero, usuario_filme_fav, usuario_ator_fav
from flask_login import login_required, current_user, login_user, logout_user
from app.funcoes import calcular_distribuicao
from sqlalchemy import func

# Pagina inicial
@main.route('/')
def index():
    filmes = Filme.query.filter_by(tipo="filme").limit(10).all()
    series = Filme.query.filter_by(tipo="serie").limit(10).all()
    atores= Ator.query.limit(4).all()
    if current_user.is_authenticated:
        lista= current_user.atores_fav
        return render_template("index.html",filmes=filmes,atores=atores, series=series,lista=lista)
    return render_template("index.html",filmes=filmes,atores=atores, series=series)

# Pagina de filmes
@main.route('/filmes/<int:filme_id>')
def filmes(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    if filme.tipo == "serie":
        return redirect(url_for('main.series', filme_id=filme.id))
    atuacoes = filme.atuacoes
    distribuicao = calcular_distribuicao(filme.id)
    total = len(filme.avaliacoes)

    return render_template('film-page.html', filme=filme, elenco=atuacoes, distribuicao=distribuicao, total=total)

# Pagina de series
@main.route('/series/<int:filme_id>')
def series(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    if filme.tipo == "filme":
        return redirect(url_for('main.filmes', filme_id = filme.id))
    episodios = filme.episodios
    atuacoes = filme.atuacoes
    distribuicao = calcular_distribuicao(filme.id)
    total = len(filme.avaliacoes)


    return render_template('series-page.html', filme=filme, episodios=episodios, elenco=atuacoes, distribuicao=distribuicao, total=total)

# Pagina de todos os filmes
@main.route('/filmes', methods = ["GET"])
def listar_filmes():
    query = Filme.query

    # filtros
    ano = request.args.get('ano')         
    generos_selecionados = request.args.getlist('genero') 
    ordenar = request.args.get('ordenar', 'recente')

    # testa e coloca os filtros
    query = query.filter_by(tipo="filme")
    
    if generos_selecionados:
        query = query.join(Filme.generos).filter(Genero.nome.in_(generos_selecionados))

    if ano:
        query = query.filter(db.extract('year', Filme.data_lancamento) == int(ano))
    
    # ordena os filmes
    if ordenar == "recente":
        query = query.order_by(Filme.data_lancamento.desc().nullslast())
    elif ordenar == "avaliacao":
        query = query.order_by(Filme.media.desc().nullslast())
    elif ordenar == "alfabetico":
        query = query.order_by(Filme.titulo.asc())
    elif ordenar == "favoritos":
        query = (
            query.outerjoin(usuario_filme_fav, Filme.id == usuario_filme_fav.c.filme_id)
            .group_by(Filme.id)
            .order_by(func.count(usuario_filme_fav.c.usuario_id).desc())
        )

    generos = Genero.query.order_by(Genero.nome).all()
    todos = Filme.query.filter_by(tipo='filme').all()
    anos = sorted({f.data_lancamento.year for f in todos if f.data_lancamento})
    
    filmes = query.all()
    return render_template('filmes.html', filmes=filmes, anos = anos, generos=generos)

# Pagina de todas as series
@main.route('/series')
def listar_series():
    query = Filme.query

    # filtros
    ano = request.args.get('ano')         
    generos_selecionados = request.args.getlist('genero') 
    ordenar = request.args.get('ordenar', 'recente')

    # testa e coloca os filtros
    query = query.filter_by(tipo="serie")
    
    if generos_selecionados:
        query = query.join(Filme.generos).filter(Genero.nome.in_(generos_selecionados))

    if ano:
        query = query.filter(db.extract('year', Filme.data_lancamento) == int(ano))
    
    # ordena os filmes
    if ordenar == "recente":
        query = query.order_by(Filme.data_lancamento.desc().nullslast())
    elif ordenar == "avaliacao":
        query = query.order_by(Filme.media.desc().nullslast())
    elif ordenar == "alfabetico":
        query = query.order_by(Filme.titulo.asc())
    elif ordenar == "favoritos":
        query = (
            query.outerjoin(usuario_filme_fav, Filme.id == usuario_filme_fav.c.filme_id)
            .group_by(Filme.id)
            .order_by(func.count(usuario_filme_fav.c.usuario_id).desc())
        )

    generos = Genero.query.order_by(Genero.nome).all()
    todos = Filme.query.filter_by(tipo='serie').all()
    anos = sorted({f.data_lancamento.year for f in todos if f.data_lancamento})
    
    series = query.all()
    return render_template('series.html', series=series, generos=generos, anos=anos)

# Pagina de todos os atores
@main.route('/todos_atores')
def listar_atores():
    atores = Ator.query.order_by(Ator.nome).all()
    
    for ator in atores:
        ator.imagem_url = url_for('static', filename=f'img/ator/{ator.nome}.jpg')

    return render_template('todos_atores.html', atores=atores)

# Função para ordenar filmes pelo título
def pegar_titulo(filme):
    return filme.titulo

# Página de filmografia dos atores
@main.route('/ator/<int:ator_id>')
def pagina_ator(ator_id):
    ator = Ator.query.get_or_404(ator_id)
    atuacoes = Atuacao.query.filter_by(ator_id=ator.id).all()

    filmes = []
    for atuacao in atuacoes:
        if atuacao.filme:  # garante que não é None
            if atuacao.filme not in filmes:
                filmes.append(atuacao.filme)

    filmes.sort(key=pegar_titulo)

    imagem_ator = url_for('static', filename=f'img/ator/{ator.nome}.jpg')

    return render_template('ator.html', ator=ator, filmes=filmes, imagem_ator=imagem_ator)

# Pagina de avaliação de filmes
@main.route("/avaliar/<int:filme_id>", methods=["GET", "POST"])
@login_required
def avaliar(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    avaliacao = Avaliacao.query.filter_by(usuario_id=current_user.id, filme_id=filme.id).first()

    if request.method == 'POST':
        nota = float(request.form['nota'])
        comentario = request.form.get('comentario', '')

        if avaliacao:
            # Atualiza avaliação
            avaliacao.nota = nota
            avaliacao.comentario = comentario
        else:
            # Nova atualização
            avaliacao = Avaliacao(
                usuario_id=current_user.id, filme_id=filme.id, nota=nota, comentario=comentario
            )
            db.session.add(avaliacao)

        db.session.commit()
        return redirect(url_for('main.filmes', filme_id=filme.id))

    return render_template('avaliar.html', filme=filme, avaliacao=avaliacao)

# Formulário de cadastro
@main.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if Usuario.query.filter_by(usuario=usuario).first():
            flash("Nome de usuário já está em uso.")
            return redirect(url_for("main.cadastro"))

        novo_usuario = Usuario(nome=nome, usuario=usuario)
        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso. Faça login.")
        return redirect(url_for("main.login"))

    return render_template("cadastro.html")

# Formulário de login
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.perfil'))
    
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = Usuario.query.filter_by(usuario=usuario).first()

        if user and user.verificar_senha(senha):
            session["usuario_id"] = user.id
            login_user(user)
            flash("Login realizado com sucesso!")
            next_page = request.args.get('next')
            return redirect(url_for("main.index")) 
        else:
            flash("Usuário não encontrado ou senha inválida. Cadastre-se!", "warning")
            # aqui não redireciona, apenas re-renderiza o login.html
            return redirect(url_for("main.login"))

    return render_template("login.html")

# Pagina de logout
@main.route("/logout")
def logout():
    session.pop("usuario_id", None)
    logout_user()
    flash("Logout realizado com sucesso.")
    return redirect(url_for("main.index"))

# Pagina perfil
@main.route("/perfil-geral")
@login_required
def perfil():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    ultimo_fav = current_user.filmes_fav.order_by(Filme.id.desc()).first()
    qtd_filmes = current_user.filmes_fav.count()
    qtd_atores = current_user.atores_fav.count()
    atores= current_user.atores_fav

    return render_template("perfil-geral.html", ultimo_fav=ultimo_fav, qtd_filmes=qtd_filmes, qtd_atores = qtd_atores,atores=atores)

@main.route("/perfil-criticas")
@login_required
def perfil_criticas():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    return render_template("perfil-criticas.html")

@main.route("/perfil-filmes")
@login_required
def perfil_filmes():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    return render_template("perfil-filmes.html")

@main.route("/perfil-atores")
@login_required
def perfil_atores():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    return render_template("perfil-atores.html")

@main.route("/perfil-assistindo")
@login_required
def perfil_assistindo():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para ver essa página.")
        return redirect(url_for("main.login"))

    return render_template("perfil-assistindo.html")

@main.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.nome = request.form.get('nome', current_user.nome)
        current_user.usuario = request.form.get('usuario', current_user.usuario)
        current_user.foto_url = request.form.get('foto_url', current_user.foto_url)
        current_user.descricao = request.form.get('descricao', current_user.descricao)
        db.session.add(current_user)
        db.session.commit()
        flash('Perfil atualizado!')
        return redirect(url_for('main.perfil'))

    return render_template('editar_perfil.html', usuario=current_user)

@main.route("/sugestoes")
def sugestoes():
    termo = request.args.get("q", "")
    if not termo:
        return jsonify([])

    filmes = Filme.query.filter(Filme.titulo.ilike(f"%{termo}%")).limit(5).all()
    return jsonify([{"id": f.id, "titulo": f.titulo} for f in filmes])

@main.post("/favoritos/filmes/toggle")
@login_required
def toggle_favorito_filme():
    data = request.get_json()
    filme_id = int(data.get("filme_id"))

    filme = Filme.query.get_or_404(filme_id)

    if current_user.filmes_fav.filter(Filme.id == filme_id).first():
        # já favoritou = remover
        current_user.filmes_fav.remove(filme)
        db.session.commit()
        return jsonify({"favoritado": False})
    else:
        # ainda não favoritou = adicionar
        current_user.filmes_fav.append(filme)
        db.session.commit()
        return jsonify({"favoritado": True})
    
@main.post("/favoritos/atores/toggle")
@login_required
def toggle_favorito_ator():
    data = request.get_json()
    ator_id = int(data.get("ator_id"))

    ator = Ator.query.get_or_404(ator_id)

    if current_user.atores_fav.filter(Ator.id == ator_id).first():
        # já favoritou = remover
        current_user.atores_fav.remove(ator)
        db.session.commit()
        return jsonify({"favoritado": False})
    else:
        # ainda não favoritou = adicionar
        current_user.atores_fav.append(ator)
        db.session.commit()
        return jsonify({"favoritado": True})
