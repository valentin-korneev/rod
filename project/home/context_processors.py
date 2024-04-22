from datetime import datetime

from config import settings


def get_project_info(request):
    return {
        'application_name': settings.APPLICATION_NAME,
        'start_year': 2024,
        'current_year': datetime.now().year,
    }
