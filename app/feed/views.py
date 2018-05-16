from flask import render_template, request, url_for, redirect
from . import feed
from ..models import Questionnaire, Item, Answer, Map
import json, datetime

@feed.route('/<id>', methods = ['GET','POST'])
def _feed(id):	
    q = Questionnaire.objects(id=id).first()
    
    i = Item.objects(questionnaire=id).all()
    title = q.title
    if request.method == 'POST':
        a = Answer()
        timestamp = datetime.datetime.now()
        a.questionnaire = q
        a.timestamp = timestamp
        p = request.form
        for c in i:
            m = Map()
            if(c.kind == "single" or c.kind == "multi"):
                for x in p.getlist(c.question):
                    m.v_choice.append(x)
                    c.update(push__vote=x)
                a.map_list.append(m)
            elif(c.kind == "blank"):
                x = p.get(c.question)
                m.v_choice.append(x)
                c.update(push__vote=x)
                c.update(push__choice=x)
                a.map_list.append(m)
            
        a.save()
        
        return redirect(url_for('.finish'))
    return render_template('feed/feed.html',title = title,items = i,id = id)

@feed.route('/finish')
def finish():
    return render_template('feed/finish.html')	    