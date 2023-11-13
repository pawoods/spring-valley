# CookBook

Bugs

1. Issue where user id's were not incrementing as expected - Fixed by changing key in IF statement from "user" to "user_id"
2. Issue with key errors displaying when singing out and being redirected to home screen - fixed by changing the session check syntax from session["user"] to "user" in session
3. Bug noted where dynamically adding fields in form and submitting empty would result in pushing empty strings into the array - fixed by filtering out the empty strings from the list before buidling the dictionary in the funtion.
4. Bug using accordion and expandable collapsibles where jQuery .collapsible() overwrote the .expandable JavaScript - Fixed by adding a second class (messages) to the accordion element and the jQuery selector 
5. Bug found where admin cannot see edit and delete buttons on other users recipe cards on home screen under popular recipes - fixed by adding in the missing or user.is_admin to the jinja if statement

$ne operator learned from <https://developerslogblog.wordpress.com/2019/10/15/mongodb-how-to-filter-by-multiple-fields/>
