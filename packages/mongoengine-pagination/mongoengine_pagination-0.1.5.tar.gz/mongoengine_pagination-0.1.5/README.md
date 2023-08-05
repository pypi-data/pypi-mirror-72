============how to use?===========

----example

class User(DocumentPro):   
    user_id = IntField() 
    
    name = StringField()
    
page_index = 2

page_size = 20

user_list = User.objects().paginate(page_index, page_size)

result_list = result.items

total_items = result.total 

total_page = result.pages,