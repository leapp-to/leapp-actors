from leapp import Actor as actor


# deduplicate results based on absolute config path
for database in actor.get_input('raw_postgresql_database'):
    pass


actor.done()
