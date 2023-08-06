# coding=UTF-8
from __future__ import print_function

import time
import cassandra.cluster
import sys

from cassandra.auth import PlainTextAuthProvider


def wait_for_cassandra(host_name='localhost',
                       wait_timeout=300, login=None, password=None):
    start_at = time.time()
    wait_println_counter = 0

    auth_provider = None
    if login is not None and password is not None:
        auth_provider = PlainTextAuthProvider(username=login, password=password)

    while time.time() - start_at < wait_timeout:
        try:
            cluster = cassandra.cluster.Cluster([host_name],
                                                load_balancing_policy=
                                                cassandra.cluster.TokenAwarePolicy(
                                                    cassandra.cluster.DCAwareRoundRobinPolicy(
                                                        local_dc='datacenter1'
                                                    )
                                                ),
                                                auth_provider=auth_provider
                                                )
            cluster.connect()

        except (cassandra.cluster.NoHostAvailable, cassandra.UnresolvableContactPoints):
            wait_println_counter += 3
            if wait_println_counter == 3:
                print("Waiting 30 more seconds...")
                wait_println_counter = 0
            time.sleep(10)
        else:
            sys.exit(0)
    else:
        print("Waiting time exceeded, aborting...")
        sys.exit(1)


def run():
    if '-h' in sys.argv:
        print('''Use like:

    wait_for_cassandra <hostname> <wait timeout>

    wait_for_cassandra <hostname> <wait timeout> <login> <password>

    Default hostname is localhost, and default timeout is 300 seconds''')
        sys.exit(0)

    hostname, timeout, login, password = 'localhost', 300, None, None

    if len(sys.argv) == 5:
        _, hostname, timeout, login, password = sys.argv
    elif len(sys.argv) == 3:
        _, hostname, timeout = sys.argv
    elif len(sys.argv) == 2:
        _, hostname = sys.argv

    timeout = float(timeout)

    wait_for_cassandra(hostname, timeout, login, password)


if __name__ == '__main__':
    run()
