# CookBook

Bugs

1. Issue where user id's were not incrementing as expected - Fixed by changing key in IF statement from "user" to "user_id"
2. Issue with key errors displaying when singing out and being redirected to home screen - fixed by changing the session check syntax from session["user"] to "user" in session
3. Bug noted where dynamically adding fields in form and submitting empty would result in pushing empty strings into the array - fixed by filtering out the empty strings from the list before buidling the dictionary in the funtion.
