# htl-tk-chat

Simple python chat application with tk frontend.


# What we use, what we do
- urllib
- JSON for message content and metadata
- Server, self written, hosted at home (port forwarding)
- Database server-side for message-history, users, authentification
- We don't care about networking failures, we let tcp handle that.
- Interface in tkinter or **qt5** (nonplusultra)

# Rules
- Commit messages should make sense

# Milestone 1
- Server is running and accessible from the internet
- Clients send messages to Server, the Server broadcasts the message to all Clients.
