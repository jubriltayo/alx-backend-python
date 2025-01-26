import django_filters
from .models import Message
from django.utils import timezone



class MessageFilter(django_filters.FilterSet):
    # Filter messages by sender
    sender = django_filters.CharFilter(field_name='sender__first_name', lookup_expr='icontains', label='Sender')

    # Filter messages by a time range (created_at)
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte', label='Start Date')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte', label='End Date')

    class Meta:
        model = Message
        fields = ['sender', 'sent_at']


    def __init__(self, *args, **kwargs):
        # Ensure filters are not applied to unathenticated users
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and (not request.user.is_authenticated or request.user.is_anonymous):
            self.filters.clear() # remove all filters if the user is not authenticated
        
