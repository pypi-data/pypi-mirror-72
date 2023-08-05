Alicorn
========

Alicorn is a Python grpc framework with built in dependency injection and middleware management.

NB: This project is in alpha status at the moment, some functionality may be missing.

```python
from alicorn import Alicorn, GrpcContext, Depends
from helloworld_pb2 import HelloWorldRequest, HelloWorldResponse
from helloworld_pb2_grpc import HelloWorldServicer


app = Alicorn()
app.debug = True


class Database:
    pass    


@app.service
class HelloWorld(HelloWorldServicer):

    def SayHello(self, request: HelloWorldRequest, context: GrpcContext, *, database: Database = Depends()):
        return HelloWorldResponse(message=f"Hello {request.name}")


if __name__ == '__main__':
    app.run()

```

## Features
 - Dependency Injection
 - before_request, after_request, after_request_teardown request handlers
 - .proto defined grpc services or python-defined grpc services
 - Extension Support
 
## Planned Future Features
 - Incoming data validation (using proto rules)
 - More internal extensions
 - Other grpc server support (besides the Google implementation)

## Requirements

- Python 3.7+
- grpcio

## To Do

- Finish Documentation
- Command-Line Options
- Release on PyPi
- Better examples
