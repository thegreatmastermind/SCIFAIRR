import json
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Entry, Event, SavedResource
from datetime import datetime
from googleapiclient.discovery import build



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
        food_name = request.form.get('mealName')
        food_description = request.form.get('mealDescription')
        sleep_start_time_str = request.form.get('sleepStartTime')
        sleep_end_time_str = request.form.get('sleepEndTime')

        note_date = datetime.strptime(note_date_str, '%Y-%m-%d').date()
        current_date = datetime.now()
        
        sleep_end_time = current_date.time()
        sleep_start_time = current_date.time()
                
        if sleep_start_time_str:
            sleep_start_time = datetime.strptime(sleep_start_time_str, '%H:%M').time()
            
        if sleep_end_time_str:
            sleep_end_time = datetime.strptime(sleep_end_time_str, '%H:%M').time()

        new_entry = Entry(
                date=note_date,
                tags=tags,
                moodTags=', '.join(mood_tags),
                note=note,
                mood=mood,
                user_id=current_user.id,
                food_name=food_name,
                food_description=food_description,
                sleep_start_time=sleep_start_time,
                sleep_end_time=sleep_end_time
            )

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
    

@views.route('/delid/<id>', methods=['GET'])
def deleteMyID(id):
    if id:
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
        
        return "hello world!"

@views.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        event_notes = request.form.get('event_notes')
        event_icon = request.form.get('event_icon')  

        new_event = Event(
            event_name=event_name,
            start_time=start_time,
            end_time=end_time,
            event_notes=event_notes,
            user_id=current_user.id,
            event_icon=event_icon  
        )

        db.session.add(new_event)
        db.session.commit()

        flash('Event added successfully!', category='success')
        return redirect(url_for('views.schedule'))

    # Retrieve events and display them in time order
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.start_time).all()

    return render_template('schedule.html', events=events)

@views.route('/delete-event', methods=['POST'])
def delete_event():
        data = request.get_json()

        event_id = data.get('eventId')

        if event_id is not None:
            event = Event.query.get(event_id)

            if event and event.user_id == current_user.id:
                db.session.delete(event)
                db.session.commit()

                return jsonify({"message": "Event deleted successfully"})
            else:
                return jsonify({"error": "Event not found or does not belong to the current user"}), 404
        else:
            return jsonify({"error": "Invalid or missing 'eventId' in the request"}), 400
    
@views.route('/data')
def data():
    entries = Entry.query.filter_by(user_id=current_user.id).all()

    if not entries:
        flash('No data available.', 'info')
        return render_template("data.html", mood_data=[], mood_tags_data=[], tags_percentage={}, tags_count={})

    # Mood Scores Data
    mood_scores_data = [{'date': entry.date.strftime('%Y-%m-%d'), 'mood': entry.mood} for entry in entries]

    # Mood Tags Data
    mood_tags_data = [{'date': entry.date.strftime('%Y-%m-%d'), 'moodTags': entry.moodTags} for entry in entries]

    # Tags Data
    tags_count = {}
    for entry in entries:
        tags_count[entry.tags] = tags_count.get(entry.tags, 0) + 1
    tags_percentage = {tag: count for tag, count in tags_count.items()}

    # Tags Count
    tags_count = {tag: count for tag, count in tags_count.items()}

    return render_template("data.html", mood_data=mood_scores_data, mood_tags_data=mood_tags_data, tags_percentage=tags_percentage, tags_count=tags_count)

@views.route('/add_event', methods=['POST'])
def add_event():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        event_notes = request.form.get('event_notes')
        event_icon = request.form.get('event_icon')

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
                user_id=current_user.id,
                event_icon=event_icon
            )

            db.session.add(new_event)
            db.session.commit()

            flash('Event added successfully!', category='success')
        except ValueError:
            flash('Invalid date/time format!', category='error')

    return redirect(url_for('views.schedule'))

@views.route('/quick-entry', methods=['POST'])
@login_required
def quick_entry():
    if request.method == 'POST':
        note_date_str = request.form.get('noteDate')

        note_date = datetime.strptime(note_date_str, '%Y-%m-%d').date()

        new_entry = Entry(
            date=note_date,
            tags=request.form.get('tags'),
            moodTags=', '.join(request.form.getlist('moodTags')),
            mood=request.form.get('mood'),
            user_id=current_user.id,
            food_name=request.form.get('mealName'),
            food_description=request.form.get('mealDescription'),
            sleep_start_time=datetime.strptime(request.form.get('sleepStartTime'), '%H:%M').time(),
            sleep_end_time=datetime.strptime(request.form.get('sleepEndTime'), '%H:%M').time()
        )

        db.session.add(new_entry)
        db.session.commit()

        flash('Quick entry added!', category='success')

        return redirect(url_for('views.dashboard'))

    return redirect(url_for('views.dashboard'))

# Function to initialize the YouTube Data API client
def youtube_api_service():
    api_key = 'AIzaSyCdM20n2aS-eleCp2NQkgK_6CrCj-P8tfY'  
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube

@views.route('/more', methods=['GET'])
def more():
    return render_template('more.html')

@views.route('/get-saved-videos', methods=['GET'])
def get_saved_videos():
    saved_videos = SavedResource.query.all()
    videos = [{'id': video.id, 'title': video.title, 'linkOrThumbnailUrl': video.link_or_thumbnail_url} for video in saved_videos]
    return jsonify({'videos': videos})


@views.route('/youtube-videos', methods=['GET'])
def youtube_videos():
    youtube = youtube_api_service()
    search_query = 'autism'  
    try:
        search_response = youtube.search().list(q=search_query, part='id,snippet', maxResults=10).execute()
        videos = search_response.get('items', [])
        return jsonify({'videos': videos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/soundscapes-videos', methods=['GET'])
def soundscapes():
    youtube = youtube_api_service()
    search_query = 'soundscapes'  
    try:
        search_response = youtube.search().list(q=search_query, part='id,snippet', maxResults=10).execute()
        videos = search_response.get('items', [])
        return jsonify({'videos': videos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/')
def landing():
    return render_template("landing.html")

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", User=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'change_password' in request.form:
            change_password()
        elif 'change_email' in request.form:
            change_email()
        elif 'change_first_name' in request.form:
            change_first_name()
        elif 'delete_account' in request.form:
            delete_account()

    return render_template('profile.html', User=current_user)

def change_password():
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, old_password):
            flash('Old password is incorrect', 'error')
        elif new_password != confirm_password:
            flash('New password and confirm password do not match', 'error')
        else:
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password changed successfully', 'success')
    
def change_email():
        new_email = request.form.get('new_email')
        current_user.email = new_email
        db.session.commit()
        flash('Email changed successfully', 'success')

def change_first_name():
        new_first_name = request.form.get('new_first_name')
        current_user.first_name = new_first_name
        db.session.commit()
        flash('First name changed successfully', 'success')

def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    flash('Account deleted successfully', 'success')
    return redirect(url_for('views.landing'))