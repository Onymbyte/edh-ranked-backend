from app import app, db, render_template, request, redirect, url_for
from forms import *
from models import User, PlayRating, EnemyRating, Comment, Listing, CardListMap, Cards, CardRating
from flask_login import login_user, login_required, current_user, logout_user
from time import sleep
from scryUtil import addCommander, getImage, addCard
from datetime import datetime
now = datetime.utcnow

@app.route('/', methods=['GET', 'POST'])
def index():
    # db.drop_all() 
    # db.create_all()
    if not current_user.is_authenticated:
        return render_template("base.html")
    else:
        return render_template("base.html", user=current_user)
@app.route('/test', methods=['GET', 'POST'])
def test():
    db.drop_all() 
    db.create_all()
    user = User(username='Onymbit', email='jhar199@lsu.edu')
    user.set_password('asdf')
    addCommander('Ghyrson')
    db.session.add(user)
    db.session.commit()
    if not current_user.is_authenticated:
        return render_template("base.html")
    else:
        return render_template("base.html", user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter((User.username==form.username.data) | (User.email==form.email.data)).first() is not None:
            print("User already exists with that Username or Email.")
            return render_template('register.html', form=RegisterForm())
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    if current_user.is_authenticated:
       return redirect(url_for('index')) 
    return render_template('register.html', form=form)
    ret
@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm(csrf_enabled=False)
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if not user:
        return redirect(url_for('login', _external=True))
    print('Checking password...')
    if user.check_password(form.password.data):
        print("User exists and password was correct")
        try:
            login_user(user, remember=form.remember.data)
        except:
            print('Login Failed')
        print("User was logged in.")
        next_page = url_for('profile', username=user.username)
        return redirect(next_page) if next_page else redirect(url_for('index', _external=True, _scheme='https'))
    else:
        return redirect(url_for('login', _external=True))
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    playRatings = PlayRating.query.filter_by(author_id=user.id).all()
    enemyRatings = EnemyRating.query.filter_by(author_id=user.id).all()
    comments = Comment.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', user=user, play=playRatings, enemy=enemyRatings, comments=comments)

@app.route('/listings', methods=['GET', 'POST'])
# @async_action
def listings():
    formid = request.args.get('formid', 1, type=int)
    form = CreateListingForm()
    form2 = ColorIdentityForm()

    colors= []
    if form2.validate_on_submit() and formid==2:
        if form2.white.data:
            colors.append(Listing.color_identity.like('%W%'))
        if form2.blue.data:
            colors.append(Listing.color_identity.like('%U%'))
        if form2.black.data:
            colors.append(Listing.color_identity.like('%B%'))
        if form2.red.data:
            colors.append(Listing.color_identity.like('%R%'))
        if form2.green.data:
            colors.append(Listing.color_identity.like('%G%'))
    listings = Listing.query.filter(*colors).limit(10).all()

    if form.validate_on_submit() and formid == 1:
        success = addCommander(form.name.data)
        
        if success:
            return redirect(url_for('listing', listing_id=success))
    if current_user.is_authenticated:
        return render_template("listings.html", listings=listings, form=form, form2=form2, user=current_user)
    return render_template("listings.html", listings=listings, form=form, form2=form2)
@app.route('/listings/<sortBy>', methods=['GET', 'POST'])
def listings_sorted(sortBy):
    formid = request.args.get('formid', 1, type=int)
    form = CreateListingForm()
    form2 = ColorIdentityForm()
    sorts = {"playAsc": Listing.play_stars, "playDesc": Listing.play_stars.desc(), "enemyAsc": Listing.enemy_stars, "enemyDesc": Listing.enemy_stars.desc(), "cmcAsc": Listing.cmc, "cmcDesc": Listing.cmc.desc()}
    if not sortBy in sorts.keys():
        return redirect(url_for('listings'))
    colors= []
    if form2.validate_on_submit() and formid==2:
        if form2.white.data:
            colors.append(Listing.color_identity.like('%W%'))
        if form2.blue.data:
            colors.append(Listing.color_identity.like('%U%'))
        if form2.black.data:
            colors.append(Listing.color_identity.like('%B%'))
        if form2.red.data:
            colors.append(Listing.color_identity.like('%R%'))
        if form2.green.data:
            colors.append(Listing.color_identity.like('%G%'))
        
    listings = Listing.query.filter(*colors).order_by(sorts[sortBy]).limit(10).all()
    
    
    if form.validate_on_submit() and formid==1:
        success = addCommander(form.name.data)
        
        if success:
            return redirect(url_for('listing', listing_id=success))
    
    if current_user.is_authenticated:
        return render_template("listings.html", listings=listings, form=form, form2=form2, user=current_user)
    return render_template("listings.html", listings=listings, form=form, form2=form2)
@app.route('/listings/search/', methods=['GET', 'POST'])
def listings_search():
    formid = request.args.get('formid', 1, type=int)
    form = CreateListingForm()
    form2 = ColorIdentityForm()
    name = request.args['name']

    colors= []
    if form2.validate_on_submit() and formid==2:
        if form2.white.data:
            colors.append(Listing.color_identity.like('%W%'))
        if form2.blue.data:
            colors.append(Listing.color_identity.like('%U%'))
        if form2.black.data:
            colors.append(Listing.color_identity.like('%B%'))
        if form2.red.data:
            colors.append(Listing.color_identity.like('%R%'))
        if form2.green.data:
            colors.append(Listing.color_identity.like('%G%'))

    listings = Listing.query.filter(Listing.name.like(f"%{name.replace(' ', '%')}%", *colors)).limit(10).all()

    if form.validate_on_submit() and formid==1:
        success = addCommander(form.name.data)
        
        if success:
            return redirect(url_for('listing', listing_id=success))
    if current_user.is_authenticated:
        return render_template("listings.html", listings=listings, form=form,form2=form2, user=current_user)
    return render_template("listings.html", listings=listings, form=form, form2=form2)


@app.route('/listing/<listing_id>', methods=["GET", "POST"])
def listing(listing_id):
    formid = request.args.get('formid', 1, type=int)
    kwargs = {}
    listing = Listing.query.get(listing_id)
    if not listing:
        return redirect(url_for("listings"))
    kwargs['listing'] = listing
    
    form1 = PlayRatingForm()
    form2 = EnemyRatingForm()
    form3 = CommentForm()

    if form1.validate_on_submit() and current_user.is_authenticated and formid == 1:
        prevRating = PlayRating.query.filter_by(author_id=current_user.id, listing_id=listing.id).first()
        if prevRating:
            listing.play_star_total += int(form2.stars.data) - prevRating.star
            listing.play_stars = listing.play_star_total/listing.play_review_num
            prevRating.star = int(form2.stars.data)
            prevRating.review = form2.review.data
            prevRating.timestamp = now()
            db.session.commit()
        else:
            playRating = PlayRating(star=form1.stars.data,review=form1.review.data ,author_id=current_user.id, author_username=current_user.username, listing_id=listing.id)
            listing.play_review_num += 1
            listing.play_star_total += int(form1.stars.data)
            listing.play_stars = (listing.play_star_total + int(form1.stars.data))/(listing.play_review_num+1)
            
            db.session.add(playRating)
            db.session.commit()
        return redirect(url_for('listing', listing_id=listing.id))
    if form2.validate_on_submit() and current_user.is_authenticated and formid==2:
        prevRating = EnemyRating.query.filter(EnemyRating.author_id==current_user.id and EnemyRating.listing_id==listing.id).first()
        if prevRating:
            listing.enemy_star_total += int(form2.stars.data) - prevRating.star
            listing.enemy_stars = listing.enemy_star_total/listing.enemy_review_num
            prevRating.star = int(form2.stars.data)
            prevRating.review = form2.review.data
            prevRating.timestamp = now()
            db.session.commit()
        else:
            enemyRating = EnemyRating(star=form2.stars.data,review=form2.review.data ,author_id=current_user.id, author_username=current_user.username, listing_id=listing.id)
            listing.enemy_review_num += 1
            listing.enemy_star_total += int(form2.stars.data)
            listing.enemy_stars = listing.enemy_star_total/listing.enemy_review_num
            db.session.add(enemyRating)
            db.session.commit()
        return redirect(url_for('listing', listing_id=listing.id))
    if form3.validate_on_submit() and current_user.is_authenticated  and formid==3:
        comment = Comment(comment=form3.comment.data ,author_id=current_user.id, author_username=current_user.username, listing_id=listing.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('listing', listing_id=listing.id))
    
    
    kwargs['play'] = PlayRating.query.filter_by(listing_id=listing.id).order_by(PlayRating.timestamp).all()
    kwargs['enemy'] = EnemyRating.query.filter_by(listing_id=listing.id).order_by(EnemyRating.timestamp).all()
    kwargs['comments'] = Comment.query.filter_by(listing_id=listing.id).order_by(Comment.timestamp).all()

    kwargs['imgUri'] = getImage(listing.uuid, size='normal')
    
    if current_user.is_authenticated:
        kwargs['user'] = current_user
        kwargs['form1'] = form1
        kwargs['form2'] = form2
        kwargs['form3'] = form3
    return render_template('listing.html', **kwargs)

@app.route('/listing/<listing_id>/suggestedCards', methods=["GET", "POST"])
def listing_cards(listing_id):
    formid = request.args.get('formid', 1, type=int)
    kwargs = {}
    listing = Listing.query.get(listing_id)
    if not listing:
        return redirect(url_for("listings"))
    kwargs['listing'] = listing

    form1 = AddCardForm()

    if form1.validate_on_submit() and current_user.is_authenticated  and formid==1:
        card_id = addCard(form1.name.data, listing)
        if not card_id:
            print("Card is not in commander's colors or did not exist.")
            return redirect(url_for('listing_cards', listing_id=listing_id))
        if CardListMap.query.filter_by(card_id=card_id, listing_id=listing_id).first() is not None:
            print('Card was already suggested.')
            return redirect(url_for('listing_cards', listing_id=listing_id))
        card_map = CardListMap(card_id=card_id, listing_id=listing_id)
        db.session.add(card_map)
        db.session.commit()
        return redirect(url_for('listing_cards', listing_id=listing_id))
    
    card_map = CardListMap.query.filter_by(listing_id=listing_id).all()
    cards = list(map(lambda card_map_i: Cards.query.get(card_map_i.card_id), card_map))
    kwargs['cards'] = cards
    kwargs['card_map'] = card_map
    kwargs['imgUri'] = getImage(listing.uuid, size='normal')
    kwargs['imgUris'] = list(map(lambda card: getImage(card.uuid), cards))

    if current_user.is_authenticated:
        kwargs['user'] = current_user
        kwargs['form1'] = form1

    return render_template('listing_cards.html', **kwargs)
@app.route('/listing/<listing_id>/addCardReview/<card_id>', methods=["GET", "POST"])
@login_required
def addCardReview(listing_id, card_id):
    kwargs = {}
    listing = Listing.query.get(listing_id)
    card = Cards.query.get(card_id)
    card_map = CardListMap.query.filter_by(listing_id=listing_id, card_id=card_id).first()
    if (not card_map) | (not listing) | (not card):
        return redirect(url_for("listing_cards", listing_id=listing_id))

    kwargs['listing'] = listing
    kwargs['card'] = card
    kwargs['card_map'] = card_map
    kwargs['imgUri'] = getImage(listing.uuid, size='normal')
    kwargs['cardUri'] = getImage(card.uuid, size='normal')

    form1 = AddCardRatingForm()

    if form1.validate_on_submit() and current_user.is_authenticated:
        
        prevRating = CardRating.query.filter_by(author_id=current_user.id, listing_id=listing_id, card_id=card_id).first()
        if prevRating:
            card_map.play_star_total += int(form1.stars.data) - prevRating.star
            card_map.play_stars = card_map.play_star_total/card_map.play_review_num
            prevRating.star = int(form1.stars.data)
            db.session.commit()
        else:
            cardRating = CardRating(star=form1.stars.data ,author_id=current_user.id, listing_id=listing.id, card_id=card_id)
            card_map.play_review_num += 1
            card_map.play_star_total += int(form1.stars.data)
            card_map.play_stars = (card_map.play_star_total + int(form1.stars.data))/(card_map.play_review_num+1)
            
            db.session.add(cardRating)
            db.session.commit()
        return redirect(url_for('listing_cards', listing_id=listing.id))

    if current_user.is_authenticated:
        kwargs['user'] = current_user
        kwargs['form1'] = form1

    return render_template('addCardRating.html', **kwargs)








