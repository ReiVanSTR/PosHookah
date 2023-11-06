from aiogram.utils.callback_data import CallbackData

new_bill_callback = CallbackData("SelectMenu", "type")

table_callback = CallbackData("Table", "action", "name")

person_callback = CallbackData("Person", "action","quantity")

commit_callback = CallbackData("Commit", "action",)




order_callback = CallbackData("Order", "level", "action")

bill_callback = CallbackData("Bill", "action", "current_table")


menu_callback = CallbackData("Menu", "level", "action", "table")

cancel_callback = CallbackData("Cancel", "action", "level") #cancel