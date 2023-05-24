import asyncio
from models.admin import User
from models.ecg import ExecutionData, ExecutionStatus, Lead
from celery import Celery
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import logging

celery_app = Celery('worker', broker='amqp://guest:guest@rabbitmq:5672//')

mongodb_url = 'mongodb://mongodb:27017/lms'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configura el formateador de los registros
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Configura un controlador de salida para los registros
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Agrega el controlador al logger
logger.addHandler(stream_handler)


@celery_app.task
def process_execution(id):
    logger.info("Received task for ID: " + id)
    loop = asyncio.get_event_loop()
    client = AsyncIOMotorClient(mongodb_url)
    init_task = loop.create_task(
        init_beanie(
            database=client.get_default_database(),
            document_models=[User, ExecutionData, ExecutionStatus, Lead]
            )
        )

    execution_data_promise = ExecutionData.get(id)
    execution_status_promise = ExecutionStatus.get(id)

    loop.run_until_complete(init_task)

    execution_status = loop.run_until_complete(execution_status_promise)
    execution_status.status = "IN PROGRESS"
    loop.run_until_complete(execution_status.save())

    execution_data = loop.run_until_complete(execution_data_promise)

    if execution_data:
        count = count_zero_passes(execution_data)
        execution_status.result = {
            "count_zero_passes": count
        }
        execution_status.status = "FINISHED"
        loop.run_until_complete(execution_status.save())

    logger.info(execution_status)
    client.close()


def count_zero_passes(execution_data: ExecutionData):
    count = 0
    for lead in execution_data.leads:
        signal = lead.signal
        if len(signal) > 0:
            last_value = signal[0]
            for value in signal[1:]:
                if value < 0:
                    if last_value > 0:
                        count += 1
                if value > 0:
                    if last_value < 0:
                        count += 1
                last_value = value if value!=0 else last_value
    return count
