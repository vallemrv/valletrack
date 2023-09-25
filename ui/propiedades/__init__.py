import bpy
from .commits import CommitData

PROPS = [
    ('user_name', bpy.props.StringProperty()),
    ('user_mail', bpy.props.StringProperty()),
    ('commit_message',  bpy.props.StringProperty()),
    ('des_version',  bpy.props.StringProperty()),
    ('commits', bpy.props.PointerProperty(type=CommitData)),
    ("branch", bpy.props.EnumProperty(items=CommitData.ramas)),
    ("to_commits", bpy.props.StringProperty()),
]   
