from . import util


class Plugin:
    def __init__(self, pipeline):
        self.pipeline = pipeline


class Input(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)
        self.logger = util.get_class_logger(self)
    
    def input(self, rows_prev=None, num_rows_prev=None):
        raise NotImplementedError


class Output(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)
        self.logger = util.get_class_logger(self)

    def output(self, rows, num_rows):
        raise NotImplementedError


class Processor(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)
        self.logger = util.get_class_logger(self)

    def process(self, rows):
        raise NotImplementedError


class Trigger(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)
        self.logger = util.get_class_logger(self)
    
    def run(self):
        raise NotImplementedError
