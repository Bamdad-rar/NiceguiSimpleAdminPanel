from sections.setting import ui_factory, model_factory

objects = model_factory({
    "model_name": "Group",

    "items":{
        "id":{
            "type":"primary_key"
        },
        "name":{
            "type":"string"
        },
        "role":{
            "type":"enum",
            "values":["R1","R2","R3"]
        }
    },
    "list":[
        {"id":1, "name": "g1", "role":"R2"},
        {"id":2, "name": "g2", "role":"R3"},
        {"id":3, "name": "g3", "role":"R1"},
    ]
})
ui_factory(objects)