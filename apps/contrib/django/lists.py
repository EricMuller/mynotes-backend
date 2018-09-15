

class AggregateList(list):
    aggregate_data = {}

    def __init__(self, *args, **kwargs):
        self.model = args[1]
        self.aggregate_data = args[2]
        super(AggregateList, self).__init__(args[0])

    def all(self):
        """django filter issue """
        return self
