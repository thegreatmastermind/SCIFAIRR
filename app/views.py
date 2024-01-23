import json
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .extensions import db  
from .models import Entry, Event
from datetime import datetime


views = Blueprint('views', __name__)

@views.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    if request.method == 'POST':
        note_date_str = request.form.get('noteDate')
        tags = request.form.get('tags')
        note = request.form.get('note')
        mood = request.form.get('mood')

        mood_tags = request.form.getlist('moodTags')

        note_date = datetime.strptime(note_date_str, '%Y-%m-%d').date()

        new_entry = Entry(date=note_date, tags=tags, moodTags=', '.join(mood_tags), note=note, mood=mood, user_id=current_user.id)
        db.session.add(new_entry)
        db.session.commit()

        flash('Entry added!', category='success')

    entries = Entry.query.filter_by(user_id=current_user.id).all()
    
    return render_template("journal.html", user=current_user, entries=entries)

@views.route('/delete-entry', methods=['POST'])
def delete_entry():
    entry = json.loads(request.data)
    entry_id = entry['entryId']
    entry = Entry.query.get(entry_id)
    
    if entry and entry.user_id == current_user.id:
        db.session.delete(entry)
        db.session.commit()

        return jsonify({})

@views.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        # Handle form submission for adding events
        event_name = request.form.get('event_name')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        event_notes = request.form.get('event_notes')

        new_event = Event(
            event_name=event_name,
            start_time=start_time,
            end_time=end_time,
            event_notes=event_notes,
            user_id=current_user.id
        )

        db.session.add(new_event)
        db.session.commit()

        flash('Event added successfully!', category='success')
        return redirect(url_for('views.schedule'))

    # Retrieve events and display them in time order
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.start_time).all()

    return render_template('schedule.html', events=events)

@views.route('/data')
def data():
    entries = Entry.query.filter_by(user_id=current_user.id).all()

    # Mood Data
    mood_data = [{'date': entry.date.strftime('%Y-%m-%d'), 'mood': entry.mood} for entry in entries]

    # Tags Percentage
    total_entries = len(entries)
    tags_count = {}
    for entry in entries:
        tags_count[entry.tags] = tags_count.get(entry.tags, 0) + 1
    tags_percentage = {tag: count / total_entries * 100 for tag, count in tags_count.items()}

    # Tags Count
    tags_count = {tag: count for tag, count in tags_count.items()}

    return render_template("data.html", mood_data=mood_data, tags_percentage=tags_percentage, tags_count=tags_count)

@views.route('/add_event', methods=['POST'])
def add_event():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        event_notes = request.form.get('event_notes')

        try:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

            if start_time >= end_time:
                flash('End time must be after start time!', category='error')
                return redirect(url_for('views.schedule'))

            new_event = Event(
                event_name=event_name,
                start_time=start_time,
                end_time=end_time,
                event_notes=event_notes,
                user_id=current_user.id
            )

            db.session.add(new_event)
            db.session.commit()

            flash('Event added successfully!', category='success')
        except ValueError:
            flash('Invalid date/time format!', category='error')

    return redirect(url_for('views.schedule'))

@views.route('/more')
def more():
    return render_template("more.html")

@views.route('/')
def landing():
    return render_template("landing.html")
