#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form, CSRFProtect
from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.app = app
db.init_app(app)
Migrate(app, db)

csrf = CSRFProtect(app)
csrf.init_app(app)


#----------------------------------------------------------------------------#
# Utility Functions.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

def get_bool(field_name):
    if request.form.get(field_name) == 'y':
        seeking = True
    else:
        seeking = False
    return seeking


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


#  Home Page
#  ----------------------------------------------------------------
@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    """
    Returns a list of all venues. Filters the list by location, with each location
    containing a list of venues (name, id, and number of upcoming shows).
    """
    # First query the venues table for all venues
    all_venues = Venue.query.all()

    # Create and populate dictionary for storing and sorting venues by city and state
    venues_dict = {}
    for venue in all_venues:
        # Set the city and state as keys
        key = f"{venue.city}, {venue.state}"

        upcoming_shows = []
        past_shows = []
        for show in venue.shows:
            if show.start_time > datetime.now():
                upcoming_shows.append(show)
            else:
                past_shows.append(show)

        venues_dict.setdefault(key, []).append({
          'id': venue.id,
          'name': venue.name,
          'city': venue.city,
          'state': venue.state,
          'num_upcoming_shows': len(upcoming_shows),
        })
    # Create a list with dictionaries for all locations and append the Venue values
    # for that location to the list.
    data = []
    for val in venues_dict.values():
        data.append({
          'city': val[0]['city'],
          'state': val[0]['state'],
          'venues': val
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Returns a list of venues matching the query term. Search results are 
    case-insensitive. They also do not have to be an exact match, only a phrasal
    match.
    """
    search_term = request.form.get('search_term', '')
    matched_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

    data = []
    for match in matched_venues:
        data.append({
            "id": match.id,
            "name": match.name,
            "num_upcoming_shows": len(match.shows)
        })
    response = {
        "count": len(data),
        "data": data
        }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    # Set show attributes
    upcoming_shows = []
    past_shows = []
    for show in venue.shows:
        show_details = {
          "artist_id": show.artist.id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M:%S')
          }

        if show.start_time < datetime.utcnow():
            past_shows.append(show_details)
        else:
            upcoming_shows.append(show_details)

    venue_data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=venue_data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # Retrieve form values
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    website = request.form['website_link']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    genres = request.form['genres'].split(',')
    seeking_talent = get_bool('seeking_talent')
    seeking_description = request.form['seeking_description']

    # Insert new venue details. If successful, flash success
    try:
        new_venue = Venue(name=name, city=city, state=state, address=address, 
          phone=phone, website=website, image_link=image_link, facebook_link=facebook_link,
          genres=genres, seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(new_venue)
        db.session.commit()

        new_venue = Venue.query.filter_by(name=name).all()[0]
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=new_venue.id))


@app.route('/venues/<venue_id>/delete', methods=['POST', 'GET', 'DELETE'])
def delete_venue(venue_id):
    """
    Delete an existing venue and redirect the user to the home page
    """
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    """
    Returns a list of dictionaries with artist's name and id
    """
    data = []
    all_artists = Artist.query.all()

    for artist in all_artists:
        artist_details = {
            "id": artist.id,
            "name": artist.name
            }
        data.append(artist_details)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Returns a list of artists that match the search query.
    Searches are case insensitive, and matches don't have to be exact.
    """
    search_term = request.form.get('search_term', '')
    data = []
    matched_artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()

    for artist in matched_artists:
        artist_details = {
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(artist.shows)
            }
        data.append(artist_details)

    response = {
        "count": len(matched_artists),
        "data": data
        }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Returns artist details alongside details of the shows they've registered for
    """
    artist = Artist.query.get(artist_id)
    past_shows = []
    upcoming_shows = []

    # Populate the list of past and upcoming shows
    for show in artist.shows:
        show_details = {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                }
        if show.start_time > datetime.now():
            upcoming_shows.append(show_details)
        else:
            past_shows.append(show_details)

    # Curate the data response to be returned
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
        }

    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form['genres'].split(',')
    seeking_venue = get_bool('seeking_venue')
    seeking_description = request.form['seeking_description']
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website_link']

    try:
        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres,
            seeking_venue=seeking_venue, seeking_description=seeking_description,
            facebook_link=facebook_link, image_link=image_link, website=website)
        db.session.add(artist)
        db.session.commit()
        artist = Artist.query.filter_by(name=name).all()[0]
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist.id))


@app.route('/artists/<artist_id>/delete', methods=['POST', 'GET', 'DELETE'])
def delete_artist(artist_id):
    """
    Delete an existing venue and redirect the user to the home page
    """
    try:
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index'))


# Edit Artist and Venue.
# ---------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    form.name.default = artist.name
    form.city.default = artist.city
    form.state.default = artist.state
    form.phone.default = artist.phone
    form.genres.default = artist.genres
    form.seeking_venue.default = artist.seeking_venue
    form.seeking_description.default = artist.seeking_description
    form.facebook_link.default = artist.facebook_link
    form.image_link.default = artist.image_link
    form.website_link.default = artist.website
    form.process()
    
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)

    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = request.form['genres'].split(',')
        artist.seeking_venue = get_bool('seeking_venue')
        artist.seeking_description = request.form['seeking_description']
        artist.facebook_link = request.form['facebook_link']
        artist.image_link = request.form['image_link']
        artist.website = request.form['website_link']

        db.session.add(artist)
        db.session.commit()
        flash("Artist " + artist.name + "was successfully updated!")
    except:
        db.session.rollback()
        flash("Error updating " + artist.name + "!")
    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    form.name.default = venue.name
    form.genres.default = venue.genres
    form.address.default = venue.address
    form.city.default = venue.city
    form.state.default = venue.state
    form.phone.default = venue.phone
    form.website_link.default = venue.website
    form.facebook_link.default = venue.facebook_link
    form.seeking_talent.default = venue.seeking_talent
    form.seeking_description.default = venue.seeking_description
    form.image_link.default = venue.image_link
    form.process()

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    print(request.form['genres'])

    try:
        venue.name = request.form['name']
        venue.genres = request.form['genres'].split(',')
        venue.address = request.form['address']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.phone = request.form['phone']
        venue.website = request.form['website_link']
        venue.facebook_link = request.form['facebook_link']
        venue.seeking_talent = get_bool('seeking_talent')
        venue.seeking_description = request.form['seeking_description']
        venue.image_link = request.form['image_link']

        db.session.add(venue)
        db.session.commit()
        flash("Venue " + venue.name + "was successfully updated!")
    except:
        db.session.rollback()
        flash("Error updating " + venue.name + "!")
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
    all_shows = Show.query.all()
    data = []
    
    for show in all_shows:
        show_details = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y %H:%M:%S")
            }
        data.append(show_details) 
    
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        
        new_show = Show(artist_id=artist_id,
            venue_id=venue_id, start_time=start_time)
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
        return redirect(url_for('shows'))


#  Error Handling
#  ----------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
