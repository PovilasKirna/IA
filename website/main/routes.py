from flask import Blueprint, render_template, redirect, url_for, Response,request
from ..models import Proposal,ClassEvent, Class, User
from flask_login import login_required, current_user
from ..users.utils import elligible, Qson, roleRequired
from flask_mail import Message
from sqlalchemy import desc,text
from .. import db, mail


main = Blueprint('main', __name__)

@main.route('/home', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def home():
    if request.method == 'POST':
        key = request.form.get('search')
        proposals = Proposal.query.from_statement(text(f"""
                                                        SELECT * 
                                                        FROM proposal 
                                                        WHERE name LIKE '%{key}%' 
                                                        OR description LIKE '%{key}%' 
                                                        OR starting_date LIKE '%{key}%'
                                                        OR ending_date LIKE '%{key}%'
                                                        OR date_created LIKE '%{key}%'
                                                        OR proposal_status LIKE '%{key}%'
                                                        ORDER BY date_created DESC
                                                        LIMIT 6;
                                                        """)).all()
        events = ClassEvent.query.filter_by(user_id=current_user.id).order_by(desc(ClassEvent.starting_date)).limit(3).all()
        unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
        unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
        return render_template('Index.html', user=current_user, proposals=proposals, events=events, unreadproposals=unreadproposals, unreadevents=unreadevents)
    elif request.method == 'GET':
        unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
        unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
        proposals = Proposal.query.filter_by(user_id=current_user.id).order_by(desc(Proposal.date_created)).limit(6).all()
        events = ClassEvent.query.filter_by(user_id=current_user.id).order_by(desc(ClassEvent.starting_date)).limit(3).all()
    return render_template('Index.html', user=current_user, proposals=proposals, events=events, unreadproposals=unreadproposals, unreadevents=unreadevents)

    
@main.route("/catalog/proposals")
@login_required
@elligible(current_user)
def catalogproposals():
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    return render_template("proposalscatalog.html", user=current_user, unreadproposals=unreadproposals, unreadevents=unreadevents)
    
@main.route("/catalog/events")
@login_required
@elligible(current_user)
def catalogevents():
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    return render_template("eventscatalog.html", user=current_user, unreadproposals=unreadproposals, unreadevents=unreadevents)
    
    
def sendapprovalemail(user):
    msg = Message(
        'Registration approved', 
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    
    msg.body =f'''Our administrators have determined that you fit our requirements and aproved your account you can login with the link below:\n
{url_for('users.login', _external=True)}
    '''

    mail.send(msg)    

@main.route('/ajax/proposals')
@login_required
def ajaxproposals():
    proposals = Proposal.query.filter_by(user_id=current_user.id)
    return Qson(proposals)

@main.route('/ajax/events')
@login_required
def ajaxevents():
    events = ClassEvent.query.filter_by(user_id=current_user.id)
    return Qson(events)