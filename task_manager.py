# task_manager.py
import itertools

class TaskManager:
    def __init__(self):
        # Список для хранения задач
        self.tasks = []
        # Генератор уникальных ID
        self._id_counter = itertools.count(1)

    def get_all_tasks(self):
        """Возвращает все задачи."""
        return self.tasks

    def get_task_by_id(self, task_id):
        """Возвращает задачу по ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def add_task(self, title, priority):
        """Добавляет новую задачу."""
        new_task = {
            'id': next(self._id_counter),
            'title': title,
            'priority': priority
        }
        self.tasks.append(new_task)
        return new_task

    def update_task(self, task_id, updated_task_data):
        """Обновляет задачу по ID."""
        task = self.get_task_by_id(task_id)
        if task:
            task.update(updated_task_data)
            return task
        return None

    def delete_task(self, task_id):
        """Удаляет задачу по ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
