import logging
import importlib
from action.job_conf import job_config
from spil import LS, SpilException
from action.action_conf import universal_actions, global_actions, engine_actions


class Broker(object):
    """
    The broker is responsible for finding the Actions, and building the job Tree.
    It sends the jobs to the Runner, for submission or direct execution.

    Running modes are:
    - embedded
    - batch
    - farm
    - command server (not implemented)
    - service queue (not implemented)
    """

    def get_actions(self, sid, engine=None):
        """
        Returns a list of actions that are implemented for the given Sid.

        If engine is set, limits the result to the actions that are configured for this engine,
        meaning that they can run in embedded mode in this engine.


        Check if this is a correct statement because "engine" != "embedded engine".
        The Engine is the host, but "embedded" is a running mode.

        """

        found = ()

        # looking up engine specific actions
        if engine:
            engines = (engine,)
            try:
                found = filter(None,
                    [
                        x if (self.__key_matches(sid, x.get('match')) and (set(x.get('engine')).intersection(engines)))
                        else None
                        for x in engine_actions
                    ] or [None]
                )
            except TypeError as e:
                raise SpilException('[Broker.get_actions] Something when wrong during retrieval of action for sid "{}" for engine "{}". '
                                    'Please check the "engine_actions" config file.'.format(sid, engine))
        else:
            found = filter(None, (x if self.__key_matches(sid, x.get('match')) else None for x in engine_actions))

        found = list(found)

        # Then looking up global actions (for all engines)
        found.extend(list(filter(None, (x if self.__key_matches(sid, x.get('match')) else None for x in global_actions))))

        # finally adding universal actions (all sids, all engines)
        found.extend(universal_actions)

        return found

    def get_jobs(self, sid, action):
        matching_actions = filter(None, (x if x.get('action') == action else None for x in job_config))
        matches = filter(None, (x if (self.__key_matches(sid, x.get('match')) or ('all' in x.get('match'))) else None for x in matching_actions))
        return list(matches)

    def get_job(self, sid, name):
        jobs = self.get_jobs(sid, name)
        if not jobs:
            logging.error("Cannot find a job.")  # TODO: change for error popup window
            return None
        return jobs[0]

    def run_job(self, job, sid):
        # Data check
        if "import" not in job:
            logging.error("Cannot execute '{}' job.".format(job))
            return

        # Import the module from the job
        module = importlib.import_module(job.get("import"))  # TODO: replace hard coding
        # importlib.reload(module)  # FIXME: why "AttributeError: 'module' object has no attribute 'reload'"
        reload(module)  # TODO: we can remove this

        # Get the function of the job
        func = getattr(module, job.get("name"))  # TODO: replace hard coding
        if not func:
            logging.warning('Function "{0}" does not exist'.format(func))

        # Execute function
        args = []
        if "batch" in job:
            args = [job.get("batch").get("command")]
        func(sid, *args)

    def run_action(self, name, sid):
        job = self.get_job(sid, name)
        if not job:
            return
        self.run_job(job, sid)

    def __key_matches(self, sid, search_sids):
        """
        Returns True as soon as the Sid matches a search from the given search_sids list.
        False otherwise.
        """
        sid = str(sid)
        fs = LS([sid])
        for search in search_sids:
            #print('Matching {} // {} ?'.format(sid, search))
            if fs.get_one(search, as_sid=False) == sid:
                #print('--------------------> match')
                return True
        return False


if __name__ == '__main__':

    import random
    from spil.util.log import setLevel, WARN
    import example_sids

    setLevel(WARN)

    selection = random.sample(example_sids.sids, 200)
    #selection = example_sids.sids[:100]
    b = Broker()
    # selection = ['CBM/S/SQ0001/SH0240/ANI/V050/WIP/mov']
    for sid in selection:

        action = 'open'
        jobs = b.get_jobs(sid, action)
        for job in jobs:
            print('Job : {} -> {} '.format(sid, job.get('name')))
        # print('')

        action = 'explore'
        jobs = b.get_jobs(sid, action)
        for job in jobs:
            print('Job : {} -> {} '.format(sid, job.get('name')))


    if False:

        actions = b.get_actions(sid)
        print('{} -> {}'.format(sid, [m.get('name') for m in actions]))

        actions = b.get_actions(sid, 'maya')
        print('{} -> {} (maya only)'.format(sid, [m.get('name') for m in actions]))

        for a in actions:
            jobs = b.get_jobs(sid, actions)
            # print('            Job : {} -> {} '.format(sid, [m.get('name') for m in jobs]))

        print('')



# sid = 'raj/a/char/juliet/low/design/v002/w/mp4'
#    sid = Sid(sid)