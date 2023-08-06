Python Client For Apache Dubbo
------------------------------

Achieve load balancing on the client side、auto discovery service function with Zookeeper
-----------------------------------------------------------------------------------------

Python calls the Dubbo interface's jsonrpc protocol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Please use dubbo-rpc-jsonrpc and configure protocol in Dubbo for jsonrpc protocol
| *Reference* https://github.com/apache/incubator-dubbo-rpc-jsonrpc

Installation
~~~~~~~~~~~~

| Download code
| python setup.py install
| pip install
| pip install dubbo-python3>=1.0.3 Git install
| pip install git+https://github.com/nickfan/dubbo-python3.git@1.0.3

Load balancing on the client side, service discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Get the registration information of the service through the zookeeper of the registry.
| Dubbo-client-py supports configuring multiple zookeeper service addresses.
| "host":"192.168.1.183:2181,192.168.1.184:2181,192.168.1.185:2181"
| Then the load balancing algorithm is implemented by proxy, and the
| server is called.
| Support Version and Group settings.

### Example
config = ApplicationConfig('test\_rpclib') service\_interface =
'com.ofpay.demo.api.UserProvider' #Contains a connection to zookeeper,
which needs caching. registry = ZookeeperRegistry('192.168.59.103:2181',
config) user\_provider = DubboClient(service\_interface, registry,
version='1.0') for i in range(1000): try:
print(user\_provider.getUser('A003')) print(user\_provider.queryUser(
{u'age': 18, u'time': 1428463514153, u'sex': u'MAN', u'id': u'A003',
u'name': u'zhangsan'})) print(user\_provider.queryAll())
print(user\_provider.isLimit('MAN', 'Joe'))
print(user\_provider('getUser', 'A005')) except DubboClientError as
client\_error: print(client\_error) time.sleep(5)

TODO
~~~~

| Optimize performance, minimize the impact of service upper and lower lines.
| Support Retry parameters
| Support weight call
| Unit test coverage

### Licenses Apache License ### Thanks Thank @jingpeicomp for being a
Guinea pig. It has been running normally for several months in the
production environment. Thank you!
