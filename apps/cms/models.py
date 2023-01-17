from django.db import models


class Faq(models.Model):
    DOCUMENTS, POLICIES, FAQ = 1, 2, 3

    CMS_TYPE_CHOICES = (
        (DOCUMENTS, 'document'),
        (POLICIES, 'policies'),
        (FAQ, 'faq')
    )

    USER_POLICY, SELLER_POLICY = 1, 2
    POLICY_TYPE = (
        (USER_POLICY, 'user'),
        (SELLER_POLICY, 'seller')
    )

    question = models.TextField()
    answer = models.TextField()
    cms_type = models.CharField(max_length=28, choices=CMS_TYPE_CHOICES)
    policy_type = models.CharField(max_length=28, choices=POLICY_TYPE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
