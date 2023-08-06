class noValidationCriteriaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class noColumnMappingException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class noColumnSetUpException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
