import asyncio
import os
import time
from gera2ld.socks.client import create_client
from gera2ld.socks.server import Config, SOCKSServer, SOCKS5Handler
from gera2ld.socks.utils import get_host, set_resolver
from async_dns.resolver import ProxyResolver
from async_dns.core import TCP, UDP
from .storage import Storage

cache = None

def delayed(handle, t, name=None):
    async def delayed_handle():
        if t > 0: await asyncio.sleep(t)
        return await handle()
    return asyncio.create_task(delayed_handle(), name=name)

class SOCKSProxyHandler(SOCKS5Handler):
    async def handle_connect(self):
        self.orig_addr = self.addr
        hostname, port = self.addr
        try:
            host = await get_host(hostname)
        except:
            print('DNS failed:', hostname)
            raise
        self.addr = host, port
        result = cache.get(hostname)
        strategy = {
            'direct': 0,
            'proxy': 3,
        }
        if result is not None:
            type, ts = result
            if type == 'direct':
                strategy['proxy'] = 5
            elif type == 'proxy':
                strategy['proxy'] = 0
                if time.time() < ts + 24 * 60 * 60:
                    strategy['direct'] = 3
        task_direct = delayed(self.handle_connect_direct, strategy['direct'], name='direct')
        task_proxy = delayed(self.handle_connect_proxy, strategy['proxy'], name='proxy')
        tasks = { task_direct, task_proxy }
        while tasks:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                try:
                    result = task.result()
                    cache.set(hostname, (task.get_name(), time.time()))
                    print(task.get_name(), hostname)
                    for task in pending:
                        task.cancel()
                    return result
                except:
                    import traceback
                    traceback.print_exc()
                    tasks.discard(task)
        raise Exception('SOCKS Connection error')

    async def handle_connect_proxy(self):
        client = create_client(os.environ.get('AUTOSOCKS_PROXY', 'socks5://127.0.0.1:9909'), remote_dns=self.config.remote_dns)
        await client.handle_connect(self.orig_addr)
        return client.writer, client.forward(self.writer, self.config.bufsize)

def main():
    global cache
    os.makedirs('data', exist_ok=True)
    cache = Storage('data/cache.json')
    set_resolver(ProxyResolver(proxies=[
        (None, os.environ.get('AUTOSOCKS_DNS', '114.114.114.114').split(',')),
    ], protocol=TCP if os.environ.get('AUTOSOCKS_DNS_PROTOCOL') == 'tcp' else UDP))
    config = Config(os.environ.get('AUTOSOCKS_BIND', ':1080'), True)
    server = SOCKSServer(config)
    server.handlers[5] = SOCKSProxyHandler
    server.serve()

if __name__ == '__main__':
    main()
