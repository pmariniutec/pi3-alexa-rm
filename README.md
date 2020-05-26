## UTEC PI3 + Valtx

## IT Assets manager with Alexa + Amazon Echo Dot

### Project Info
- `lambda.py` is the lambda handler for alexa to communicate with.
- `db_utils.py` is a collection of the queries needed plus any extra utilities for processing data as needed.
- `local_debugger.py` is a utility provided by Amazon that enables the ability to debug a lambda function locally.

### Project Setup
```{bash}
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
* Install ngrok if you want to debug the function locally.

### Local Testing:

We use [ngrok](https://ngrok.com/) as a proxy to expose a local server so that we can debug from a local environment without having to upload changes to an AWS Lambda function.

```{bash}
# start the proxy.
ngrok http 3001

# start the local lambda server.
python local_debugger.py --portNumber 3001 --skillEntryFile lambda.py --lambdaHandler handler

# Go to your alexa developer console and go into the "Test" tab to issue commands.
```
