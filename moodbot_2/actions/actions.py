from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database

# Create an instance of the Database class
db = Database()

class RetrieveEmployeeList(Action):
    def name(self) -> Text:
        return "action_retrieve_employee_list"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = "SELECT user_name FROM employee_master"
        result = db.execute_query(query)

        if result:
            employee_list = [row[0] for row in result]
            employee_list_text = ", ".join(employee_list)
            dispatcher.utter_message(text=f"The full employee list is: {employee_list_text}")
        else:
            dispatcher.utter_message(text="Employee list not found.")

        return []

def fetch_employee_details(name, id, birthdate, phone_number):
    cursor = db.connection.cursor()
    query = "SELECT * FROM employee_master WHERE user_name = %s OR id = %s OR birth_date = %s OR phone = %s"
    values = (name, id, birthdate, phone_number)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    return result


class RetrieveEmployeeDetailsAction(Action):
    def name(self) -> Text:
        return "action_retrieve_employee_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        id = tracker.get_slot("id")
        birthdate = tracker.get_slot("birthdate")
        phone_number = tracker.get_slot("phone_number")

        query = "SELECT * FROM employee_master WHERE user_name = %s OR id = %s OR birth_date = %s OR phone = %s"
        values = (name, id, birthdate, phone_number)
        result = db.execute_query(query, values)

        if len(result) > 0:
            employee_name = result[0][0]
            employee_id = result[0][1]
            response = f"Employee details found:\nName: {employee_name}\nID: {employee_id}"
        else:
            response = "No employee details found."

        dispatcher.utter_message(text=response)

        return []
