import bpy
from bpy.types import Operator
from .menus import CustomMenu
from ..tools.git_command import (git_init,
                               git_commit, set_global_params,
                               git_select_version, git_status)
from ..tools.utilidades import save_mainfile


class InitOperator(Operator):
    
    bl_idname = 'valleapp.init_git_repo'
    bl_label = 'Init repo'
         
    def execute(self, context):
        mainpath = bpy.path.abspath('//')
        
        if mainpath != '':
            success = git_init(mainpath)
            if not success:
                self.report({'ERROR'}, "Error al inicializar el repositorio Git.")
       
        return {'FINISHED'}
    

    
class CommitVersionOperator(Operator):
    
    bl_idname = 'valleapp.commit_version'
    bl_label = 'Commit'
         
    def execute(self, context):
        mainpath = bpy.path.abspath('//')
        commit_message = context.scene.commit_message
        if mainpath != '' and commit_message != "":
            context.scene.commit_message = ""
            success = git_commit(commit_message, mainpath)
            if not success:
                self.report({'ERROR'}, "Error al realizar el commit.")
            
        return {'FINISHED'}
    
class SetGitUserOperator(Operator):
    bl_idname = 'valleapp.set_git_user'
    bl_label = 'Modify Git User'
    
    def execute(self, context):
        mainpath = bpy.path.abspath('//')

        if mainpath != '':
            success_name = set_global_params("name", context.scene.user_name)
            success_email = set_global_params("email", context.scene.user_mail)
            
            if not (success_name and success_email):
                self.report({'ERROR'}, "Error al configurar usuario de Git.")
                return {'CANCELLED'}
        
        return {'FINISHED'}


   
class SaveOperator(Operator):
    bl_idname = 'valleapp.save_main_file'
    bl_label = "Save file"
    
    def execute(self, context):
        success = save_mainfile()
        if not success:
            self.report({'ERROR'}, "Error al guardar el archivo principal.")
        
        return {'FINISHED'}
    
class SwitchGitVersionOperator(Operator):
    bl_idname = 'valleapp.switch_git_version'
    bl_label = 'Switch Version'

    commit: bpy.props.StringProperty()
    op: bpy.props.StringProperty()
    
    def execute(self, context):
        cwd = bpy.path.abspath('//')
        current_head = context.scene.commits.get_head()
        is_dirty = bpy.data.is_dirty

        if self.commit == current_head["commit"]:
            return {'FINISHED'}
        
        
        status, success = git_status(cwd)
        
        if not success:
            self.report({'ERROR'}, "Error al obtener el estado de Git.")
            return {'CANCELLED'}
        
        
        if is_dirty or status:
            if self.op in ["save", "cancel", "des"]:
                if self.op == "save":
                    commit_message = context.scene.commit_message
                    if commit_message != "":
                        context.scene.commit_message = ""
                        success = git_commit(commit_message, cwd)
                        if not success:
                            self.report({'ERROR'}, "Error al realizar el commit.")
                            return {'CANCELLED'}
                        else:
                            git_select_version(self.commit, cwd)
                    else:
                        context.scene.commit_message = current_head["subject"] + " *"
                          
                elif self.op == "cancel":
                    return {'FINISHED'}
                else:
                    git_select_version(self.commit, cwd)
            else:
                bpy.ops.wm.call_menu(name=CustomMenu.bl_idname)
        else:
            git_select_version(self.commit, cwd)
            
        return {'FINISHED'}

    
class RefreshCommitsOperator(Operator):

    bl_idname = 'valleapp.refresh_commits'
    bl_label = 'Refresh Commits'
        
    def execute(self, context):
        context.scene.commits.clear()
        return {'FINISHED'}