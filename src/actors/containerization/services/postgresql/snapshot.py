from leapp import Actor as actor, object_with_parent, get_command_output


def _data_export_command(db):
    cmd = 'sudo -u {system_user_id} PGPASSWORD={password} pg_dump -F t -U {user_id} {database_name}'
    return cmd.format(**db)


for database in actor.get_input('postgresql_database'):
    export_command = _data_export_command(database)

    database_data = {'payload': get_command_output(export_command)}
    actor.output('postgresql_snapshot',
                 object_with_parent(database_data, database))

actor.done()
