import bpy
from .ui.propiedades import PROPS, CommitData
from .ui.menus import CustomMenu
from .ui.panels import (VALLETRACK_PT_InitTrackPanel, 
                        VALLETRACK_PT_VersionPanel, VALLETRACK_PT_UserPanel)
from .ui.operadores import (SaveOperator, 
                           InitOperator,  SetGitUserOperator,
                           CommitVersionOperator, 
                           SwitchGitVersionOperator,
                           RefreshCommitsOperator)      

bl_info = {
    "name": "ValleTrack",
    "author": "valle.mrv",
    "version": (1, 5, 5),
    "blender": (3, 0, 0),
    "location": "VIEW3D",
    "description": "Control simple de versiones git lsf",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}




CLASSES = [
    SaveOperator,
    InitOperator,
    SetGitUserOperator,
    CommitVersionOperator,
    SwitchGitVersionOperator,
    RefreshCommitsOperator,
    CommitData,
    CustomMenu,
    VALLETRACK_PT_InitTrackPanel,
    VALLETRACK_PT_VersionPanel,
    VALLETRACK_PT_UserPanel,
]
      
def register():
    for k in CLASSES:
        bpy.utils.register_class(k)
        
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

def unregister():
    
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    for k in CLASSES:
        bpy.utils.unregister_class(k)
        
        
if __name__ == '__main__':
    register()
