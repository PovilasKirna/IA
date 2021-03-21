from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from ..users.utils import elligible
from .forms import ProposalForm
from ..models import Proposal, ClassEvent
from .. import db
from sqlalchemy import func, text

proposals = Blueprint('proposals', __name__)

@proposals.route("/create", methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def createnew():
    form = ProposalForm()
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    if form.validate_on_submit():
        if form.starting_date.data and form.ending_date.data:
            proposal = Proposal(
                name=form.name.data, 
                description=form.description.data, 
                starting_date=form.starting_date.data, 
                ending_date=form.ending_date.data, 
                date_created=func.now(), 
                proposal_status='Pending', 
                user_id=current_user.id
            )
            db.session.add(proposal)
            db.session.commit()
            flash('Proposal created successfully!', category='success')
            return redirect(url_for('main.home'))
        else:
            proposal = Proposal(
                name=form.name.data, 
                description=form.description.data, 
                starting_date=form.starting_date.data, 
                ending_date=form.ending_date.data, 
                date_created=func.now(), 
                proposal_status='Draft', 
                user_id=current_user.id
            )
            db.session.add(proposal)
            db.session.commit()
            flash('Proposal draft created successfully!', category='success')
            return redirect(url_for('main.home'))
    return render_template("documentCreateForm.html", user=current_user, form=form, legend='New Proposal', unreadevents=unreadevents, unreadproposals=unreadproposals)



    
@proposals.route('/proposal/<int:proposal_id>', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def proposal(proposal_id):
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    proposal = Proposal.query.get_or_404(proposal_id)
    if proposal.user_id != current_user.id and current_user.role != 'Admin' and current_user.role != 'Manager':
        abort(403)
    proposal = Proposal.query.get_or_404(proposal_id)
    if request.method == 'POST':
        if request.form['select'] == 'Approve':
            proposal.proposal_status = 'Approved'
            db.session.commit()
        elif request.form['select'] == 'Reject':
            proposal.proposal_status = 'Rejected'
            db.session.commit()
    return render_template('proposal.html', user=current_user, proposal=proposal, unreadevents=unreadevents, unreadproposals=unreadproposals)
    
@proposals.route('/proposal/<int:proposal_id>/update', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def proposalUpdate(proposal_id):
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    proposal = Proposal.query.get_or_404(proposal_id)
    if proposal.proposal_status == 'Approved':
        flash('This proposal was approved by administration you cannot update it anymore!', category='error')
        return redirect(url_for('main.home'))
    if proposal.user_id != current_user.id and current_user.role != 'Admin' and current_user.role != 'Manager':
        abort(403)
    else:
        form = ProposalForm()
        if form.validate_on_submit():
            proposal.name = form.name.data
            proposal.description = form.description.data
            proposal.starting_date = form.starting_date.data
            proposal.ending_date = form.ending_date.data
            if form.starting_date.data and form.starting_date.data:
                proposal.proposal_status = 'Pending'
            db.session.commit()
            flash('Proposal'+ str(proposal.name) + ' was updated!', category='success')
            return redirect(url_for('proposals.proposal', proposal_id=proposal.id))
        elif request.method == 'GET':
            form.name.data = proposal.name
            form.description.data = proposal.description
            form.starting_date.data = proposal.starting_date
            form.ending_date.data = proposal.ending_date
        return render_template("documentCreateForm.html", user=current_user, form=form, legend='Update Proposal', unreadevents=unreadevents, unreadproposals=unreadproposals)

@proposals.route('/proposal/<int:proposal_id>/delete', methods=['POST'])
@login_required
@elligible(current_user)
def proposalDelete(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    if proposal.user_id != current_user.id:
        abort(403)
    db.session.delete(proposal)
    db.session.commit()
    flash('Proposal was deleted!', category='success')
    return redirect(url_for('main.home'))

@proposals.route('/managerproposalview', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def managerproposalview():
    if request.method == 'POST':
        key = request.form['search']
        print(key)
        if key != '':
            proposals = Proposal.query.from_statement(text(f"""
                                                            SELECT * 
                                                            FROM proposal 
                                                            WHERE name LIKE '%{key}%' 
                                                            OR description LIKE '%{key}%' 
                                                            OR starting_date LIKE '%{key}%'
                                                            OR ending_date LIKE '%{key}%'
                                                            OR date_created LIKE '%{key}%'
                                                            AND proposal_status = 'Pending';
                                                            """)).all()
        else:
            proposals = Proposal.query.filter_by(proposal_status='Pending').all()
        unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
        unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
        view = 'proposals'
        return render_template('managerview.html', user=current_user, view=view, data=proposals, unreadevents=unreadevents, unreadproposals=unreadproposals)
    
    unreadproposals = len(Proposal.query.filter_by(proposal_status='pending').all())
    unreadevents = len(ClassEvent.query.filter_by(event_status='pending').all())
    view = 'proposals'
    proposals = Proposal.query.filter_by(proposal_status='Pending').all()
    return render_template('managerview.html', user=current_user, view=view, data=proposals, unreadevents=unreadevents, unreadproposals=unreadproposals)
