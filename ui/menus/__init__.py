from bpy.types import Menu

class CustomMenu(Menu):
    bl_label = "Atención a cambios!!!"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("valleapp.set_version", text="Nueva versión").op = "save"
        layout.operator("valleapp.set_version", text="Descartar cambios").op = "des"
        layout.operator("valleapp.set_version", text="Cancelar").op = "cancel"
