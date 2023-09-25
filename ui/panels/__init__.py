import bpy
from bpy.types import Panel
import os
from tools.git_command import get_global_params, load_commits

class InitTrackPanel(Panel):
    bl_label = 'Initialize Tracking'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ValleTrack'

    @classmethod
    def poll(cls, context):
        mainpath = bpy.path.abspath('//')
        git_dir = os.path.join(mainpath, ".git")
        return not mainpath or not os.path.exists(git_dir)

    def draw(self, context):
        layout = self.layout
        mainpath = bpy.path.abspath('//')

        if not mainpath:
            layout.operator('valleapp.save_main_file', text="Guardar Archivo")
        else:
            git_dir = os.path.join(mainpath, ".git")
            if not os.path.exists(git_dir):
                layout.operator('valleapp.init_git_repo', text="Inicializar Repositorio")


class VersionPanel(Panel):
    bl_label = 'Versiones'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ValleTrack'

    @classmethod
    def poll(cls, context):
        mainpath = bpy.path.abspath('//')
        git_dir = os.path.join(mainpath, ".git")
        name, name_status = get_global_params("name")
        email, email_status = get_global_params("email")
        return os.path.exists(git_dir) and name_status and email_status


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        commits = bpy.context.scene.commits
        if not commits.has_commits():
            mainpath = bpy.path.abspath('//')
            success = load_commits(mainpath)
            if not success:
                self.report({'ERROR'}, "Error al cargar commits.")


    def draw_new_version_section(self, context):
        col = self.layout.column()
        col.label(text="Datos de la versión")
        col.label(text="Descripción corta:")
        col.prop(context.scene, "name_version", text="")
        col.operator("valleapp.add_version", text="Nueva versión")

    def draw_version_list(self, context, commits):
        col = self.layout.column()
        col.label(text="Ramas")
        row = col.row()
        row.prop(context.scene, "branch", text="")
        row.operator("valleapp.refresh", text="Refrescar")
        col.label(text="Lista de versiones")

        for c in commits.get_rama():
            icon = 'PROP_ON' if "HEAD" in c["refs"] else 'PROP_OFF'
            ops = col.operator("valleapp.set_version", text=c["subject"], icon=icon)
            ops.commit = c["commit"]
            ops.op = ""

    def draw(self, context):
        self.draw_new_version_section(context)
        commits = bpy.context.scene.commits
        if commits.has_commits():
            self.draw_version_list(context, commits)


class UserPanel(Panel):
    
    bl_label = 'User Data'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ValleTrack'
    bl_options = {'DEFAULT_CLOSED'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name, success_name = get_global_params("name")
        email, success_email = get_global_params("email")
        
        if success_name and bpy.data.scenes["Scene"].user_name == "":
            bpy.data.scenes["Scene"].user_name = name
            
        if success_email and bpy.data.scenes["Scene"].user_mail == "":
            bpy.data.scenes["Scene"].user_mail = email

    def draw(self, context):
        col = self.layout.column()
        col.prop(context.scene, "user_name", text="User")
        col.prop(context.scene, "user_mail", text="Email")
        col.operator('valleapp.modify_user_data', text='Modify')
