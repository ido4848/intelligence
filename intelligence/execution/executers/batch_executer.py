class BatchExecuter(object):
    def __init__(self, executers):
        self._executers = executers

    def execute(self):
        for executer in self._executers:
            executer.execute()
