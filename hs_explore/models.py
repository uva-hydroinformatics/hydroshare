from django.db import models, transaction
from hs_core.models import BaseResource
from django.contrib.auth.models import User, Group
from hs_core.hydroshare import user_from_id, group_from_id, get_resource_by_shortkey


class Status(object):
    STATUS_NEW = 1
    STATUS_VIEWED = 2
    STATUS_APPROVED = 3
    STATUS_DISMISSED = 4
    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_VIEWED, 'Viewed'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_DISMISSED, 'Dismissed')
    )


class RecommendedResource(models.Model):
    user = models.ForeignKey(User, editable=False)
    candidate_resource = models.ForeignKey(BaseResource, editable=False,
                                           related_name='resource_recommendation')
    relevance = models.FloatField(editable=False, default=0.0)
    state = models.IntegerField(choices=Status.STATUS_CHOICES,
                                default=Status.STATUS_NEW,
                                editable=False)

    class Meta:
        unique_together = ('user', 'candidate_resource')

    @staticmethod
    def recommend(u, r, relevance=None, state=None):

        defaults = {}
        if relevance is not None:
            defaults['relevance'] = relevance
        if state is not None:
            defaults['state'] = state

        with transaction.atomic():
            object, created = RecommendedResource.objects.get_or_create(user=u,
                                                                         candidate_resource=r,
                                                                         defaults=defaults)
            if not created:
                if relevance is not None:
                    object.relevance = relevance
                if state is not None:
                    object.state = state
                if relevance is not None or state is not None:
                    object.save()

    @staticmethod
    def recommend_ids(uid, rid, relevance=None, state=None):
        """ use string ids rather than User and Resource objects """
        u = user_from_id(uid, raise404=False)
        r = get_resource_by_shortkey(rid, or_404=False)
        RecommendedResource.recommend(u, r, relevance=relevance, state=state)

    def viewed(self):
        self.state = Status.STATUS_VIEWED
        self.save()

    def approved(self):
        self.state = Status.STATUS_APPROVED
        self.save()

    def dismissed(self):
        self.state = Status.STATUS_DISMISSED
        self.save()

    @staticmethod
    def delete(u, r):
        try:
            record = RecommendedResource.objects.get(user=u, candidate_resource=r)
            record.delete()
        except Exception:
            pass

    @staticmethod
    def clear():
        for r in RecommendedResource.objects.all():
            r.delete()


class RecommendedUser(models.Model):
    """ Users whose attributes cause them to be recommended """
    user = models.ForeignKey(User, editable=False)
    candidate_user = models.ForeignKey(User, editable=False, related_name='user_recommendation')
    relevance = models.FloatField(editable=False, default=0.0)
    state = models.IntegerField(choices=Status.STATUS_CHOICES,
                                default=Status.STATUS_NEW,
                                editable=False)

    class Meta:
        unique_together = ('user', 'candidate_user')

    @staticmethod
    def recommend(u, r, relevance=None, state=None):

        defaults = {}
        if relevance is not None:
            defaults['relevance'] = relevance
        if state is not None:
            defaults['state'] = state

        with transaction.atomic():
            object, created = RecommendedUser.objects.get_or_create(user=u, candidate_user=r,
                                                                     defaults=defaults)
            if not created:
                if relevance is not None:
                    object.relevance = relevance
                if state is not None:
                    object.state = state
                if relevance is not None or state is not None:
                    object.save()

    @staticmethod
    def recommend_ids(uid, rid, relevance=None, state=None):
        """ use string ids rather than User and Resource objects """
        u = user_from_id(uid, raise404=False)
        r = user_from_id(rid, or_404=False)
        RecommendedUser.recommend(u, r, relevance=relevance, state=state)

    def viewed(self):
        self.state = Status.STATUS_VIEWED
        self.save()

    def approved(self):
        self.state = Status.STATUS_APPROVED
        self.save()

    def dismissed(self):
        self.state = Status.STATUS_DISMISSED
        self.save()

    @staticmethod
    def delete(u, r):
        try:
            record = RecommendedUser.objects.get(user=u, candidate_user=r)
            record.delete()
        except Exception:
            pass

    @staticmethod
    def clear():
        for r in RecommendedUser.objects.all():
            r.delete()


class RecommendedGroup(models.Model):
    """ Groups whose attributes cause them to be recommended """
    user = models.ForeignKey(User, editable=False)
    candidate_group = models.ForeignKey(Group, editable=False, related_name='group_recommendation')
    relevance = models.FloatField(editable=False, default=0.0)
    state = models.IntegerField(choices=Status.STATUS_CHOICES,
                                default=Status.STATUS_NEW,
                                editable=False)

    class Meta:
        unique_together = ('user', 'candidate_group')

    @staticmethod
    def recommend(u, r, relevance=None, state=None):

        defaults = {}
        if relevance is not None:
            defaults['relevance'] = relevance
        if state is not None:
            defaults['state'] = state

        with transaction.atomic():
            object, created = RecommendedGroup.objects.get_or_create(user=u,
                                                                      candidate_group=r,
                                                                      defaults=defaults)
            if not created:
                if relevance is not None:
                    object.relevance = relevance
                if state is not None:
                    object.state = state
                if relevance is not None or state is not None:
                    object.save()

    @staticmethod
    def recommend_ids(uid, rid, relevance=None, state=None):
        """ use string ids rather than User and Resource objects """
        u = user_from_id(uid, raise404=False)
        r = group_from_id(rid, or_404=False)
        RecommendedGroup.recommend(u, r, relevance=relevance, state=state)

    def viewed(self):
        self.state = Status.STATUS_VIEWED
        self.save()

    def approved(self):
        self.state = Status.STATUS_APPROVED
        self.save()

    def dismissed(self):
        self.state = Status.STATUS_DISMISSED
        self.save()

    @staticmethod
    def delete(u, r):
        try:
            record = RecommendedGroup.objects.get(user=u, candidate_group=r)
            record.delete()
        except Exception:
            pass

    @staticmethod
    def clear():
        for r in RecommendedGroup.objects.all():
            r.delete()