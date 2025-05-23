from app.celery_worker import celery
import time
import random

@celery.task(bind=True, name="generate_and_process_numbers")
def generate_and_process_numbers(self, count: int):
    numbers = []
    for _ in range(count):
        num = random.randint(1, 10)
        numbers.append(num)
        self.update_state(state='PROGRESS', meta={'current': _ + 1, 'total': count, "numbers": numbers})
        time.sleep(5)
        print(f"Generated number: {num} after 5s delay")
    return {"count": count, "numbers": numbers}
