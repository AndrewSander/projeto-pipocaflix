from sqlalchemy import func
from app.models import Avaliacao, db

def calcular_distribuicao(filme_id):
    total = db.session.query(func.count(Avaliacao.nota)).filter_by(filme_id=filme_id).scalar()

    # evitar divisão por zero
    if total == 0:
        return {i: 0 for i in range(1, 6)}

    # contar quantas notas de cada valor
    resultados = (
        db.session.query(Avaliacao.nota, func.count(Avaliacao.nota))
        .filter_by(filme_id=filme_id)
        .group_by(Avaliacao.nota)
        .all()
    )

    distribuicao = {i: 0 for i in range(1, 6)}
    for nota, qtd in resultados:
        distribuicao[int(nota)] = (qtd / total) * 100 

    return distribuicao
