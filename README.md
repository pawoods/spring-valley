Bugs

1. Issue where user id's were not incrementing as expected - Fixed by changing key in IF statement from "user" to "user_id"
2. Issue with key errors displaying when singing out and being redirected to home screen - fixed by changing the session check syntax from session["user"] to "user" in session
3. 