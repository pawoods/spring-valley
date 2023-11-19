# CookBook

Bugs

1. Issue where user id's were not incrementing as expected - Fixed by changing key in IF statement from "user" to "user_id"
2. Issue with key errors displaying when singing out and being redirected to home screen - fixed by changing the session check syntax from session["user"] to "user" in session
3. Bug noted where dynamically adding fields in form and submitting empty would result in pushing empty strings into the array - fixed by filtering out the empty strings from the list before buidling the dictionary in the funtion.
4. Bug using accordion and expandable collapsibles where jQuery .collapsible() overwrote the .expandable JavaScript - Fixed by adding a second class (messages) to the accordion element and the jQuery selector 
5. Bug found where admin cannot see edit and delete buttons on other users recipe cards on home screen under popular recipes - fixed by adding in the missing or user.is_admin to the jinja if statement
6. Bug found where users could edit or delete other users recipes from the liked recipe section of their profile page - Fixed by adding in the missing jinja if statement around the edit and delete buttons.
7. Bug found where bringing up the delete user modal from the ser page caused the input to be unclickable - fixed by changing the id and name of the input by appending the user id to the end of the string meaning they would each now be unique. 

Remaining bugs

1. Redirect using the session url works well in majority of normal use cases, although where a user navigates using back button, the browser will load a cahced version of the page and won't overwrite the url in session. Meaning, when a user then triggers another function (like, delete etc.), they will be returned to the last page that stores the url in session. 


$ne operator learned from <https://developerslogblog.wordpress.com/2019/10/15/mongodb-how-to-filter-by-multiple-fields/>
