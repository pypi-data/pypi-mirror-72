[![PyPI version](https://badge.fury.io/py/jeffy.svg)](https://badge.fury.io/py/jeffy) ![Jeffy CI](https://github.com/serverless-operations/jeffy/workflows/Jeffy%20CI/badge.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python Versions](https://img.shields.io/pypi/pyversions/jeffy.svg)](https://pypi.org/project/jeffy/)

<div align="center">
<img src="https://raw.githubusercontent.com/serverless-operations/jeffy/master/logo.png" alt="Serverless Application Framework Jeffy" width="60%">
</div>

<div align="center">
  <p><strong>Jeffy is Serverless Application Framework for Python AWS Lambda.</strong></p>
</div>


# Description
Jeffy is Serverless **"Application"** Framework for Python, which is
suite of Utilities for Lambda functions to make it easy to develop serverless applications.

Mainly, Jeffy is focusing on three things.

- Logging: Providing easy to see JSON format logging. All decorators are capturing all events, responses and errors. And you can configure to inject additional attributes what you want to see to logs.
- Decorators: To save time to implement common things for Lambda functions, providing some useful decorators and utiliies.
- Tracing: Traceable events within related functions and AWS services with generating and passing `correlation_id`.
- Configurable: You can customize the framework settings easily.

<!-- vscode-markdown-toc -->
* 1. [Logging](#Logging)
	* 1.1. [Basic Usage](#BasicUsage)
	* 1.2. [Injecting additional attributes to logs](#Injectingadditionalattributestologs)
	* 1.3. [Change the attribute name of correlation id](#Changetheattributenameofcorrelationid)
	* 1.4. [Change the log lervel](#Changetheloglervel)
* 2. [Event handlers](#Eventhandlers)
	* 2.1. [common](#common)
	* 2.2. [rest_api](#rest_api)
	* 2.3. [sqs](#sqs)
	* 2.4. [sns](#sns)
	* 2.5. [kinesis_streams](#kinesis_streams)
	* 2.6. [dynamodb_streams](#dynamodb_streams)
	* 2.7. [s3](#s3)
	* 2.8. [schedule](#schedule)
* 3. [SDK](#SDK)
	* 3.1. [Kinesis Clinent](#KinesisClinent)
	* 3.2. [SNS Client](#SNSClient)
	* 3.3. [SQS Client](#SQSClient)
	* 3.4. [S3 Client](#S3Client)
* 4. [Encoding](#Encoding)
* 5. [Validation](#Validation)
	* 5.1. [JSONSchemaValidator](#JSONSchemaValidator)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

# Install

```sh
$ pip install jeffy
```

# Features

##  1. <a name='Logging'></a>Logging

###  1.1. <a name='BasicUsage'></a>Basic Usage
Jeffy logger automatically inject some Lambda contexts to CloudWatchLogs.

```python
from jeffy.framework import get_app

app = get_app()

def handler(event, context):
    app.logger.info({'foo': 'bar'})
```

Output in CloudWatchLogs
```json
{
   "msg": {"foo":"bar"},
   "aws_region":"us-east-1",
   "function_name":"jeffy-dev-hello",
   "function_version":"$LATEST",
   "function_memory_size":"1024",
   "log_group_name":"/aws/lambda/jeffy-dev-hello",
   "log_stream_name":"2020/01/21/[$LATEST]d7729c0ea59a4939abb51180cda859bf",
   "correlation_id":"f79759e3-0e37-4137-b536-ee9a94cd4f52"
}
```

###  1.2. <a name='Injectingadditionalattributestologs'></a>Injecting additional attributes to logs
You can inject some additional attributes what you want to output with using `update_context` method.

```python
from jeffy.framework import get_app
app = get_app()

app.logger.update_context({
   'username': 'user1',
   'email': 'user1@example.com'
})

def handler(event, context):
    app.logger.info({'foo': 'bar'})
```

Output in CloudWatchLogs
```json
{
   "msg": {"foo":"bar"},
   "username":"user1",
   "email":"user1@example.com",
   "aws_region":"us-east-1",
   "function_name":"jeffy-dev-hello",
   "function_version":"$LATEST",
   "function_memory_size":"1024",
   "log_group_name":"/aws/lambda/jeffy-dev-hello",
   "log_stream_name":"2020/01/21/[$LATEST]d7729c0ea59a4939abb51180cda859bf",
   "correlation_id":"f79759e3-0e37-4137-b536-ee9a94cd4f52"
}
```

###  1.3. <a name='Changetheattributenameofcorrelationid'></a>Change the attribute name of correlation id
You can change the attribute name of correlation id in the setting options. 

```python
from jeffy.framework import get_app
from jeffy.settings import Logging
app = get_app(logging=Logging(correlation_attr_name='my-trace-id'))

def handler(event, context):
    app.logger.info({'foo': 'bar'})
```

Output in CloudWatchLogs
```json
{
   "msg": {"foo":"bar"},
   "aws_region":"us-east-1",
   "function_name":"jeffy-dev-hello",
   "function_version":"$LATEST",
   "function_memory_size":"1024",
   "log_group_name":"/aws/lambda/jeffy-dev-hello",
   "log_stream_name":"2020/01/21/[$LATEST]d7729c0ea59a4939abb51180cda859bf",
   "my-trace-id":"f79759e3-0e37-4137-b536-ee9a94cd4f52"
}
```

###  1.4. <a name='Changetheloglervel'></a>Change the log lervel
You can change the log level of Jeffy logger. 

```python
import logging
from jeffy.framework import get_app
from jeffy.settings import Logging
app = get_app(logging=Logging(log_level=logging.DEBUG))

def handler(event, context):
    app.logger.info({'foo': 'bar'})
```

##  2. <a name='Eventhandlers'></a>Event handlers
Decorators make simple to implement common lamdba tasks, such as parsing array from Kinesis, SNS, SQS events etc.

Here are provided decorators

###  2.1. <a name='common'></a>common
`common` decorator allows you to output `event`, `response` and error infomations when you face Exceptions

```python
from jeffy.framework import get_app
app = get_app()

app.logger.update_context({
   'username': 'user1',
   'email': 'user1@example.com'
})

@app.handlers.common()
def handler(event, context):
    ...
```

Error output with auto_logging

```json
{
   "msg": "JSONDecodeError('Expecting value: line 1 column 1 (char 0)')", 
   "exec_info":"Traceback (most recent call last):
  File '/var/task/jeffy/decorators.py', line 41, in wrapper
    raise e
  File '/var/task/jeffy/decorators.py', line 36, in wrapper
    result = func(event, context)
  File '/var/task/handler.py', line 8, in hello
    json.loads('s')
  File '/var/lang/lib/python3.8/json/__init__.py', line 357, in loads
    return _default_decoder.decode(s)
  File '/var/lang/lib/python3.8/json/decoder.py', line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File '/var/lang/lib/python3.8/json/decoder.py', line 355, in raw_decode
    raise JSONDecodeError('Expecting value', s, err.value) from None",
   "function_name":"jeffy-dev-hello",
   "function_version":"$LATEST",
   "function_memory_size":"1024",
   "log_group_name":"/aws/lambda/jeffy-dev-hello",
   "log_stream_name":"2020/01/21/[$LATEST]90e1f70f6e774e07b681e704646feec0",
   "correlation_id":"f79759e3-0e37-4137-b536-ee9a94cd4f52"
}

```

###  2.2. <a name='rest_api'></a>rest_api
Decorator for API Gateway event. Automatically get the correlation id from request header and set the correlation id to response header.

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
app = get_app()

@app.handlers.rest_api()
def handler(event, context):
    return {
        'statusCode': 200,
        'headers': 'Content-Type':'application/json',
        'body': json.dumps({
            'resutl': 'ok.'
        })
    }
```

Default header name is 'x-jeffy-correlation-id'. 
You can change this name in the setting option.

```python
from jeffy.framework import get_app
from jeffy.settings import RestApi
app = get_app(
    rest_api=RestApi(correlation_id_header='x-foo-bar'))

@app.handlers.rest_api()
def handler(event, context):
    return {
        'statusCode': 200,
        'headers': 'Content-Type':'application/json',
        'body': json.dumps({
            'resutl': 'ok.'
        })
    }
```

###  2.3. <a name='sqs'></a>sqs
Decorator for sqs event. Automaticlly parse `"event.Records"` list from SQS event source to each items for making it easy to treat it inside main process of Lambda.

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
app = get_app()

@app.handlers.sqs()
def handler(event, context):
    return event['foo']
    """
    "event.Records" list from SQS event source was parsed each items
    if event.Records value is the following,
     [
         {'foo': 1},
         {'foo': 2}
     ]

    event['foo'] value is 1 and 2, event['correlation_id'] is correlation_id you should pass to next event
    """
```

###  2.4. <a name='sns'></a>sns
Decorator for sns event. Automaticlly parse `event.Records` list from SNS event source to each items for making it easy to treat it inside main process of Lambda.

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
app = get_app()

@app.handlers.sns()
def handler(event, context):
    return event['foo']
    """
    "event.Records" list from SNS event source was parsed each items
    if event.Records value is the following,
     [
         {'foo': 1},
         {'foo': 2}
     ]

    event['foo'] value is 1 and 2, event['correlation_id'] is correlation_id you should pass to next event
    """
```

###  2.5. <a name='kinesis_streams'></a>kinesis_streams
Decorator for kinesis stream event. Automaticlly parse `event.Records` list from Kinesis event source to each items and decode it with base64 for making it easy to treat it inside main process of Lambda.

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
app = get_app()

@app.handlers.kinesis_streams()
def handler(event, context):
    return event['foo']
    """
    "event.Records" list from Kinesis event source was parsed each items
    and decoded with base64 if event.Records value is the following,
     [
         <base64 encoded value>,
         <base64 encoded value>
     ]

    event['foo'] value is 1 and 2, event['correlation_id'] is correlation_id you should pass to next event
    """
```

###  2.6. <a name='dynamodb_streams'></a>dynamodb_streams
Decorator for dynamodb stream event. Automaticlly parse `event.Records` list from Dynamodb event source to  items for making it easy to treat it inside main process of Lambda.

```python
from jeffy.framework import get_app
app = get_app()

@app.handlers.dynamodb_streams()
def handler(event, context):
    return event['foo']
    """
    "event.Records" list from Dynamodb event source was parsed each items
    if event.Records value is the following,
     [
         {'foo': 1},
         {'foo': 2}
     ]

    event['foo'] value is 1 and 2, event['correlation_id'] is correlation_id you should pass to next event
    """
```

###  2.7. <a name='s3'></a>s3
Decorator for S3 event. Automatically parse body stream from triggered S3 object and S3 bucket and key name to Lambda.

**This handler requires `s3:GetObject` permission.**

Default encoding is `jeffy.encoding.bytes.BytesEncoding`.

```python
from jeffy.framework import get_app
app = get_app()

@app.handlers.s3()
def handler(event, context):
    event['key']            # S3 bucket key
    event['bucket_name']    # S3 bucket name
    event['body']           # Bytes data of the object
    event['correlation_id'] # correlation_id
    event['metadata']       # object matadata
```

###  2.8. <a name='schedule'></a>schedule
Decorator for schedule event. just captures correlation id before main Lambda process. do nothing other than that.

```python
from jeffy.framework import setup
app = setup()

@app.handlers.schedule()
def handler(event, context):
    ...
```

##  3. <a name='SDK'></a>SDK
Jeffy has the original wrapper clients of AWS SDK(boto3). The clients automatically inject `correlation_id`  in the event payload and encode it to the specified(or default) encoding. 

###  3.1. <a name='KinesisClinent'></a>Kinesis Clinent

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
from jeffy.sdk.kinesis import Kinesis

app = get_app()

@app.handlers.kinesis_streams()
def handler(event, context):
    Kinesis().put_record(
        stream_name=os.environ['STREAM_NAME'],
        data={'foo': 'bar'},
        partition_key='your_partition_key'
    )
```

###  3.2. <a name='SNSClient'></a>SNS Client

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
from jeffy.sdk.sns import Sns

app = get_app()

@app.handlers.sns()
def handler(event, context):
    Sns().publish(
        topic_arn=os.environ['TOPIC_ARN'],
        subject='hello',
        message='world'
    )
```

###  3.3. <a name='SQSClient'></a>SQS Client

Default encoding is `jeffy.encoding.json.JsonEncoding`.

```python
from jeffy.framework import get_app
from jeffy.sdk.sqs import Sqs

app = get_app()

@app.handlers.sqs()
def handler(event, context):
    Sqs().send_message(
        queue_url=os.environ['QUEUE_URL'],
        message='hello world'
    )
```

###  3.4. <a name='S3Client'></a>S3 Client

Default encoding is `jeffy.encoding.bytes.BytesEncoding`.

```python
from jeffy.framework import get_app
from jeffy.sdk.s3 import S3

app = get_app()

@app.handlers.s3()
def handler(event, context):
    S3().upload_file(
        file_path='/path/to/file', 
        bucket_name=os.environ['BUCKET_NAME'],
        key='key/of/object'
    )
```

##  4. <a name='Encoding'></a>Encoding
Each handler and SDK client has a default encoding and automatically encode/decode the data from/to python object. And you can change the encoding.

Currently, the encodings you can choose are:
- `jeffy.encoding.bytes.BytesEncoding`
- `jeffy.encoding.json.JsonEncoding`

Each encoding class also has `encode` methods to encode `bytes` data into own encoding.

```python
from jeffy.framework import get_app
from jeffy.encoding.bytes import BytesEncoding
from jeffy.sdk.kinesis import Kinesis

app = get_app()
bytes_encoding = BytesEncoding()

@app.handlers.kinesis_streams(encoding=bytes_encoding)
def handler(event, context):
    kinesis = Kinesis(encoding=bytes_encoding)
    kinesis.put_record(
        stream_name=os.environ['STREAM_NAME'],
        data=bytes_encoding.encode('foo'.encode('utf-8)),
        partition_key='your-partition-key'
    )
```

##  5. <a name='Validation'></a>Validation

###  5.1. <a name='JSONSchemaValidator'></a>JSONSchemaValidator
`JsonSchemaValidator` is automatically validate event payload with following json schema you define. raise `ValidationError` exception if the validation fails.

```python
from jeffy.framework import get_app
from jeffy.validator.jsonschema import JsonSchemaValidator

app = get_app()

@app.handlers.rest_api(
    validator=JsonSchemaValidator(schema={
        'type': 'object',
        'properties': {
            'message': {'type': 'string'}}}))
def handler(event, context):
    return {
        'statusCode': 200,
        'headers': 'Content-Type':'application/json',
        'body': json.dumps({
            'message': 'ok.'
        })
    }
```

# Requirements

- Python 3.6 or higher

Development
-----------

-   Source hosted at [GitHub](https://github.com/serverless-operations/jeffy)
-   Report issues/questions/feature requests on [GitHub
    Issues](https://github.com/serverless-operations/jeffy/issues)

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1.  Fork the repo
2.  Create your feature branch (`git checkout -b my-new-feature`)
3.  Commit your changes (`git commit -am"Added some feature"`)
4.  Push to the branch (`git push origin my-new-feature`)
5.  Create new Pull Request

Authors
-------

- Bought up initial idea by [Masashi Terui](https://github.com/marcy-terui) (<marcy9114@gmail.com>)
- Created and maintained by [Serverless Operations, Inc]()

Credits
-------
Jeffy is inspired by the following products.
- [Lambda Powertools](https://github.com/awslabs/aws-lambda-powertools)
- [DAZN Lambda Powertools](https://github.com/getndazn/dazn-lambda-powertools)
- [lambda_decorators](https://github.com/dschep/lambda-decorators)

License
-------

MIT License (see [LICENSE](https://github.com/serverless-operations/jeffy/blob/master/LICENSE))
