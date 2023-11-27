import dominate
from dominate.tags import *

def build(imobiliarias):
    doc = dominate.document(title='Imobiliárias de Guará', encoding='utf-8')

    with doc.head:
        link(rel='stylesheet', href='style/style.css')
        script(src='script/script.js')
        meta(name="viewport", content="width=device-width, initial-scale=1", charset='utf-8')

    with doc:
        for imobiliaria, houses in imobiliarias.items():
            h1(imobiliaria, cls='title')
            with div(cls='imobiliaria-row'):
                with div(cls='carousel'):
                    for house in houses:
                        with a(href=house['href'], cls='card', target="_blank"):
                            if house['new'] == True :
                                with div(cls='ribbon ribbon-top-right'):
                                    span('NOVO!')
                            with div(cls='img-wrapper'):
                                img(src=house['image'], cls='bg')
                                img(src=house['image'], cls='cover')
                            with div(cls='info-wrapper'):
                                p(house['location'], cls='info')
                                p(house['value'], cls='info')
                with div(cls='control'):
                    div(cls='start')
                    div(cls='prev')
                    div(cls='next')
                    div(cls='end')
    
    f = open("index.html", "w")
    f.write(doc.render())
    f.close()