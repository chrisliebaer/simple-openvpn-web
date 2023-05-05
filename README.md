This is a little web frontend that I wrote for managing low security logins to an OpenVPN layer 2 tunnel for playing LAN games. This project is build for easy of use. It stores passwords in plain text, has no authentication but it does however make it trivial to distribute logins.

# Features
* Stores passwords in plain text(!!) in an actual `text/plain` file. (I heard you like plaintext...)
* Management of users (create, delete, update).
* Copy button which will copy a preformatted message into clipboard, ready to be send to friends.
* No access control. You need to bring your own.
* Comes with a script to use with OpenVPN for validating logins.
* Looks janky as shit.
* Even has a Docker image.

# Demo
![Example Screenshot of Website](demo.png)