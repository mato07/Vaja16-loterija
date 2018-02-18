#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2 # lahko so rdeci ker v resnici poganja googlov python
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None): # pod params lahko dodamo argumente za spletno stran
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("osnovna-stran.html")

class LotoHandler(BaseHandler):
    def get(self):
        loto_listek = []

        for i in range(8):
            while True:
                nakljucno_stevilo = random.randint(1, 39)
                if nakljucno_stevilo not in loto_listek:
                    break
            loto_listek.append(nakljucno_stevilo)

        info = {"listek": loto_listek}
        return self.render_template("loto.html",info)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/loto', LotoHandler)
], debug=True)
