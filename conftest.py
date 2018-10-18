import os

from leapp.repository.scan import scan_repo


def pytest_sessionstart(session):
    actor_path = os.environ.get('LEAPP_TESTED_ACTOR', None)
    if not actor_path:
        return
    repo = scan_repo(('/'.join(actor_path.split('/')[:-2])))
    repo.load()

    actor = None
    # find which actor is being tested
    for a in repo.actors:
        if a.full_path == actor_path:
            actor = a
            break

    if not actor:
        return

    # load actor context so libraries can be imported on module level
    session.actor_context = actor.injected_context()
    session.actor_context.__enter__()
