from bpy.types import Menu

class CustomMenu(Menu):
    bl_label = "Proyecto modificado!!"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("valleapp.switch_git_version", text="Crear Nueva Versión").op = "save"
        layout.operator("valleapp.switch_git_version", text="Descartar cambios").op = "des"
        layout.operator("valleapp.switch_git_version", text="Cancelar").op = "cancel"
