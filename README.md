# CookBook

Description of site, purpose and reason.
Am I responsive screenshot
Live site - https://project-3-pawoods-dcf83ae94f0f.herokuapp.com/

## Table of Contents

## UX

### User stories
1. First time User
    - See a description of the site and be able to view all recipe and category content, including detailed recipes.
    - Have a clear navigation menu that is consistently accessible.
    - Have prompts to register for an account to get more from the site and find an easy to complete registration form with helpful form field feedback.
    - Find a contact page to submit feedback to admin with queries or comments.

2. Registered user (in addition to first time user)
    - Find a simple sign in page to log in to my account, giving feedback on incorrect account information. 
    - See my details on a profile page, including personal information, recipes I have created and recipes I have liked.
    - Add new recipes with an entry form including dynamic fields for ingredients and instructions.
    - Update or delete my details, including recipes I have created.
    - Add/remove likes to recipes and view list of liked recipes on my profile page.

3. Super user (in addition to registered user)
    - Add new categories for use on recipes with a consistent submission form.
    - Update of delete category information on all categories and have changes show up across all existing applicable tags.
    - See a visual badge on my profile page to denote super user status.

4. Admin user (in addition to super user)
    - Have full access to update or delete recipes and categories directly from the cards.
    - See dedicated buttons for changing the super user and admin status of all users. 
    - See a page of all users with options to update details or delete users.
    - See a page of messages sent through the contact page.
    - See a visual badge on my profile page to denote admin user status.

### Wireframes (external file)
Mobile (Portrait/Landscape)
Tablet (Portrait/Landscape)
Desktop
Data design
Visual Design

### Themes

#### Colours

#### Fonts

#### Icons

## Features
Current Features
Features to page matrix
Visibility Table
Future Features

## Languages and Technologies

## Testing (external file)

Manual Testing

User Stories (click path)

Code Validators
add_recipe.html - lower accessibility score due to dynamic instructions and ingredients sections which do not have individual labels for the inputs, rather a group label
cards reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.
Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user. 
Best Practices score reduction due to two of the linked image URLS causing Cookie issues in Chrome Devtools.
SEO reduction (Recipe Details) due to the floating more options Materialize button not being crawlable.

### Bugs

#### Fixed bugs

1. Issue where user id's were not incrementing as expected - Fixed by changing key in IF statement from "user" to "user_id"
2. Issue with key errors displaying when singing out and being redirected to home screen - fixed by changing the session check syntax from session["user"] to "user" in session
3. Bug noted where dynamically adding fields in form and submitting empty would result in pushing empty strings into the array - fixed by filtering out the empty strings from the list before buidling the dictionary in the funtion.
4. Bug using accordion and expandable collapsibles where jQuery .collapsible() overwrote the .expandable JavaScript - Fixed by adding a second class (messages) to the accordion element and the jQuery selector 
5. Bug found where admin cannot see edit and delete buttons on other users recipe cards on home screen under popular recipes - fixed by adding in the missing or user.is_admin to the jinja if statement
6. Bug found where users could edit or delete other users recipes from the liked recipe section of their profile page - Fixed by adding in the missing jinja if statement around the edit and delete buttons.
7. Bug found where bringing up the delete user modal from the user page caused the input to be unclickable - fixed by changing the id and name of the input by appending the user id to the end of the string meaning they would each now be unique.
8. Bug created by the above fix meant users deleting their account from their profile faced a Werkzeug error - fixed by adding the user's id to the id of the input field so it can be picked up in the same way as from the users page by the app.route function.

#### Remaining bugs

1. Redirect using the session url works well in majority of normal use cases, although where a user navigates using back button, the browser will load a cahced version of the page and won't overwrite the url in session. Meaning, when a user then triggers another function (like, delete etc.), they will be returned to the last page that stores the url in session. 

## Deployment

### Live

### Local

## Credits

$ne operator learned from <https://developerslogblog.wordpress.com/2019/10/15/mongodb-how-to-filter-by-multiple-fields/>
