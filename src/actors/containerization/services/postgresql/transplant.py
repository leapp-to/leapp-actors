from leapp import Actor as actor, object_with_parent, get_command_output, call_command_with_input, bail, Severity


snapshots = actor.get_input('postgresql_snapshot')
done = 0

for snapshot in snapshots:
    command = call_command_with_input(['pg_restore', '-C', '-d', 'postgres',
                                       '-F', 't'], snapshot['payload'])

    if command.wait() != 0:
        message = 'Error restoring postgresql snapshot {}/{}'
        bail(Severity.Fatal, message.format(done, len(snapshots)))

    credentials = actor.get_dependent_result(snapshot)
    get_command_output(
        'psql -c "ALTER USER {user_id} PASSWORD \'{password}\';"'.format(**credentials))

    done += 1

actor.done()
