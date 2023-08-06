from render.util import user_data

broker_url = (
    'amqp://'
    f'{user_data["rabbit_user"]}'
    f':{user_data["rabbit_pass"]}'
    f'@{user_data["rabbitmq_host"]}'
    f':{user_data.get("rabbit_port", "5672")}'
    f'/{user_data["rabbit_vhost"]}'
)

task_routes = {
    'local': {'queue': 'local'},
    'rendering': {'queue': 'rendering'},
}

task_serializer = 'json'
accept_content = ['json']
enable_utc = True

task_acks_late = True
worker_prefetch_multiplier = 1
worker_concurrency = 1
worker_disable_rate_limits = True

worker_send_task_events = True
task_send_sent_event = True
