from django.core.exceptions import ValidationError

class EmployerTypeError(ValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__("This user isn't employer.Allow user(admin,teacher,employer)")
