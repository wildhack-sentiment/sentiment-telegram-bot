class PrepareData:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        params = self.load_params()

        api_result = self.call_api(params)

        data = self.prepare_data(api_result)

        return self.prepare_dataframe(data)

    def load_params(self):
        return {}

    def call_api(self, params):
        return {}

    def prepare_data(self, api_results):
        return api_results

    def prepare_dataframe(self, data):
        return data
