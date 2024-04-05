import logging
import time


class ProgressTracker:
    def __init__(self):
        self.progress = {}

    def start_task(self, agent_name: str, task_name: str):
        if agent_name not in self.progress:
            self.progress[agent_name] = {}
        self.progress[agent_name][task_name] = {
            "start_time": time.time(),
            "status": "In Progress"
        }
        logging.info(f"{agent_name} started task: {task_name}")

    def complete_task(self, agent_name: str, task_name: str):
        if agent_name in self.progress and task_name in self.progress[agent_name]:
            self.progress[agent_name][task_name]["end_time"] = time.time()
            self.progress[agent_name][task_name]["status"] = "Completed"
            logging.info(f"{agent_name} completed task: {task_name}")

    def generate_report(self):
        report = "Progress Report:\n"
        for agent_name, tasks in self.progress.items():
            report += f"\n{agent_name}:\n"
            for task_name, task_details in tasks.items():
                start_time = task_details["start_time"]
                end_time = task_details.get("end_time", time.time())
                duration = end_time - start_time
                status = task_details["status"]
                report += f"  - {task_name}: {status} (Duration: {duration:.2f} seconds)\n"
        logging.info(report)
