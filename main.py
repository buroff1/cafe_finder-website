from flask import render_template, redirect, url_for, session, \
    Flask  # Import necessary Flask modules for web development
from flask_bootstrap import Bootstrap5  # Import Bootstrap for better styling and UI
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database management
from sqlalchemy.orm import DeclarativeBase  # Import DeclarativeBase for SQLAlchemy model base class
from flask_wtf import FlaskForm  # Import FlaskForm for creating forms
from wtforms import StringField, SubmitField  # Import fields for the form
from wtforms.validators import DataRequired, URL  # Import validators for form fields

# Initialize the Flask application
app = Flask(__name__)

# Set secret key for session management
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize Bootstrap with the Flask app
Bootstrap5(app)

# Define admin key for accessing restricted parts of the application
ADMIN_KEY = "TopSecretKey"


# CREATE DB
class Base(DeclarativeBase):
    pass  # Define base class for SQLAlchemy models


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'  # Set the database URI for SQLite
db = SQLAlchemy(model_class=Base)  # Initialize SQLAlchemy with the Base model class
db.init_app(app)  # Bind SQLAlchemy to the Flask app


# Add Cafe Form
class AddCafe(FlaskForm):
    # Define form fields with appropriate validators
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Cafe Maps URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    sockets = StringField("Does cafe have sockets? (yes/no)", validators=[DataRequired()])
    wifi = StringField("Does cafe have Wifi? (yes/no)", validators=[DataRequired()])
    toilet = StringField("Does cafe have toilet? (yes/no)", validators=[DataRequired()])
    calls = StringField("Can cafe take calls? (yes/no)", validators=[DataRequired()])
    seats = StringField("How many seats are there?", validators=[DataRequired()])
    coffee_price = StringField("What's the coffee price? E.g. £2.75", validators=[DataRequired()])
    open_hours = StringField("When does the cafe open?", validators=[DataRequired()])
    close_hours = StringField("When does the cafe close?", validators=[DataRequired()])
    submit = SubmitField('Add Cafe')  # Submit button

    def validate_yes_no_fields(self):
        # Validate yes/no fields to ensure correct input
        fields = [self.sockets, self.wifi, self.toilet, self.calls]
        for field in fields:
            if field.data.lower() not in ['yes', 'no']:
                field.errors.append('Must be "yes" or "no".')
                return False
        return True

    def to_bool(self, value):
        # Convert yes/no strings to boolean values
        return value.lower() == 'yes'


# Cafe TABLE Configuration
class Cafe(db.Model):
    # Define the structure of the Cafe table in the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    open_hours = db.Column(db.String(250), nullable=False)
    close_hours = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()  # Create all tables in the database


@app.route('/')
def home():
    # Query all cafes from the database
    cafes = Cafe.query.all()
    is_admin = session.get('is_admin', False)  # Check if the user is an admin
    # Render the home page with a list of cafes and admin status
    return render_template('index.html', cafes=cafes, is_admin=is_admin)


@app.route('/add-cafe', methods=["GET", "POST"])
def add_cafe():
    form = AddCafe()  # Initialize the form for adding a cafe
    if form.validate_on_submit() and form.validate_yes_no_fields():
        # If form is submitted and validated, create a new Cafe object
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.to_bool(form.sockets.data),
            has_wifi=form.to_bool(form.wifi.data),
            has_toilet=form.to_bool(form.toilet.data),
            can_take_calls=form.to_bool(form.calls.data),
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            open_hours=form.open_hours.data,
            close_hours=form.close_hours.data
        )
        db.session.add(new_cafe)  # Add the new cafe to the database session
        db.session.commit()  # Commit changes to the database
        return redirect(url_for('home'))  # Redirect to the home page
    return render_template('add_cafe.html', form=form)  # Render the add cafe page with the form


@app.route('/edit-cafe/<int:cafe_id>', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)  # Get the cafe by its ID
    # Initialize the form with the cafe's current data
    form = AddCafe(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        sockets='yes' if cafe.has_sockets else 'no',
        wifi='yes' if cafe.has_wifi else 'no',
        toilet='yes' if cafe.has_toilet else 'no',
        calls='yes' if cafe.can_take_calls else 'no',
        seats=cafe.seats,
        coffee_price=cafe.coffee_price,
        open_hours=cafe.open_hours,
        close_hours=cafe.close_hours
    )
    if form.validate_on_submit() and form.validate_yes_no_fields():
        # If form is submitted and validated, update the cafe's data
        cafe.name = form.name.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.has_sockets = form.to_bool(form.sockets.data)
        cafe.has_wifi = form.to_bool(form.wifi.data)
        cafe.has_toilet = form.to_bool(form.toilet.data)
        cafe.can_take_calls = form.to_bool(form.calls.data)
        cafe.seats = form.seats.data
        cafe.coffee_price = form.coffee_price.data
        cafe.open_hours = form.open_hours.data
        cafe.close_hours = form.close_hours.data
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('home'))  # Redirect to the home page
    return render_template('add_cafe.html', form=form, is_edit=True)  # Render the edit cafe page with the form


@app.route('/delete-cafe/<int:cafe_id>', methods=["POST"])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)  # Get the cafe by its ID
    db.session.delete(cafe)  # Delete the cafe from the database session
    db.session.commit()  # Commit the deletion to the database
    return redirect(url_for('home'))  # Redirect to the home page


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Run the Flask app in debug mode on port 5001
