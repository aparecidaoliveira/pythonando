from ninja import Router, Query
from .schemas import LivroSchema, AvaliacaoSchema, FiltrosSortear, LivrosViewSchema
from .models import Livros, Categorias
from typing import List

livros_router = Router()


@livros_router.get("/", response={200: List[LivrosViewSchema]})
def get_livro(request):
    livros = Livros.objects.all()
    print(livros)
    return livros


@livros_router.post("/")
def create_livro(request, livro_schema: LivroSchema):
    nome = livro_schema.dict()["nome"]
    streaming = livro_schema.dict()["streaming"]
    categorias = livro_schema.dict()["categorias"]
    if streaming not in ["F", "AK"]:
        return 400, {"status": "Erro: Streaming deve ser F ou AK"}

    livro = Livros(nome=nome, streaming=streaming)
    livro.save()

    for categoria in categorias:
        # livro.categorias.add(Categorias.objects.get(id=categoria))
        categoria_temp = Categorias.objects.get(id=categoria)
        livro.categorias.add(categoria_temp)

    livro.save()
    print(livro_schema.dict())
    return {"status": "Ok"}
    # return livro


@livros_router.put("/{livro_id}")
def avaliar_livro(request, livro_id: int, avaliacao_schema: AvaliacaoSchema):
    comentarios = avaliacao_schema.dict()["comentarios"]
    nota = avaliacao_schema.dict()["nota"]
    try:
        livro = Livros.objects.get(id=livro_id)
        livro.comentarios = comentarios
        livro.nota = nota
        livro.save()
        return 200, {"status": "Avaliação realizada com sucesso"}
    except:
        return 500, {"status": "Erro interno do servidor"}


@livros_router.delete("/{livro_id}")
def deletar_livro(request, livro_id: int):
    livro = Livros.objects.get(id=livro_id)
    livro.delete()
    return livro_id


@livros_router.get("/sortear/", response={200: LivroSchema, 404: dict})
def sortear_livro(request, filtros: Query[FiltrosSortear]):
    nota_minima = filtros.dict()["nota_minima"]
    categoria = filtros.dict()["categorias"]
    reler = filtros.dict()["reler"]

    print(nota_minima)
    print(categoria)
    print(reler)

    livros = Livros.objects.all()

    if not reler:
        livros = livros.filter(nota=None)
    if nota_minima:
        livros = livros.filter(nota__gte=nota_minima)
    if categoria:
        livros = livros.filter(categorias__id=categoria)

    livro = livros.order_by("?").first()
    print(livro)
    if livros.count() > 0:
        return 200, livro
    else:
        return 404, {"status": "Livro não encontrado"}
