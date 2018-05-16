from flask import render_template, jsonify, request
from . import main
import json,datetime
from flask_login import current_user, login_required
from ..models import Questionnaire, Item, Answer, Map, User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/design', methods=['GET', 'POST'])
@login_required
def design():
    
    if request.method == 'POST':
        a = request.get_json(force = True)
        title = a["title"]
        timestamp = datetime.datetime.now()
        user_id = current_user.get_id()
        items = a["items"]
        q = Questionnaire()
        if(title != ""):
            q.title = title
        q.user_id = user_id
        q.timestamp = timestamp
        q.save()
        for item in items:
            i = Item()
            question = item["question"]
            no = item["no"]
            kind = item["kind"]
            i.question = question
            i.no = no
            i.kind = kind
            choice = item["choice"]
            for c in choice:
                i.choice.append(c)   
            i.questionnaire = q
            i.save()
        return jsonify(result=str(q.id))
    return render_template('design.html',id="")



@main.route('/old/p/<str>')
@login_required
def old(str):
    user_id = current_user.get_id()
    q = Questionnaire.objects(user_id=user_id).order_by("-timestamp").all()

    return render_template('old.html',q=q, str=str)

@main.route('/old/edit/<id>')
def edit(id):
    q = Questionnaire.objects(id=id).first()
    i = Item.objects(questionnaire=id).order_by("+no").all()

    return render_template('edit.html',q=q, i=i)

@main.route('/old/delete', methods=['GET', 'POST'])
def delete():
    a = request.get_json(force = True)
    id = a["id"]
    q = Questionnaire.objects(id = id).first()
    i = Item.objects(questionnaire=id).all()
    a = Answer.objects(questionnaire = id).all()
    q.delete()
    for item in i:
        item.delete()
    for answer in a:
        answer.delete()
    return jsonify(a=1)

@main.route('/old/<id>')
def detail(id):
    q = Questionnaire.objects(id=id).first()
    i = Item.objects(questionnaire=id).order_by("+no").all()
    count = 0
    a = Answer.objects(questionnaire = q.id).count()
    if(a):
        count = a
    a = Answer.objects(questionnaire = q.id).all()
    answer_list = []
    for answer in a:
        answer_dict = {}
        answer_dict['timestamp'] = answer.timestamp
        answer_dict['content'] = []
        for x in range(len(i)):
            answer_item = {}
            answer_item['question'] = i[x].question
            answer_item['no'] = i[x].no
            answer_item['kind'] = i[x].kind
            answer_item['choice'] = []
            for choice in i[x].choice:
                
                tem = answer.map_list[x].v_choice
                if(choice in tem):
                    choice_add=(choice,True)
                else:
                    choice_add=(choice,False)
                answer_item['choice'].append(choice_add)
            answer_dict['content'].append(answer_item)
        answer_list.append(answer_dict)

    return render_template('detail.html',x=count, a=a, q=q, i=i, answer_list=answer_list)

@main.route('/chart')
def chart():
    id = request.args.get('id')
    q = Questionnaire.objects(id=id).first()
    i = Item.objects(questionnaire=id).all()
    L = []
    for item in i:
        d = {}
        
        for choice in item.choice:
            d[choice] = 0

        for v in item.vote:
            d[v]=d[v]+1
        L.append(d)    
    return json.dumps(L)

@main.route('/create', methods=['GET', 'POST'])
def create():
    a = request.get_json(force = True)
    title = a["title"]
    timestamp = datetime.datetime.now()
    user_id = current_user.get_id()
    items = a["items"]
    q = Questionnaire()
    if(title != ""):
        q.title = title
    q.user_id = user_id
    q.timestamp = timestamp
    q.save()
    for item in items:
        i = Item()
        question = item["question"]
        no = item["no"]
        kind = item["kind"]
        i.question = question
        i.no = no
        i.kind = kind
        choice = item["choice"]
        for c in choice:
            i.choice.append(c)   
        i.questionnaire = q
        i.save()
    return jsonify(result=str(q.id))

@main.route('/example')
@login_required
def example():
    u = User.query.all()
    i = Item.objects().all()
    for user in u:
        if user.is_administrator():
            id = str(user.id)
    q = Questionnaire.objects(user_id=id).all()
    return render_template('fromExample.html',q=q, i=i)