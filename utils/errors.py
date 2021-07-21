class TopicNotFoundError(Exception):
    """
    Exception raised when a topic is not found.
    """
    def __init__(self, topic_name):
        self.topic_name = topic_name

    def __str__(self):
        return "Topic '{}' not found.".format(self.topic_name)