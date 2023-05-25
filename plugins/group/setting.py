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
})
ui_factory(objects)