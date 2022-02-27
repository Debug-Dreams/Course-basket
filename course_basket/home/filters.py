import django_filters
from home.models import Course

class CourseFilter(django_filters.FilterSet):
    FilteredBy = django_filters.ChoiceFilter()
    class Meta:
        model = Course
        fields = [
            'type',
            'credits',
            # 'Duration',
            # '',
            # 'Tags',
            # 'FilteredBy'
        ]