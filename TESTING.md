# Testing

## Manual Testing

Manual testing was completed by myself as I developed the project, making sure I manually tested each component as it was added, I used Google Chrome Devtools to view the code from the browser alongside the rendered site.

Once I had the full functionality up and running, I asked friends family and my Code Institute cohort to use the site as much as possible to see whether there were any UX ommissions or components that didn't work as they would expect as a real life user. 

This proved insightful as other people managed to come across issues that I didn't face as the admin user of the site that I may have missed had I not planned to go back and test as a regular user once everything was completed. Getting the site live early meant I could fix these issues one by one earlier rather than finding them all later on in the develepment and possibly having to edit more as a chain reaction.

## User Stories

The below tables detail the paths I followed on the site to test each of the user stories, also documented with screenshots of the components and location on the site.

### First time user

|                                                                       Story                                                                        | Site Path | Images |
| :------------------------------------------------------------------------------------------------------------------------------------------------: | :-------: | :---: |
|                   See a description of the site and be able to view all recipe and category content, including detailed recipes.                   | Home page, click menu, click recipes/categories, view content, click pop out button on recipe card for details.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/anon1a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon1b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon1c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon1d.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon1e.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon1f.webp)      |
|                                           Have a clear navigation menu that is consistently accessible.                                            | Click menu icon in top right corner, visible on all screens, click CookBook logo to navigate to Navigate to Home          | ![User Story Screenshot](/static/images/readme/testing/user_stories/anon2a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon2b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon2c.webp)      |
| Have prompts to register for an account to get more from the site and find an easy to complete registration form with helpful form field feedback. | Visibile on Home page in About Us section OR click Menu, click Register. Fill in details, prompts display if formats are incorrect         | ![User Story Screenshot](/static/images/readme/testing/user_stories/anon3a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon3b.webp)      |
|                                     Find a contact page to submit feedback to admin with queries or comments.                                      | Click Get In Touch button in footer OR Menu, click Contact, fill in details, receive feedback if email in incorrect format, click submit, receive feedback message on home screen          | ![User Story Screenshot](/static/images/readme/testing/user_stories/anon4a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon4b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/anon4c.webp)      |

### Registered user

|                                                       Story                                                        | Site Path | Images |
| :----------------------------------------------------------------------------------------------------------------: | :-------: | :---: |
|       Find a simple sign in page to log in to my account, giving feedback on incorrect account information.        | Click Menu, click Sign In OR from Register page, click Sign In link, input details incorrectly, click sign in button, receive feedback message and return to sign in page to log in correctly         | ![User Story Screenshot](/static/images/readme/testing/user_stories/user1a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user1b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user1c.webp)       |
| See my details on a profile page, including personal information, recipes I have created and recipes I have liked. | Sign in OR IF SIGNED IN click Menu, click on profile picture, view profile card with details, scroll to view My Recipes, scroll to view Liked Recipes          | ![User Story Screenshot](/static/images/readme/testing/user_stories/user2a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user2b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user2c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user2d.webp)      |
|           Add new recipes with an entry form including dynamic fields for ingredients and instructions.            | From recipes or filtered recipe page, click + button in bottom right corner OR click Menu, click + Add Recipe, click + next to ingredients to add new line after, click + next to ingredients to add new line after, click - to remove any lines not needed. Click submit, receive feedback on successfully adding recipe.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/user3a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user3b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user3c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user3d.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user3e.webp)      |
|                           Update or delete my details, including recipes I have created.                           | From Profile, click Edit Details/Delete button OR on recipe cards, click pencil/bin icon, FOR EDIT update details and click Update button. Confirm password if editing user details. FOR DELETE, confirm in confirmation modal, enter password to delete account. Receive confirmation message.       | ![User Story Screenshot](/static/images/readme/testing/user_stories/user4a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user4b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user4c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user4d.webp)      |
|                   Add/remove likes to recipes and view list of liked recipes on my profile page.                   | Click Like button on recipe card I haven't yet liked, review card to see Liked button turns pink. Navigate to Menu, Profile picture, scroll down to Liked Recipes section to review liked recipe is in list, click like button to unlike, scroll down to liked recipes section to review recipe is no longer in list          | ![User Story Screenshot](/static/images/readme/testing/user_stories/user5a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user5b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user5c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/user5d.webp)      |

### Super user

|                                                         Story                                                         | Site Path | Images |
| :-------------------------------------------------------------------------------------------------------------------: | :-------: | :---: |
|                       Add new categories for use on recipes with a consistent submission form.                        | From categories page, click + button in button right OR click Menu, click + Add Category, fill in details, click submit button, receive feedback confirming success          | ![User Story Screenshot](/static/images/readme/testing/user_stories/super1a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/super1b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/super1c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/super1d.webp)      |
| Update or delete category information on all categories and have changes show up across all existing applicable tags. | From categories page, click pencil icon for edit/bin icon for delete. FOR EDIT, amend any details and click submit. FOR DELETE, confirm on confirmation modal. Receive feedback message.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/super2a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/super2b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/super2c.webp)      |
|                          See a visual badge on my profile page to denote super user status.                           | Click Menu, click profile picture, view Super User star icon with tooltip          | ![User Story Screenshot](/static/images/readme/testing/user_stories/super3.webp)      |

### Admin user

|                                        Story                                         | Site Path | Images |
| :----------------------------------------------------------------------------------: | :-------: | :---: |
| Have full access to update or delete recipes and categories directly from the cards. | On recipe or category cards, click pencil/bin icon to edit/delete. FOR EDIT, update applicable details, click update button. FOR DELETE, confirm on confirmation modal. Receive feedback message.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/admin1a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin1b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin1c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin1d.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin1e.webp)      |
|       See a page of all users with options to update details or delete users.        | Click Menu, click Users, click pencil/bin icon to edit/delete user. FOR EDIT, update applicable details, click Update button. Input password to confirm edit/delete. Receive feedback message.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/admin2a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin2b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin2c.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin2d.webp)      |
|   See dedicated buttons for changing the super user and admin status of all users.   | From Users page, click star/person icon to add/remove super/admin status. Review user card to see change updated and highlighting added/removed to applicable icon.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/admin3a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin3b.webp)      |
|                See a page of messages sent through from the contact page and to be able to delete messages.                 | Click Menu, click Messages, click header to expand message and view details, click bin icon to delete, click to confirm in confirmation modal. Receive feedback message.          | ![User Story Screenshot](/static/images/readme/testing/user_stories/admin4a.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin4b.webp)![User Story Screenshot](/static/images/readme/testing/user_stories/admin4c.webp)      |
|          See a visual badge on my profile page to denote admin user status.          | Click Menu, click Profile picture, view Admin User icon with tooltip          | ![User Story Screenshot](/static/images/readme/testing/user_stories/admin5.webp)      |

🔽🔽🔽🔽🔽
## Code Validators

### HTML



### CSS

I used [W3 CSS Validator](https://jigsaw.w3.org/css-validator/validator) to validate the style.css file and received no errors.

![CSS Validation Screenshot](/static/images/readme/testing/testcss.webp)

### JavaScript

I used [JsHint](https://jshint.com/) to check the script.js file for errors and after adding the ```/*jshint esversion: 6 */``` line to the top of the file to counter the ES6 errors, I only received undefined variable notes from the jquery materialize calls and unused variable notes from the functions which are all called directly from on clicks on the HTML files.

![JS Validation Screenshot](/static/images/readme/testing/testjs.webp)

### Python

I used the [Code Institue Python Linter](https://pep8ci.herokuapp.com/) to check the app.py for errors, after fixing some whitespace errors and lines which were too long, I retested to find there were no errors.

![Python Validation Screenshot](/static/images/readme/testing/testpython.webp)

## Lighthouse

I used Google Chrome Dev Tools Lighthouse function to check the performance, accessibility and search engine optimization with scores documented below and notes to explain reduced scores in certain areas.

Home

-   Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user.

![Home Lighthouse Screenshot](/static/images/readme/testing/homelh.webp)

Register

-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Register Lighthouse Screenshot](/static/images/readme/testing/registerlh.webp)

Sign In

-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Sign In Lighthouse Screenshot](/static/images/readme/testing/signinlh.webp)

Recipes

-   Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user.

![Recipe Lighthouse Screenshot](/static/images/readme/testing/recipeslh.webp)

Recipe Details

-   Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user.
-   SEO reduction due to the floating more options Materialize button not being crawlable.

![Recipe Details Lighthouse Screenshot](/static/images/readme/testing/recipedetailslh.webp)

Add Recipe

- lower accessibility score due to dynamic instructions and ingredients sections which do not have individual labels for the inputs, rather a group label
-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Add Recipe Lighthouse Screenshot](/static/images/readme/testing/addrecipelh.webp)

Edit Recipe

- lower accessibility score due to dynamic instructions and ingredients sections which do not have individual labels for the inputs, rather a group label
-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Edit Recipe Lighthouse Screenshot](/static/images/readme/testing/editrecipelh.webp)

Categories

![Categories Lighthouse Screenshot](/static/images/readme/testing/categorylh.webp)

Add Category

-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Add Category Lighthouse Screenshot](/static/images/readme/testing/addcategorylh.webp)

Edit Category

-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Edit Category Lighthouse Screenshot](/static/images/readme/testing/editcategorylh.webp)

Profile

-   Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user.

![Profile Lighthouse Screenshot](/static/images/readme/testing/profilelh.webp)

Edit Details

-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Edit Details Lighthouse Screenshot](/static/images/readme/testing/editdetailslh.webp)

Users

-   Performance score reduction due to the images being URL linked rather than appropriately sized and formatted uploads direct from the user.

![Users Lighthouse Screenshot](/static/images/readme/testing/userslh.webp)

Messages

![Messages Lighthouse Screenshot](/static/images/readme/testing/messageslh.webp)

Contact

-   Form card reducing accessibility score due to being the same colour as the background, this was a design choice to keep the colour pallete simple and clean so as to not become distracting to the user.

![Contact Lighthouse Screenshot](/static/images/readme/testing/contactlh.webp)

[Back to README](README.md)
