from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from ..models import Class, User, ClassEvent, Proposal
from flask_login import login_required, current_user
from ..users.utils import elligible, skip_lessons
from .forms import ClassEventForm
from sqlalchemy import func, text
from .. import db

events=Blueprint('events', __name__)

@events.route('/createevent/<token>', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def createclassevent(token):
    proposal = Proposal.verify_reset_token(token)
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all()) 
    if not proposal:
        flash('That token is invalid or expired', category='error')
        return redirect(url_for('main.home'))
    else:
        form = ClassEventForm()
        form.name.data = proposal.name
        form.starting_date.data = proposal.starting_date
        form.ending_date.data = proposal.ending_date
        form.attending_class.choices = [(c.id, c.name) for c in Class.query.order_by(Class.name)]
        form.teacher.choices = [(t.id, (t.name+' '+t.surname)) for t in User.query.order_by(User.name, User.surname).filter_by(role='Mokytojas')]
        if form.validate_on_submit():
            #generate a document
            event = ClassEvent(
                name=form.name.data,
                starting_date=form.starting_date.data,
                ending_date=form.ending_date.data,
                starting_location=form.starting_location.data,
                ending_location=form.ending_location.data,
                assistant=form.assistant.data, 
                route=form.route.data,
                goal=form.goal.data,
                event_content=form.event_content.data,
                skipped_lessons = skip_lessons(form.starting_date.data, form.ending_date.data),
                destination=form.destination.data, 
                atending_class=form.attending_class.data,
                teacher=form.teacher.data,
                user_id=current_user.id,
                date_created=func.now()
                #documentas = katik sugeneruotas dokas. 
            )
            db.session.add(event)
            db.session.delete(proposal)
            db.session.commit()
            flash('Class event has been created!', category ='success')
            return redirect(url_for('main.home'))
   
    return render_template('eventCreateForm.html', form=form, user=current_user, unreadevents=unreadevents, legend='Create Event', unreadproposals=unreadproposals)

@events.route('/managereventview', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def managerproposalview():
    if request.method == 'POST':
        key = request.form['search']
        print(key)
        if key != '':
            events = ClassEvent.query.from_statement(text(f"""
                                                            SELECT * 
                                                            FROM class_event 
                                                            WHERE name LIKE '%{key}%' 
                                                            OR starting_date LIKE '%{key}%'
                                                            OR ending_date LIKE '%{key}%'
                                                            OR date_created LIKE '%{key}%'
                                                            OR teacher LIKE '%{key}%'
                                                            OR assistant LIKE '%{key}%'
                                                            OR destination LIKE '%{key}%'
                                                            OR atending_class LIKE '%{key}%'
                                                            OR starting_location LIKE '%{key}%'
                                                            OR ending_location LIKE '%{key}%'
                                                            OR route LIKE '%{key}%'
                                                            OR goal LIKE '%{key}%'
                                                            OR event_content LIKE '%{key}%'
                                                            OR skipped_lessons LIKE '%{key}%'
                                                            OR document LIKE '%{key}%'
                                                            AND event_status = 'Pending';
                                                            """)).all()
        else:
            events = ClassEvent.query.filter_by(event_status='Pending').all()
        unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
        unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
        view = 'events'
        classes = Class.query.all()
        return render_template('managerview.html', user=current_user, view=view, data=events, unreadevents=unreadevents, unreadproposals=unreadproposals, classes=classes)
    
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    view = 'events'
    events = ClassEvent.query.filter_by(event_status='Pending').all()
    classes = Class.query.all()
    return render_template('managerview.html', user=current_user, view=view, data=events, unreadevents=unreadevents, unreadproposals=unreadproposals, classes=classes)

@events.route('/event/<event_id>', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def event(event_id):
    event = ClassEvent.query.get_or_404(event_id)
    if event.user_id != current_user.id and current_user.role != 'Admin' and current_user.role != 'Manager':
        abort(403)
    else:
        if request.method=='POST':
            if request.form['select'] == 'Approve':
                event.event_status = 'Approved'
                db.session.commit()
            elif request.form['select'] == 'Reject':
                proposal.event_status = 'Rejected'
                db.session.commit()
            unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
            unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
            return render_template('event.html', user=current_user, event=event, unreadevents=unreadevents, unreadproposals=unreadproposals)
 
        unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
        unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
        classes = Class.query.all()
        return render_template('event.html', user=current_user, event=event, unreadevents=unreadevents, unreadproposals=unreadproposals, classes=classes)