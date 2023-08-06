from celery import shared_task


@shared_task(bind=False, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def update_promise_task(external_id: str, service_name: str, results: dict, status: str) -> dict:
    """Asynchronous task to update task status in order to reduce load on web servers

    :param external_id:
    :param service_name:
    :param results:
    :param status:
    :return:
    """
    from stratus_api.jobs.promises import update_promise, generate_promise_id
    updated, promise = update_promise(
        external_id=external_id, service_name=service_name, results=results,
        status=status)
    return dict(external_id=external_id, service_name=service_name,
                promise_id=generate_promise_id(service_name=service_name, external_id=external_id))
