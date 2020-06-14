from django.urls import path, include
from polls.viewsets.polls_viewsets import PollCreate, PollDetail, PollList


urlpatterns = [
    # path("<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    # path("<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    # path("choices/", ChoiceList.as_view(), name="choice_list"),
    # path("vote/<int:pk>/<int:choice_pk>/", CreateVote.as_view(), name="create_vote"),
    path("all-polls/", PollList.as_view(), name="polls_list"),
    path("create-polls/", PollCreate.as_view(), name='poll_create'),
    path("all-polls/<int:pk>/", PollDetail.as_view(), name="poll_detail"),
    # path('choice/<int:pk>/<int:poll_id>/', ChoiceDelete.as_view(), name='choice_delete'),
    # path('choice-edit/<int:pk>/<int:poll_id>/', ChoiceEdit.as_view(), name='choice_edit')

]
