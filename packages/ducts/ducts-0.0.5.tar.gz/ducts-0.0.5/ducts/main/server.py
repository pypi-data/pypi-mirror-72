#!/usr/bin/env python3

import sys

import asyncio

from ifconf import configure_module, config_callback, configure_main

from ducts.server import HttpdServer

def run():
    loop = asyncio.get_event_loop()
    server = HttpdServer(loop)
    asyncio.ensure_future(server.run())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()

def main():
    configure_main()
    run()
    
if __name__ == '__main__':
    main()
