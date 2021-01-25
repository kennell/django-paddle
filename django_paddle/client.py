from copy import copy
import requests
from django.conf import settings


class PaddleClient:

    def __init__(self):
        self.base_url = 'https://vendors.paddle.com/api/2.0/'
        self.vendor_id = settings.PADDLE_VENDOR_ID
        self.vendor_auth_code = settings.PADDLE_AUTH_CODE
        self.base_payload = {
            'vendor_id': self.vendor_id,
            'vendor_auth_code': self.vendor_auth_code
        }

    # Plans

    def plans_list(self):
        rsp = requests.post(
            url=self.base_url + 'subscription/plans',
            json=self.base_payload
        )
        return rsp.json()['response']

    def plans_get(self, plan_id):
        payload = copy(self.base_payload)
        payload.update(plan_id=plan_id)
        rsp = requests.post(
            url=self.base_url + 'subscription/plans',
            json=payload
        )
        return rsp.json()['response'][0]

    # Subscriptions

    def subscriptions_list(self, state=None):

        """
        :param state:   filter by state, returns all active, past_due, trialing
                        and paused subscription plans if not specified.
                        Will NOT return deleted subscriptions
                See https://developer.paddle.com/api-reference/subscription-api/users/listusers
        """

        subscriptions = []
        max_results = 200
        payload = copy(self.base_payload)
        payload.update(page=1, results_per_page=max_results)

        if state:
            payload.update(state=state)

        while True:
            data = requests.post(
                url=self.base_url + 'subscription/users',
                json=payload
            ).json()['response']
            subscriptions += data
            if len(data) < max_results:
                break
            else:
                payload['page'] += 1

        return subscriptions

    def subscriptions_get(self, subscription_id):
        payload = copy(self.base_payload)
        payload.update(subscription_id=subscription_id)
        return requests.post(
            url=self.base_url + 'subscription/users',
            json=payload
        ).json()['response'][0]

    def subscriptions_cancel(self, subscription_id):
        payload = copy(self.base_payload)
        payload.update(
            subscription_id=subscription_id
        )
        requests.post(
            url=self.base_url + 'subscription/users_cancel',
            json=payload
        )

    def subscriptions_pause(self, subscription_id):
        payload = copy(self.base_payload)
        payload.update(
            subscription_id=subscription_id,
            pause=True
        )
        requests.post(
            url=self.base_url + 'subscription/users/update',
            json=payload
        )

    def subscriptions_unpause(self, subscription_id):
        payload = copy(self.base_payload)
        payload.update(
            subscription_id=subscription_id,
            pause=False
        )
        requests.post(
            url=self.base_url + 'subscription/users/update',
            json=payload
        )

    # Payments

    def payments_list(self, subscription_id=None, is_paid=None):
        payload = copy(self.base_payload)
        if subscription_id:
            payload.update(subscription_id=subscription_id)
        if is_paid is not None:
            payload.update(is_paid=is_paid)
        return requests.post(
            url=self.base_url + 'subscription/payments',
            json=payload
        ).json()['response']

    # Transactions

    def transactions_list(self, entity, id):
        payload = copy(self.base_payload)
        return requests.post(
            url=self.base_url + '{}/{}/transactions'.format(entity, id),
            json=payload
        ).json()['response']
