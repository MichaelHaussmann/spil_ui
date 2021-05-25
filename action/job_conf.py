
job_config = [
    {
        'action': 'open',
        'name': 'open_maya_scene',
        'match': ['*/*/**/maya'],
        'hooks': {},  # TBD
        'import': 'pipe_maya.libs.files',
        'run': 'open_maya_scene',
        'requires': ['pipe_maya'],
        'engine': ['maya'],
        # 'modes' : ['embedded']#
    },
    {
        'action': 'open',
        'name': 'open_hou_scene',
        'match': ['*/*/**/hou'],
        'hooks': {},  # TBD
        'import': 'hou_engine.HoudiniEngine',
        'run': 'HoudiniEngine.open',
        'requires': ['pipe_houdini'],
        'engine': ['hou']  #
    },
    {
        'action': 'explore',
        'name': 'explore',
        'description': 'Opens the file explorer',
        'match': ['all'],
        'import': 'pipe_action.libs.files',
        'run': 'explore',
        'requires': ['pipe_action'],
        'engine': ['all']  #
    },
    {
        'action': 'play',
        'name': 'play_movie',
        'description': 'Launches a movie player',
        'match': ['*/*/**/movie'],
        'import': 'pipe_action.libs.files',
        'run': 'play_movie',
        'requires': ['pipe_action'],
        'engine': ['all']
    },
    {
        'action': 'build',
        'name': 'build_mod',
        'description': 'Build the modeling scene of the specified asset.',
        'match': ['*/A/*/*/MOD'],
        'import': 'pipe_maya.tools.build.build_mod',
        'run': 'run',
        'requires': ['pipe_maya'],
        'engine': ['maya']
    },
    {
        'action': 'build',
        'name': 'build_rig',
        'description': 'Build the rigging scene of the specified asset.',
        'match': ['*/A/*/*/RIG'],
        'import': 'pipe_maya.tools.build.ui.build_rig_ui',
        'run': 'run',
        'requires': ['pipe_maya'],
        'engine': ['maya']
    },
    {
        'action': 'create',
        'name': 'create_project',
        'match': ['*'],
        'import': 'pipe_action.tools.project',
        'run': 'show_create_project_ui',
        'requires': ['pipe_action'],
        'engine': ['all']
    },
    {
        'action': 'create',
        'name': 'create_asset',
        'match': ['*/A/*'],
        'import': 'pipe_action.tools.asset.ui.create_asset_ui',
        'run': 'CreateAssetUI',
        'requires': ['pipe_action'],
        'engine': ['all']
    },
    {
        'action': 'create',
        'name': 'create_shot',
        'match': ['*/S/*'],
        'import': 'pipe_action.tools.shot.ui.create_shot_ui',
        'run': 'CreateShotUI',
        'requires': ['pipe_action'],
        'engine': ['all']
    },
    {
        'action': 'create',
        'name': 'create_sequence',
        'match': ['*/S'],
        'import': 'pipe_action.tools.sequence.ui.create_sequence_ui',
        'run': 'CreateSequenceUI',
        'requires': ['pipe_action'],
        'engine': ['all']
    },

]

drafts = [
    {
        'action': 'publish',
        'name': 'publish_design_ma',
        'match': ['*/a/*/*/*/design/*/w/maya'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['pipe_maya'],
        'engine': ['maya']  #
    },
    {
        'action': 'create',
        'name': 'create_project',
        'match': ['*'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'save_next_version',
        'name': 'save_next_version',
        'match': ['*/*/**/maya'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'build',
        'name': 'build_char_file',
        'match': ['*/a/char/**/maya'],
    },
    {
        'action': 'build',
        'name': 'build_char_task_maya',
        'match': ['*/a/char/*/*/?/**/maya'],  # by the nature of this mapping, this cannot work.
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'build',
        'name': 'build_task',
        'match': ['*/a/char/*/*'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'build',
        'name': 'build_juliet_char_file',
        'match': ['*/a/char/juliet/**/maya'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'build',
        'name': 'build_setup+houdini',
        'match': ['*/a/**/setup/*/*/hou'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'build',
        'name': 'build_something',
        'match': ['*/a,s/**/setup,animation/*/w/hou'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
    {
        'action': 'publish',
        'name': 'publish_design_ma',
        'match': ['*/a/*/*/*/design/*/w/maya'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['pipe_maya']
    },
    {
        'action': 'edit',
        'name': 'edit',
        'match': ['*/*/**'],
        'hooks': {},  # TBD
        'script': 'maya_util.publishes.publish_mod_ma',
        'requires': ['']
    },
]
