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
    "list":[
        {"id":1, "name":"User1", "age":10},
        {"id":2, "name":"User2", "age":20},
        {"id":3, "name":"User3", "age":15},
    ]
})
ui_factory(objects)