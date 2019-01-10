
<!--lint disable no-heading-punctuation-->
# Surfs Up!
<!--lint enable no-heading-punctuation-->

<img src='images/surfs-up.jpeg'/>

We decided to create a climate analysis and app for our favorite vacation destination- Hawaai.

## First - We created a notebook dedicated for Database Engineering

We use SQLAlchemy to model our table schemas and create a sqlite database for our tables. We weill be needing one table for measurements and one for stations.
- Use Pandas to read our cleaned measurements and stations CSV data.
- Use the engine and connection string to create a database called hawaii.sqlite.
- Use declarative_base and create ORM classes for each table.

## Secondly - we created a notebook dedicated for Climate Analysis and Exploration

We use Python and SQLAlchemy to do basic climate analysis and data exploration on our new weather station tables. 
- Used SQLAlchemy ORM queries, Pandas, and Matplotlib.

## Finally we created a Climate App
Now that we have completed your initial analysis, we design a Flask api based on the queries that we have just developed.
- We use FLASK to create our routes.

### Routes

* `/api/v1.0/precipitation`

  * Query for the dates and temperature observations from the last year.

  * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

  * Return the json representation of your dictionary.

* `/api/v1.0/stations`

  * Return a json list of stations from the dataset.

* `/api/v1.0/tobs`

  * Return a json list of Temperature Observations (tobs) for the previous year

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


