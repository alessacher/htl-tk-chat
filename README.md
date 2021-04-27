# htl-tk-chat
Watch the development progress at https://gitea.escpe.net/cc69222/htl-tk-chat

# Build documentation
To build the documentation run:

```bash
make doc
```

After this you can open the documentation.pdf.

For lazy people or Windows folks, a precompiled version of the documentation can be found [here](./documentation.pdf).
# Project description
A Server and client for a self-written chat application.
The client interface uses Qt 6, the server uses sockets and msgpack.
## Planned features:
- Selecting users to send messages to ("Public", "Private")
- Notify users when new messages are available (for them)
- database to store message history
- attachments (files)
- embedded pictures in chat
- authentification / identification of users via username
- encryption ? (GPG) or SSL -> Let's Encrypt for server

# What we use, what we do
- sockets, tcp streams
- ~~JSON for message content and metadata~~
- msgpack for message content and metadata, because it is faster and encodes in binary instead of strings.
- Server, self written, hosted at home (port forwarding)
- Database server-side for message-history, users, authentification
- For the Database SQLite, cause it is a lightweight disk-based database and doesn't require a separate server process. Also the sqlite3 python module is in [The Python Standard Library](https://docs.python.org/3/library/).
- We don't care about networking failures, we let tcp handle that.
- Interface in ~~tkinter~~ or **Qt 6** (via PyQt6)
- Doxygen for documentation

# Rules
- Commit messages should make sense
- If you're planning to implement a new feature, open an issue with the correct label
- Working on the development branch and after the one week sprint make a pull request, to merge it back to the master.
- Write sensible reviews and document your Code

# Milestone 1
- Server is running and accessible from the internet
- Clients send messages to Server, the Server broadcasts the message to all Clients.

