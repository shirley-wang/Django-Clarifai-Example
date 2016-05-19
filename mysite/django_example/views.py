from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render_to_response
from django import forms

import os, requests, json, os.path
import httplib2

from clarifai.client import ClarifaiApi

api = ClarifaiApi(app_id=settings.CLARIFAI_APP_ID, app_secret= settings.CLARIFAI_APP_SECRET)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class LandingPageView(TemplateView):
  template_name = 'index.html'

  def get(self, request, *args, **kwargs):
    template = loader.get_template('index.html')
    context = Context({'name': 'Cami'})
    return HttpResponse(template.render(context))

class ResultPageView(FormView):
  template_name = 'result.html'

  def post(self, request, *args, **kwargs):
    global api
    tag_list = ""

    file = request.FILES.get('file')
    result = api.tag_images(file)

    tags = result['results'][0]['result']['tag']['classes']
    for tag in tags:
      tag_list += tag + " "

    template = loader.get_template('result.html')
    context = Context({'tag_list': tag_list})
    return render_to_response("result.html", {"tag_list": tag_list})