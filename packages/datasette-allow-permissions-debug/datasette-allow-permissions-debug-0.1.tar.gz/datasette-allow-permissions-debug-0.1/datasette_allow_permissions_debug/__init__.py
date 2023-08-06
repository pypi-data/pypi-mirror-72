from datasette import hookimpl


@hookimpl
def permission_allowed(action):
    if action == "permissions-debug":
        return True
