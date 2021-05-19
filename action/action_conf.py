

engine_actions = [  # engine specific and sid specific
    {
        'name': 'open',
        'label': 'Open',
        'description': 'Opens the scene',
        'match': ['*/A/**', '*/S/**'],
        'engine': ['maya', 'hou', 'nk']
    },
    {
        'name': 'save_next_version_ma',
        'label': 'Save Next Version',
        'description': 'Saves the open scene as the next version',
        'match': ['*/*/**/maya'],
        'engine': ['maya']  #
    },
    {
        'name': 'save_next_version',
        'label': 'Save Next Version',
        'description': 'Saves the open scene as the next version',
        'match': ['*/*/**/hou'],
        'engine': ['hou']
    },
    {
        'name': 'build',
        'label': 'Build',
        'description': 'Build a new scene for this task/variant',
        'match': ['*/A/*/*/*', '*/S/*/*/*/*'],
        'engine': ['maya', 'hou', 'nk']
    },
]

global_actions = [  # All Engines, sid specific

    {
        'name': 'play',
        'label': 'Play',
        'description': 'Launches a movie player',
        'match': ['*/*/**/movie'],
    },
    {
        'name': 'create',
        'label': 'Create',
        'description': 'Creates a new Entity (Project, Asset or Shot)',
        'match': ['*', '*/A,S/*'],
    },
    {
        'name': 'edit',
        'label': 'Edit',
        'description': 'Edit the Entity',
        'match': ['*/A,S/*', '*/A,S/*/*', '*/A,S/*/*/*'],
    },

]

universal_actions = [  # All Engines, all sids
    {
        'name': 'explore',
        'label': 'Explore',
        'description': 'Opens the file explorer'
    },
]


"""{
        'name': 'publish',
        'label': 'Publish',
        'description': 'Publish the scene',
        'match': ['*/A/*/*/*/*', '*/S/*/*/*/*'],
        'engine': ['maya', 'hou', 'nk']
    }"""
