from django import template
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        today = datetime.now().date()
        value = timezone.localtime(value)
        yesterday = today - timedelta(days=1)
        
        if value.date() == today:
            return f"Today At {value.strftime('%I:%M %p')}"
        elif value.date() == yesterday:
            return f"Yesterday At {value.strftime('%I:%M %p')}"
        else:
            return f"{value.date().strftime('%B %d')}, {value.strftime('%I:%M %p')}"
    return "NO Login record available"
        