#encoding:utf-8
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from datetime import datetime
# user autentication
from django.contrib.auth.decorators import login_required
from microsip_api.comun.sic_db import get_conecctionname, get_existencias_articulo

@login_required( login_url = '/login/' )
def index( request ):

    return render( request,'main/index.html',{})
