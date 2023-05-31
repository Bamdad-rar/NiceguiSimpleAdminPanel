from sections.setting import ui_factory, model_factory


objects=model_factory({
    "model_name":"User",
    "items":{
        "id":{
            "type":"primary_key"
        },
        "name":{
            "type":"string"
        },
        "age":{
            "type":"number"
        }
    },
})
ui_factory(objects)