# htl-tk-chat

Simple python chat application with tk (or maybe qt5) frontend.


# What we use, what we do
- sockets, tcp streams
- ~~JSON for message content and metadata~~
- msgpack for message content and metadate, because it is faster and encodes in binary instead of strings.
- Server, self written, hosted at home (port forwarding)
- Database server-side for message-history, users, authentification
- For the Database SQLite, cause it is a lightweight disk-based database and doesn't require a separate server process. Also the sqlite3 python module is in [The Python Standard Library](https://docs.python.org/3/library/).
- We don't care about networking failures, we let tcp handle that.
- Interface in tkinter or **qt5** (nonplusultra)

# Rules
- Commit messages should make sense
- If you're planning to implement a new feature, open an issue with the correct label
- Working on the development branch and after the one week sprint make a pull request, to merge it back to the master.
- Write sensible reviews and document your Code

# Milestone 1
- Server is running and accessible from the internet
- Clients send messages to Server, the Server broadcasts the message to all Clients.
