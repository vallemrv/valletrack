bl_info = {
    "name": "ValleTrack",
    "author": "valle.mrv",
    "version": (1, 5, 1),
    "blender": (3, 3, 1),
    "location": "VIEW3D",
    "description": "Control simple de versiones git lsf",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

import bpy
import json
import os
import subprocess
from bpy.types import Operator



def clean_signos(value):
    value = value.replace("b'", "")
    value = value.replace("'","")
    value = value.replace("M", "")
    value = value.replace("\t","")
    value = value.replace("\n", "")
    return value

def get_global_params(p):
    lst = subprocess.check_output(['git','config', '--global',  '--get',  "user."+p]).decode().strip()
    return lst

def set_global_params(p, v):
    subprocess.check_output(['git','config', '--global',  "user."+p, v])
    
    
def git_add(cwd):
    subprocess.check_output(['git','add', '.'], cwd=cwd)
    
def git_init(cwd):
    subprocess.check_output(['git','init'], cwd=cwd)
    
    
def git_commit(v, cwd):
    if bpy.context.scene.commits.has_ramas():
        bpy.context.scene.branch = "0"
    bpy.context.scene.commits.clear()        
    bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
    git_add(cwd)
    subprocess.check_output(['git','commit', '-m',  v], cwd=cwd)
    
            
def load_commits(cwd):
    count = subprocess.check_output(['git', 'rev-list', '--all', '--count'], cwd=cwd).decode().strip()
    if int(count) > 0:
        cmd = ['git', 'log', '--pretty=format:"%h": {"commit": "%h", "parent": "%p", "refs": "%D", "subject": "%s"},', '--reflog']
        commits = subprocess.check_output(cmd, cwd=cwd).decode().strip()
        bpy.context.scene.commits.add_commits(commits)


def git_select_version(id, cwd):
    subprocess.check_output(['git', 'reset', '--hard', id], cwd=cwd)
    bpy.ops.wm.revert_mainfile()
    bpy.context.scene.commits.clear()

class CommitData(bpy.types.PropertyGroup):
    
    __ramas = []
    __head = ""
    
    def crear_rama(self, item,  items, rama):
        if item["parent"] == "":
            rama.append(item)
            return rama
        else:
            rama.append(item)
            return self.crear_rama(items[item["parent"]], items, rama)
        
        
         
     
    def add_commits(self, commits):
       items = json.loads("{"+commits[:-1]+"}")
       ramas = []
       parents = []
       
       for k in items.keys():
           item = items[k]
           
           
           if item['refs'] != "":
               CommitData.__head = item
               
           if item["commit"] not in parents:
               ramas.append(self.crear_rama(item, items, []))
             
           parents.append(item["parent"])
               
       CommitData.__ramas = ramas
       
    def has_ramas(self):
        return len(CommitData.__ramas)
    
    def get_rama(self):
        i = (bpy.context.scene.branch)
        if i == "": return []
        i = int(i)
        return CommitData.__ramas[i]
        
    def has_commits(self):
        return len(CommitData.__ramas) > 0
    
    def clear(self):
        CommitData.__ramas = []
        
    def get_head(self):
        return CommitData.__head
    
    @staticmethod   
    def ramas(obj, context):
        if len(CommitData.__ramas) <= 0:
            return []
        items = []
        for i in range(0, len(CommitData.__ramas)):
            items.append((str(i), "Rama "+str(i+1), "Rama "+str(i+1)))
        return items     
                


PROPS = [
    ('user_name', bpy.props.StringProperty()),
    ('user_mail', bpy.props.StringProperty()),
    ('name_version',  bpy.props.StringProperty()),
    ('des_version',  bpy.props.StringProperty()),
    ('commits', bpy.props.PointerProperty(type=CommitData)),
    ("branch", bpy.props.EnumProperty(items=CommitData.ramas)),
    ("to_commits", bpy.props.StringProperty()),
]   


       

class SaveOperator(Operator):
    bl_idname = 'valleapp.save_main_file'
    bl_label = "Save file"
    
    def execute(self, context):
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        
        return {'FINISHED'}

class InitOperator(Operator):
    
    bl_idname = 'valleapp.init_git_repo'
    bl_label = 'Init repo'
         
    def execute(self, context):
        mainpath = bpy.path.abspath('//')
        
        if mainpath != '':
            git_init(mainpath)
       
        return {'FINISHED'}
    
class AddOperator(Operator):
    
    bl_idname = 'valleapp.add_git_repo'
    bl_label = 'Add'
         
    def execute(self, context):
        mainpath = bpy.path.abspath('//')
        
        if mainpath != '':
            git_add(mainpath)
            
       
        return {'FINISHED'}
    
class CHUserOperator(Operator):
    
    bl_idname = 'valleapp.ch_user_operator'
    bl_label = 'Modify'
         
    def execute(self, context):
        set_global_params("name", context.scene.user_name)
        set_global_params("email", context.scene.user_mail)
            
        return {'FINISHED'}


class AddVersion(Operator):
    
    bl_idname = 'valleapp.add_version'
    bl_label = 'Add version'
         
    def execute(self, context):
        mainpath = bpy.path.abspath('//')
        name = context.scene.name_version
        if mainpath != '' and name != "":
            context.scene.name_version = ""
            git_commit(name, mainpath)
            
        return {'FINISHED'}
    
    
    
class OBJECT_OT_set_version(Operator):
    
    bl_idname = 'valleapp.set_version'
    bl_label = 'Set version'
    commit: bpy.props.StringProperty()
    op: bpy.props.StringProperty()
        
    def execute(self, context):
        if self.commit != context.scene.commits.get_head()["commit"]:
            cwd = bpy.path.abspath('//')    
            m = subprocess.check_output(['git', 'status', '-s'], cwd=cwd).decode().strip()
            
            if (bpy.data.is_dirty or m != "") and self.op not in ["save", "cancel", "des"]:
                bpy.ops.wm.call_menu(name=CustomMenu.bl_idname)
            elif self.op == "save":
                cm = context.scene.commits.get_head()
                git_commit(cm["subject"]+ " *", cwd)
                git_select_version(self.commit,  cwd)
            elif self.op == "cancel":
                return {'FINISHED'}
            elif (not bpy.data.is_dirty and  m == "") or self.op == "des":  
                git_select_version(self.commit,  cwd)
            
                
        return {'FINISHED'}
    
    
   
class OBJECT_OT_refresh(Operator):
    
    bl_idname = 'valleapp.refresh'
    bl_label = 'Set version'
        
    def execute(self, context):
        context.scene.commits.clear()
        return {'FINISHED'}

class CustomMenu(bpy.types.Menu):
    bl_label = "Atencion cambios!!!"
    bl_idname = "OBJECT_MT_custom_menu"
    

    def draw(self, context):
        c = context.scene.to_commits
        col = self.layout.column()
        col.operator("valleapp.set_version", text="Nueva version").op = "save"
        col.operator("valleapp.set_version", text="Descartar cambios").op = "des"
        col.operator("valleapp.set_version", text="Cancelar").op = "cancel"
        

        

class OBJECT_PT_init_panel(bpy.types.Panel):    
    bl_label = 'Init track'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ValleTrack'
    
    @classmethod
    def poll(cls, context):
        mainpath = bpy.path.abspath('//')
        git_dir = os.path.join(mainpath, ".git")
        return (mainpath == '') or (not os.path.exists(git_dir))
    
    def draw(self, context):
        col = self.layout.column()
        mainpath = bpy.path.abspath('//')  
        if mainpath == '':
            col.operator('valleapp.save_main_file', text="Save File")
        else:
            git_dir = os.path.join(mainpath, ".git")
            if not os.path.exists(git_dir):
                col.operator('valleapp.init_git_repo', text='Init Repo')
                
                
        
class OBJECT_PT_version_panel(bpy.types.Panel):
    
    bl_label = 'Versions'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ValleTrack'
            
    @classmethod
    def poll(cls, context):
        mainpath = bpy.path.abspath('//')  
        git_dir = os.path.join(mainpath, ".git")
        return  os.path.exists(git_dir) and get_global_params("name") != "" and get_global_params("email") != ""
      
    def __init__(self, *arg, **vargs):
        super(*arg, **vargs)
        commits = bpy.context.scene.commits
        if not commits.has_commits():
            print("cargando commit")
            mainpath = bpy.path.abspath('//')
            load_commits(mainpath)
        
               
    
    def draw_new_version(self, context):
        col = self.layout.column()
        col.label(text="Version data")
        col.label(text="Short description:")
        col.prop(context.scene, "name_version", text="")
        col.operator("valleapp.add_version", text="New version")
    
    def draw(self, context):
        self.draw_new_version(context)
        commits = bpy.context.scene.commits
        if commits.has_commits():
            col = self.layout.column()
            col.label(text="Ramas")
            row = col.row()
            
            row.prop(context.scene, "branch", text="")
            row.operator("valleapp.refresh", text="Refresh")
            col.label(text="Lista de versiones")
            g = context.scene.commits
            for c in g.get_rama():
                icon = 'PROP_ON' if c["refs"] != "" else 'PROP_OFF'
                ops = col.operator("valleapp.set_version", text=c["subject"], icon=icon)
                ops.commit = c["commit"]
                ops.op = ""
               
            
            

class OBJECT_PT_user_panel(bpy.types.Panel):
    
    bl_label = 'User data'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ValleTrack'
    bl_options = {'DEFAULT_CLOSED'}
    
    def __init__(self, *arg, **vargs):
        super(*arg, **vargs)
        name = get_global_params("name")
        mail = get_global_params("email")
        if bpy.data.scenes["Scene"].user_name == "" and name != "":
            bpy.data.scenes["Scene"].user_name = name
        if bpy.data.scenes["Scene"].user_mail == "" and mail != "":
            bpy.data.scenes["Scene"].user_mail = mail
        
    
    def draw(self, context):
        
        col = self.layout.column()
        col.prop(context.scene, "user_name", text="User")
        col.prop(context.scene, "user_mail", text="Email")
        col.operator('valleapp.ch_user_operator', text='Modify')
            
                   
                
            

CLASSES = [
    SaveOperator,
    InitOperator,
    AddOperator,
    CHUserOperator,
    AddVersion,
    CommitData,
    CustomMenu,
    OBJECT_OT_set_version,
    OBJECT_OT_refresh,
    OBJECT_PT_version_panel,
    OBJECT_PT_init_panel,
    OBJECT_PT_user_panel,
    
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
