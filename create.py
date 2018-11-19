from database import db,Puppy

# This is how you create an entry to database
# create an instance of Puppy
my_puppy = Puppy('Rufus',5, 'Golden Retriever')

# save it to database with the following 2 lines of code
db.session.add(my_puppy)
db.session.commit()