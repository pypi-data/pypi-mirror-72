import weakref

__all__ = ['DRIVERS']


class BaseDriver(object):
    def __init__(self, parent):
        self.parent = weakref.ref(parent)

    @property
    def session(self):
        return self.parent()


class DriverV0(BaseDriver):
    def get_tasks(self, user=None):
        query = {'status': 'queued'}

        if user is not None:
            query['user'] = user

        response = self.session.get('/tasks', query=query)

        data = response.json()

        # Return in format of newer api versions
        data = {'tasks': [{'url': x} for x in data['tasks']]}

        return data


class DriverV1(BaseDriver):
    def get_tasks(self, user=None):
        query = {'status': 'queued'}

        if user is not None:
            query['user'] = user

        response = self.session.get('/tasks', query=query)

        data = response.json()
        return data


DRIVERS = {
    0: DriverV0,
    0.5: DriverV1,
    1: DriverV1
}
