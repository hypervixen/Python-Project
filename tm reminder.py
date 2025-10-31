from datetime import date, datetime


class Task:
    def __init__(self, title, due_date, priority):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.completed_status = False

    def mark_done(self):
        self.completed_status = True
        print(f"The task {self.title} is marked as completed")

    def is_overdue(self):
        if self.due_date < date.today():
            print(f"The task is overdue: {self.title}")
            return True
        return False

    def __str__(self):
        return f"{self.title} | {self.due_date} | Priority:{self.priority} | Status:{self.completed_status}"


class TaskManager:
    """
         Task manager with an empty task list.
            """
    def __init__(self):
        self.tasks = []

    def get_priority_input(self):
        """
              Enter a valid priority.
              Keeps asking until input is valid.
              """
        while True:
            priority = input("Enter priority (Low, Medium, High): ").lower()
            if priority in ['low', 'medium', 'high']:
                break
            else:
                print("Invalid priority.")
        return priority

    def get_date_input(self):
        """
             Enter a valid date in yyyy-mm-dd format.
             Returns a date if valid.
             """
        date_input = input("Enter the date (yyyy-mm-dd): ")

        if not date_input:
            print("Date cannot be empty.")
            return None

        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use yyyy-mm-dd.")
            return None

    def add_task(self, title, due_date, priority):
        """
             Adds a new task to the task list.
             """
        task_add = Task(title, due_date, priority)
        self.tasks.append(task_add)

    def view_tasks(self):
        """
               Displays all tasks with index numbers.
               """
        if not self.tasks:
            print("No tasks available.")
            return
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def mark_done(self, index):
        """
               Marks a task by index as completed.
               """
        if 0 < index <= len(self.tasks):
            self.tasks[index - 1].mark_done()
        else:
            print("Invalid task number.")

    def delete_task(self, index):
        """
             Deletes a task by index from list.
             """
        if 0 < index <= len(self.tasks):
            removed = self.tasks.pop(index - 1)
            print(f"Deleted task: {removed.title}")
        else:
            print("Invalid task number.")

    def search_tasks(self):
        """
         Searches tasks by a keyword in the title.
               """
        print("\nSearch Tasks")
        keyword = input("Enter keyword: ")
        if not keyword:
            print("Keyword cannot be empty.")
            return []
        task_match = [task for task in self.tasks if keyword.lower() in task.title.lower()]
        if not task_match:
            print(f"\nNo tasks found using the keyword: {keyword}.")
        else:
            for i, task in enumerate(task_match, 1):
                print(f"{i}. {task}")
        return task_match

    def get_overdue_tasks(self):
        """
            Returns a list of overdue and incomplete tasks.
              """
        today_date = date.today()
        return [task for task in self.tasks if (task.due_date < today_date and not task.completed_status)]

    def get_tasks_by_date(self):
        """
             Allows user to search tasks based on a specific date.
             Tasks are divided into:
             - Overdue & Present & Upcoming
             """
        print("\nSearch tasks by date")
        date_input = input("Enter the date (yyyy-mm-dd): ")

        if not date_input:
            print("Date cannot be empty.")
            return []

        try:
            date_selected = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use yyyy-mm-dd.")
            return []

        overdue_tasks = [task for task in self.tasks if (task.due_date < date_selected and not task.completed_status)]
        present_tasks = [task for task in self.tasks if (task.due_date == date_selected)]
        upcoming_tasks = [task for task in self.tasks if (task.due_date > date_selected and not task.completed_status)]

        if overdue_tasks:
            print("\nOverdue Tasks:")
            for i, task in enumerate(overdue_tasks):
                print(f"{i + 1}. {task.title}")
        else:
            print(f"\nNo overdue tasks found as of {date_selected}.")

        if present_tasks:
            print(f"\nTasks as per {date_selected} :")
            for i, task in enumerate(present_tasks):
                print(f"{i + 1}. {task.title}")
        else:
            print(f"\nNo tasks found on {date_selected}.")

        if upcoming_tasks:
            print("\nUpcoming Tasks:")
            for i, task in enumerate(upcoming_tasks):
                print(f"{i + 1}. {task.title}")
        else:
            print(f"\nNo upcoming tasks found after {date_selected}.")

        return overdue_tasks, present_tasks, upcoming_tasks

    def filter_by_priority(self):
        """
           Filters and displays tasks that match the user's selected priority.
           """
        desired_priority = input("Enter priority to filter by (Low, Medium, High): ").lower()
        if desired_priority not in ['low', 'medium', 'high']:
            print("Invalid priority.")
            return

        def matches_priority(task):
            return task.priority == desired_priority

        filtered_tasks = []
        for task in self.tasks:
            if matches_priority(task):
                filtered_tasks.append(task)

        if not filtered_tasks:
            print(f"No tasks with priority '{desired_priority}'.")
        else:
            print(f"\nTasks with priority '{desired_priority}':")
            for i, task in enumerate(filtered_tasks, 1):
                print(f"{i}. {task}")


    def sort_by_due_date(self):
        """
            Sorts tasks in ascending order of due dates.
            """
        def get_due_date(task):
            return task.due_date

        sorted_tasks = sorted(self.tasks, key=get_due_date)

        print("\nTasks Sorted by Due Date:")
        for i, task in enumerate(sorted_tasks, 1):
            print(f"{i}. {task}")


    def sort_by_priority(self):
        """
               Sorts tasks in order of priority: high > medium > low.
               """
        def get_priority_value(task):
            priority_order = {'low': 1, 'medium': 2, 'high': 3}
            return priority_order.get(task.priority, 0)

        sorted_tasks = sorted(self.tasks, key=get_priority_value, reverse=True)

        print("\nTasks Sorted by Priority:")
        for i, task in enumerate(sorted_tasks, 1):
            print(f"{i}. {task}")


manager = TaskManager()


def overdue_alert():
    """
       Displays a message if there are overdue tasks at startup.
       """

    overdue = manager.get_overdue_tasks()
    count_of_overdue = len(overdue)

    if count_of_overdue != 0:
        print(f"You have {count_of_overdue} overdue task(s)!")
    else:
        print("You have 0 overdue task!")


def menu():
    overdue_alert()

    """
    Main menu loop for the Task Manager CLI.
    User selects from 9 options to manage tasks.
    """

    while True:
        print("\nTASK MANAGER MENU")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Filter by Priority")
        print("7. Sort by Due Date")
        print("8. Sort by Priority")
        print("9. Exit")

        user_input = input("Enter your choice: ")

        if user_input == "1":
            title = input("Enter task title: ")
            due_date = manager.get_date_input()
            if not due_date:
                continue
            priority = manager.get_priority_input()
            manager.add_task(title, due_date, priority)
            print("Task added.")

        elif user_input == "2":
            manager.view_tasks()

        elif user_input == "3":
            manager.view_tasks()
            try:
                index = int(input("Choose task index: "))
                manager.mark_done(index)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif user_input == "4":
            manager.view_tasks()
            try:
                index = int(input("Choose task index: "))
                manager.delete_task(index)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif user_input == "5":
            manager.search_tasks()

        elif user_input == "6":
            manager.filter_by_priority()

        elif user_input == "7":
            manager.sort_by_due_date()

        elif user_input == "8":
            manager.sort_by_priority()

        elif user_input == "9":
            print("Good Bye!")
            break

        else:
            print("Invalid number. Please try again!")


menu()
