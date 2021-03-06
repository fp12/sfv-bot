from datetime import datetime
from twitter_update import api  # , get_server_availability
from log import log_twitter

if __name__ == "__main__":
    server_statuses = api.GetHomeTimeline(exclude_replies=True, since_id=753756834154938368)
    for s in server_statuses:
        log_twitter.info(s)
    server_statuses.sort(key=lambda status: status.id)
    log_twitter.info('Sorted')
    for s in server_statuses:
        log_twitter.info(s)
    print('%s _do_refresh with %s new status' % (datetime.now().strftime("[%Y/%m/%d] [%I:%M%p]"), len(server_statuses)))

    """
    statuses = api.GetHomeTimeline(exclude_replies=True, count=200)
    print('Received %s statuses' % len(statuses))
    for s in statuses:
        avail = get_server_availability(s.text)
        print('{0:7} - {1}'.format(avail.name, s.text))
        """
