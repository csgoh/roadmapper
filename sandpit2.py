from print_dict import pd
data = {
     "groups": {
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "group_items": {
                0: {
                    "x": 0,
                    "y": 0,
                    "width": 0,
                    "height": 0,
                    "tasks": {
                        1: {"x": 100, "y": 110, "width": 120, "height": 130},
                        2: {"x": 200, "y": 210, "width": 220, "height": 230},
                    },
                },
                2: {
                    "x": 0,
                    "y": 0,
                    "width": 0,
                    "height": 0,
                    "tasks": {
                        3: {"x": 300, "y": 310, "width": 320, "height": 240},
                        4: {"x": 400, "y": 410, "width": 420, "height": 250},
                    },
                },
            }
     }
}

#print(data.get("groups",{}).get("group_items",{}).get(0, {}).get("tasks",{}).get(1,{}).get("x",0))
#data["groups"]["group_items"][0]["tasks"][1]["x"] = 999
#data["groups"]["group_items"][0]["tasks"][3] = {"x": 250, "y": 250, "width": 250, "height": 250}
#print(data.get("groups",{}).get("group_items",{}).get(0, {}).get("tasks",{}).get(1,{}).get("x",0))
#print(data.get("groups",{}).get("group_items",{}).get(0, {}).get("tasks",{}))

data["groups"]["group_items"][3] = {"x": 0, "y": 0, "width": 0, "height": 0, "tasks": {}}
                    
print(pd(data.get("groups",{}).get("group_items",{})))