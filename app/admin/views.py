from . import admin
from flask import render_template, request, url_for, redirect
from ..models import Questionnaire, Answer, Map, User

@admin.route('/example')
def example():
	return render_template('admin/example.html')

@admin.route('/admin')
def _admin():
    page = request.args.get('page',1,type=int)
    pagination = User.query.paginate(page,per_page=10)
    u = pagination.items
    #u = User.query.all()
    q = Questionnaire.objects().all()
    
    for ques in q:
    	ques.count = Answer.objects(questionnaire=ques.id).count()
    return render_template('admin/admin.html', u=u, q=q, pagination=pagination)