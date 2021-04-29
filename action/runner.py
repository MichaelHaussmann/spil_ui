


class Runner(object):
    pass

    def run_tree(self):  # submit a job tree
        pass

    def run(self, sid, action, mode='batch', context={}):
        pass

    def batch(self, sid, job):

        requires = job.get('requires')

        from rez.resolved_context import ResolvedContext

        resolver = ResolvedContext(requires, add_implicit_packages=False)

        p = resolver.execute_shell(command=['maya', file], stdout=subprocess.PIPE)
        out, err = p.communicate()
        print(out)
