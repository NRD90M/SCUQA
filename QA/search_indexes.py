from .models import Question
from haystack import indexes


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
