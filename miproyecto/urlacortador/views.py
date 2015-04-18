from django.shortcuts import render
from models import Pages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def formulario():
    return ( "<form method='post'>FORMUMLARIO URLS ACORTADAS:<input type='text'name='valor' value='' /><button type='submit'> Enviar</button></form>")


def printmodels():
    codehtml = "Paginas:"
    urlink1 = ""
    urlink2 = ""
    for iterador in  Pages.objects.all():
        urlink1  = "<a href='http://localhost:8000/"+ str(iterador.id) +  "'>"+ "http://localhost:8000/"+str(iterador.id) + "</a>"
        urlink2 = "<a href='"+ iterador.pagina +  "'>"+ iterador.pagina + "</a>"
        codehtml +=  "<p>Pagina: " + str(urlink2) +"----URCL acortada----->"+ str(urlink1) +"</p>"

    return codehtml

@csrf_exempt
def acortador(request, recurso):
    cuerpo = request.body
    if request.method == "GET":
        if recurso == "":
            return HttpResponse(formulario() + printmodels())
        else:
            try:
                retorno = Pages.objects.get(id=recurso)
                return HttpResponseRedirect(str(retorno.pagina))
            except Pages.DoesNotExist:
                return HttpResponseNotFound ( "<h1>PAGINA NO ENCONTRADA </h1><p><a href='http://localhost:8000'>formulario</a></p>")

    if request.method == "POST":
        respuesta = ""
        cuerpo = cuerpo.split('=')[1]

        if cuerpo.find("http%3A%2F%2F") >=  0:
            cuerpo = cuerpo.split('http%3A%2F%2F')[1]

        cuerpo = "http://" + cuerpo

        try:
            retorno = Pages.objects.get(pagina = cuerpo)
            respuesta += "URL: " + cuerpo + " ya acortada como: " + str(retorno.id)
        except Pages.DoesNotExist:
            p = Pages(pagina=cuerpo)
            p.save()
            respuesta = "<p> Pagina acortada: " + cuerpo + " </p>" + printmodels()



        return HttpResponse(respuesta  + "<p><a href='http://localhost:8000'>formulario</a></p>")



