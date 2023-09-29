import bpy
import json


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
        
        
    def load_commits(self, commits):
       items = json.loads("{"+commits[:-1]+"}")
       ramas = []
       parents = []
       
       for k in items.keys():
           item = items[k]
           
           if "HEAD" in item['refs']:
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
    
                