import bpy
import traceback

def save_mainfile():
    try:
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        return True
    except Exception as e:
        print('Error al guardar el archivo principal: ', e)
        traceback.print_exc()
        return False
    

def clean_signos(value):
    value = value.replace("b'", "")
    value = value.replace("'","")
    value = value.replace("M", "")
    value = value.replace("\t","")
    value = value.replace("\n", "")
    return value