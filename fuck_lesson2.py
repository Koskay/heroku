import sentry_sdk

from bottle import Bottle, run
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn="https://ae04dba4deee4ab09adf027ef7ae5b7f@o525576.ingest.sentry.io/5639922",
    integrations=[BottleIntegration()]
)

app = Bottle()


@app.route('/')
def index():
    return "Hello"
    

if __name__ == "__main__":

    app.run(host='localhost', port=8080)