__publisher__ = None
__subscriber__ = None


def create_publisher(refresh=False, credentials=None):
    from google.cloud.pubsub import PublisherClient
    global __publisher__
    if __publisher__ is None or refresh:
        __publisher__ = PublisherClient()
    return __publisher__


def create_subscriber(refresh=False, credentials=None):
    from google.cloud.pubsub import SubscriberClient
    global __subscriber__
    if __subscriber__ is None or refresh:
        __subscriber__ = SubscriberClient()
    return __subscriber__


def format_pubsub_name(name, project_id=None, pubsub_type='topic'):
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    mapping = dict(topic='topics', subscription='subscriptions')
    if pubsub_type not in mapping.keys():
        raise ValueError('Invalid pubsub_type. pubsub_type must be topic or subscription')
    if not project_id:
        project_id = app_settings['project_id']
    return 'projects/{0}/{1}/{2}'.format(project_id, mapping[pubsub_type], name.split('/')[-1])


def get_topic(name, project_id=None):
    from stratus_api.core.settings import get_settings
    settings = get_settings(settings_type="app")
    publisher = create_publisher()
    topic_name = format_pubsub_name(name=name, pubsub_type='topic', project_id=project_id)
    topic = publisher.get_topic(topic_name)
    return topic


def create_topic(name, project_id=None) -> tuple:
    from google.api_core.exceptions import Conflict
    from stratus_api.core.logs import get_logger
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    logger = get_logger()
    publisher = create_publisher()
    topic_name = format_pubsub_name(name=name, pubsub_type='topic', project_id=project_id)
    created = False
    try:
        publisher.create_topic(topic_name)
    except Conflict as e:
        logger.warning(e)
    else:
        created = True
    return topic_name, created


def delete_topic(name, project_id=None):
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    publisher = create_publisher()
    topic_name = format_pubsub_name(name=name, pubsub_type='topic', project_id=project_id)
    publisher.delete_topic(topic_name)
    return topic_name, True


def get_subscription(name, project_id=None):
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    subscriber = create_subscriber()
    subscription_name = format_pubsub_name(name=name, pubsub_type='subscription', project_id=project_id)
    subscription = subscriber.get_subscription(subscription_name)
    return subscription


def delete_subscription(name, project_id=None):
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    subscriber = create_subscriber()
    subscription_name = format_pubsub_name(name=name, pubsub_type='subscription', project_id=project_id)
    subscriber.delete_subscription(subscription_name)
    return True


def create_subscription(topic, subscription, path, project_id=None):
    from google.api_core.exceptions import Conflict
    from stratus_api.core.logs import get_logger
    from urllib.parse import urljoin
    from stratus_api.core.settings import get_settings
    logger = get_logger()
    app_settings = get_settings(settings_type='app')
    subscriber = create_subscriber()
    push_config = dict()
    created = False
    topic_name = format_pubsub_name(name=topic, pubsub_type='topic', project_id=project_id)
    subscription_name = format_pubsub_name(
        name=subscription, pubsub_type='subscription', project_id=project_id,
    )
    if app_settings.get('service_url'):
        push_config['push_endpoint'] = urljoin(app_settings['service_url'], path)
    try:
        subscriber.create_subscription(
            topic=topic_name, name=subscription_name, push_config=push_config
        )
    except Conflict as e:
        logger.warning(e)
    else:
        created = True
    return subscription, created


def create_topics_and_subscriptions(topic_list):
    for topic in topic_list:
        create_topic(name=topic['topic'], project_id=topic.get('project_id'))
        if topic.get('subscription'):
            create_subscription(topic=topic['topic'], subscription=topic['subscription'], path=topic['path'],
                                project_id=topic.get('project_id'))
    return topic_list


def push_to_topic(topic_name, attributes, payload: dict):
    import json
    publisher = create_publisher()
    topic=format_pubsub_name(name=topic_name)
    publisher.publish(
        topic=topic, data=json.dumps(payload).encode('utf-8'),
        **{k: v for k, v in attributes.items() if v is not None and k not in {'data', 'topic'}}
    ).result()
    return True
