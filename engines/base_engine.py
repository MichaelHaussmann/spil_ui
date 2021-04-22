import sys


class BaseEngine(object):

    name = 'Base'
    implements = []
    needs_confirm = []

    def get_current_sid(self):
        """
        Returns the "current" Sid.
        Might not be always implemented.
        """
        return None

    def __str__(self):
        return '{} @ {}'.format(self.__class__.__name__, sys.executable)


if __name__ == '__main__':

    e = BaseEngine()
    print(e)