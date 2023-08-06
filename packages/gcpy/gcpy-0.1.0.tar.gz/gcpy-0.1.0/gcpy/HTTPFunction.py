from gcpy.CloudFunction import CloudFunctionTrigger, CloudFunction
from gcpy.utils.binary import binary_decode


class HTTPFunctionTrigger(CloudFunctionTrigger):
    cli_trigger_string = '--trigger-http '


class HTTPFunction(CloudFunction):
    name = 'function_public_name'
    trigger = HTTPFunctionTrigger()

    @property
    def cli_trigger_string(self):
        return self.trigger.cli_trigger_string

    def handle(self, request):
        print('Handling {}'.format(request))

    @staticmethod
    def body(request):
        result = request.data
        if not result:
            return
        return binary_decode(result)
