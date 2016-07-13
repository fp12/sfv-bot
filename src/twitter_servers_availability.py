from twitter_update import api, get_server_availability


if __name__ == "__main__":
    statuses = api.GetHomeTimeline(exclude_replies=True, count=200)
    print('Received %s statuses' % len(statuses))
    for s in statuses:
        avail = get_server_availability(s.text)
        print('{0:7} - {1}'.format(avail.name, s.text))
