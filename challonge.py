import challonge

# Tell pychal about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
challonge.set_credentials(os.getenv("challonge_users", os.getenv("challonge_token"))

# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show(3272)

# Tournaments, matches, and participants are all represented as normal Python dicts.
print(tournament["id"]) # 3272
print(tournament["name"]) # My Awesome Tournament
print(tournament["started_at"]) # None

# Retrieve the participants for a given tournament.
participants = challonge.participants.index(tournament["id"])
print(len(participants)) # 13

# Start the tournament and retrieve the updated information to see the effects
# of the change.
challonge.tournaments.start(tournament["id"])
tournament = challonge.tournaments.show(tournament["id"])
print(tournament["started_at"]) # 2011-07-31 16:16:02-04:00