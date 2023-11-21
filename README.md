# CookBook

Description of site, purpose and reason.
Am I responsive screenshot
Live site - https://project-3-pawoods-dcf83ae94f0f.herokuapp.com/

## Table of Contents

-   [UX](#ux)
    -   [User Stories](#user-stories)
    -   [Design](#design)
        -   [Wireframes](#wireframes)
        -   [Data Design](#data-design)
    -   [Themes](#themes)
        -   [Colours](#colours)
        -   [Fonts](#fonts)
        -   [Icons](#icons)
-   [Features](#features)
    -   [Current Features](#current-features)
        -   [Page Features Matrix](#page-features-matrix)
        -   [User Feature Visibility](#user-features-visibility)
    -   [Future Features](#future-features)
-   [Languages and Technologies](#languages-and-technologies)
-   [Testing](#testing)
    -   [Bugs](#bugs)
        -   [Fixed Bugs](#fixed-bugs)
        -   [Unfixed Bugs](#unfixed-bugs)
-   [Deployment](#deployment)
    -   [Live Deployment](#live-deployment)
    -   [Local Deployment](#local-deployment)
-   [Credits](#credits)

## UX

### User stories

I wrote up the below user stories to ensure I kept the users in mind when creating the site. As I planned to have a multi level permission structure, I made a note to ensure each next level had full visibility and functionality of the user level below:

1. First time User

    - See a description of the site and be able to view all recipe and category content, including detailed recipes.**********
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

### Design

#### Wireframes
(external File)
Mobile (Portrait/Landscape)
Tablet (Portrait/Landscape)
Desktop

#### Data design

As a data driven project, I wanted to make sure I thoroughly planned the data that would be stored in the database, how each document would link to eachother and how the user would interact with the data on the front end, considering full CRUD functionality. I Wrote up the following document plans to keep in mind when writing the python logic and applicable forms.

Users:
```
{
    _id: ObjectId,
    user_id: integer,
    f_name: string,
    l_name: string,
    username: string,
    email: string,
    password: hashed password,
    user_since: datetime object,
    photo_url: string,
    is_super: boolean,
    is_admin: boolean
}
```

Categories:
```
{
    _id: ObjectId,
    category_name: string,
    category_description: string,********
    category_color: string
}
```

Recipes:
```
{
    _id: ObjectId
    recipe_name: string,
    recipe_description: string,
    categories: [ //multiple categories can be added
        {
            _id: (from category)
            category_name: (from category),
            category_description: (from category),
            category_color: (from category)
        }
    ],
    ingredients: [
        "Ingredient 1", "Ingredient 2" ...
    ],
    "Instructions": [
        "Instruction 1", "Instruction 2" ...
    ],
    "prep_time": integer,
    "cook _time": integer,
    "serves": Integer,
    "likes": {
        count: integer,
        id: [
            (id from user), (id from user2)...
        ]
    },
    "created_by": {
        "username": (from user),
        "user_id": (from user)
    },
    "created_date": datetime object
}
```

Messages:
```
{
    _id: ObjectId,
    user_name: string (from user if signed in),
    user_email: string (from user if signed in),
    message_date: datetime object,
    message_content: string
}
```

### Themes

#### Colours

#### Fonts

#### Icons

## Features

### Current Features

#### Page Feature Matrix

#### User Feature Visibility

To help guide me within the development process and ensure I made all features available for the relevent users, I found it helpful to visualise applicable users for each feature in a table:

| PAGE/Feature             | Anonymous User | Registered User | Super User | Admin |
| :----------------------- | :------------: | :-------------: | :--------: | :---: |
| HOME                     |       ✅       |       ✅        |     ✅     |  ✅   |
| New Recipes              |       ✅       |       ✅        |     ✅     |  ✅   |
| Popular Recipes          |       ✅       |       ✅        |     ✅     |  ✅   |
| RECIPES/FILTERED RECIPES |       ✅       |       ✅        |     ✅     |  ✅   |
| Recipe Card              |       ✅       |       ✅        |     ✅     |  ✅   |
| - Likes                  |      View      |       ✅        |     ✅     |  ✅   |
| - Details                |       ✅       |       ✅        |     ✅     |  ✅   |
| - Edit                   |       ❌       |    If Owner     |  If Owner  |  ✅   |
| - Delete                 |       ❌       |    If Owner     |  If Owner  |  ✅   |
| - Category Filters       |       ✅       |       ✅        |     ✅     |  ✅   |
| Menu (Signed Out)        |       ✅       |       ✅        |     ✅     |  ✅   |
| - Home                   |       ✅       |       ✅        |     ✅     |  ✅   |
| - Recipes                |       ✅       |       ✅        |     ✅     |  ✅   |
| - Sign In                |       ✅       |       ✅        |     ✅     |  ✅   |
| - Register               |       ✅       |       ✅        |     ✅     |  ✅   |
| - Contact                |       ✅       |       ✅        |     ✅     |  ✅   |
| Menu (Signed In)         |       ❌       |       ✅        |     ✅     |  ✅   |
| - Home                   |       ❌       |       ✅        |     ✅     |  ✅   |
| - Recipes                |       ❌       |       ✅        |     ✅     |  ✅   |
| - Add Recipe             |       ❌       |       ✅        |     ✅     |  ✅   |
| - Categories             |       ❌       |       ✅        |     ✅     |  ✅   |
| - Add Categories         |       ❌       |       ❌        |     ✅     |  ✅   |
| - Profile                |       ❌       |       ✅        |     ✅     |  ✅   |
| - Contact                |       ❌       |       ✅        |     ✅     |  ✅   |
| - Users                  |       ❌       |       ❌        |     ❌     |  ✅   |
| - Messages               |       ❌       |       ❌        |     ❌     |  ✅   |
| - Sign Out               |       ❌       |       ✅        |     ✅     |  ✅   |
| ADD RECIPE               |       ❌       |       ✅        |     ✅     |  ✅   |
| EDIT RECIPE              |       ❌       |    If Owner     |  If Owner  |  ✅   |
| CONTACT                  |       ✅       |       ✅        |     ✅     |  ✅   |
| Contact Form             |       ✅       |       ✅        |     ✅     |  ✅   |
| - Pre Populated          |       ❌       |       ✅        |     ✅     |  ✅   |
| CATEGORIES               |       ✅       |       ✅        |     ✅     |  ✅   |
| Category Card            |       ✅       |       ✅        |     ✅     |  ✅   |
| - Filter Button          |       ✅       |       ✅        |     ✅     |  ✅   |
| - Edit                   |       ❌       |       ❌        |     ✅     |  ✅   |
| - Delete                 |       ❌       |       ❌        |     ✅     |  ✅   |
| ADD CATEGORY             |       ❌       |       ❌        |     ✅     |  ✅   |
| EDIT CATEGORY            |       ❌       |       ❌        |     ✅     |  ✅   |
| PROFILE (User Specific)  |       ❌       |       ✅        |     ✅     |  ✅   |
| Liked Recipe Cards       |       ❌       |       ✅        |     ✅     |  ✅   |
| Owned Recipe Cards       |       ❌       |       ✅        |     ✅     |  ✅   |
| Delete Account           |       ❌       |       ✅        |     ✅     |  ✅   |
| EDIT DETAILS             |       ❌       |     If User     |  If User   |  ✅   |
| USERS                    |       ❌       |       ❌        |     ❌     |  ✅   |
| User Card                |       ❌       |       ❌        |     ❌     |  ✅   |
| Make Super               |       ❌       |       ❌        |     ❌     |  ✅   |
| Make Admin               |       ❌       |       ❌        |     ❌     |  ✅   |
| Edit Details             |       ❌       |       ❌        |     ❌     |  ✅   |
| Delete Account           |       ❌       |       ❌        |     ❌     |  ✅   |
| RECIPE DETAILS           |       ✅       |       ✅        |     ✅     |  ✅   |
| All Details              |       ✅       |       ✅        |     ✅     |  ✅   |
| Likes                    |      View      |       ✅        |     ✅     |  ✅   |
| Edit                     |       ❌       |    If Owner     |  If Owner  |  ✅   |
| Delete                   |       ❌       |    If Owner     |  If Owner  |  ✅   |

### Future Features

Features that were part of my initial scope but deemed a lower priority and therefore forming my future features are as follows:

- Direct photo upload from user, using cloudinary or similar technology - As noted in testing, the URL links add the risk of large files and therefore long page loads and lower performance.
- Add shopping list feature to user profile where users can click an icon next to ingredients on a recipe to add to a shopping list for future use.

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

1. Issue where user id's were not incrementing as expected. 
    - Fixed by changing key in IF statement from "user" to "user_id"
2. Issue with key errors displaying when singing out and being redirected to home screen.
    - Fixed by changing the session check syntax from session["user"] to "user" in session.
3. Bug noted where dynamically adding fields in form and submitting empty would result in pushing empty strings into the array.
    - Fixed by filtering out the empty strings from the list before buidling the dictionary in the funtion.
4. Bug using accordion and expandable collapsibles where jQuery .collapsible() overwrote the .expandable JavaScript. 
    - Fixed by adding a second class (messages) to the accordion element and the jQuery selector.
5. Bug found where admin cannot see edit and delete buttons on other users recipe cards on home screen under popular recipes. 
    - fixed by adding in the missing or user.is_admin to the jinja if statement.
6. Bug found where users could edit or delete other users recipes from the liked recipe section of their profile page. 
    - Fixed by adding in the missing jinja if statement around the edit and delete buttons.
7. Bug found where bringing up the delete user modal from the user page caused the input to be unclickable. 
    - Fixed by changing the id and name of the input by appending the user id to the end of the string meaning they would each now be unique.
8. Bug created by the above fix meant users deleting their account from their profile faced a Werkzeug error.
    - Fixed by adding the user's id to the id of the input field so it can be picked up in the same way as from the users page by the app.route function.
9. Bug found where custom user ids were being reused when a user deleted their account, leading to the likes from the previous user showing up for the next user to register.
    - Fixed by creating a new DB collection with a single document called used_ids. On every register, the generated id is pushed into an array on this document and this is what is checked instead of the user_id from the users DB collection.
10. Bug found where dynamic "instruction" or "ingredients" fields could all be removed from the add_recipe form.
    - Fixed by adding in a check on remove() function to count the children of the list and add another child if all input field children are deleted.

#### Unfixed Bugs

1. Redirect using the session url works well in majority of normal use cases, although where a user navigates using back button, the browser will load a cahced version of the page and won't overwrite the url in session. Meaning, when a user then triggers another function (like, delete etc.), they will be returned to the last page that stores the url in session.

## Deployment

### Live

### Local

## Credits

$ne operator learned from <https://developerslogblog.wordpress.com/2019/10/15/mongodb-how-to-filter-by-multiple-fields/>
