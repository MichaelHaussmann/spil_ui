import sys
from action.broker import Broker

class BaseEngine(object):

    name = 'Base'
    implements = []
    needs_confirm = []

    def __init__(self):
        self.action_broker = Broker()

    def get_actions(self, sid):
        actions = self.action_broker.get_actions(sid, self.name.lower())
        return (a.get('name') for a in actions)

    def get_current_sid(self):
        """
        Returns the "current" Sid.
        Might not be always implemented.
        """
        return None

    def run_action(self, name, sid):
        self.action_broker.run_action(name, sid, self)

    def __str__(self):
        return '{} @ {}'.format(self.__class__.__name__, sys.executable)


if __name__ == '__main__':

    e = BaseEngine()
    print(e)