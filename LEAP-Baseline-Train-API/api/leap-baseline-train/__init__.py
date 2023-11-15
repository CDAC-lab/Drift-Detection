import azure.functions as func
from datetime import datetime
from common_utilities import insert_model_train_process

from queue_handler import send_baseline_train_message

import logging

log = logging.getLogger()
log.setLevel(logging.INFO)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        building_ids = req.params.get('building_ids')
        model_type = req.params.get('model_type')
        start_date = req.params.get('start_date')
        end_date = req.params.get('end_date')

        if building_ids is None or model_type is None or start_date is None or end_date is None:
            return func.HttpResponse(f"Please provide building_ids, model_type, start_date and end_date!",
                                     status_code=400)

        building_ids = [building_id.strip()
                        for building_id in building_ids.split(',')]

        if len(building_ids) == 0:
            return func.HttpResponse(f"Please provide building_ids separated by commas!", status_code=400)

        for building_id in building_ids:
            if datetime.now() > datetime.strptime(end_date, '%Y%m%d'):
                send_baseline_train_message(building_id, model_type, start_date, end_date)
            else:
                insert_model_train_process(building_id, model_type, start_date, end_date)

        return func.HttpResponse(f'Model Training Triggered Successfully for Buildings = {building_ids}!',
                                 status_code=200)

    except Exception as ex:
        log.error(ex)

        return func.HttpResponse(f"Model Training failed!", status_code=500)
