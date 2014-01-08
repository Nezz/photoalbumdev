group-1-2013
============

General plan (described in the implementation order): 
- Design a database scheme with the following entities:
    = Album
    = Slide
    = Photo 
    = User
    = Order
- Develop models based on the DB scheme:
    = User (one-to-many connection with Album  and Order entities)
    = Album (one-to-many connection with Slide entity)
    = Slide (one-to-many connection with Photo entity)
    = Photo (contains the Link and the Caption)
    = Order
- Create and run simple tests for models
- Designing the following templates and elementary logic:
    = Welcome screen
    = Registration (results into creating a new User instance)
    = Login (checks credentials and changes the state of the user)
    = Dashboard which contains the album list and order history (renders all Album and Order instances created by the current User)
    = Album viewer (Renders the Slide instances of the current Album in a specific order)
    = Album editor (Renders the Slide instances of the current Album in a specific order and allows changes to both current Album instance and Slide instances)
    = Order placement (results into creating a new Order instance)
    = Profile editor (changes the User instance fields)
- Designing the templates for albums slides
- Developing the back-end logic including the following features:
    = User's authentication (login, logout, register)
    = Automatic e-mailing (registration confirmation, order confirmation, etc)
    = Album logic (create, delete, edit, share, etc)
    = Order logic (create, pay, finalize, cancel)
    = Social media sharing
- Create and run tests for the back-end logic
- Design improvements (Twitter Bootstrap)
- Additional logic:
    = 3rd party login
    = AJAX
    = Flickr API integration
    
Project milestones:
- The first version of models is ready for testing: January 15th
- Templates are ready and tested to work with the models and the elementary logic is implemented and tested: January 23rd
- All the logic is implemented: February 5th
- Additional logic is implemented and the design is improved: February 11th


