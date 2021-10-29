# django-paddle

Django models and helpers for integrating Paddle.com subscriptions

<small>⚠️This library is very much WORK IN PROGRESS, please read this README carefully to understand what is currently supported</small>

### Installation

Requires:

* Python 3.6+ 
* Django 2.1.0+

1. Install the `django-paddle` package

```
pip install django-paddle
```

2. Add `django_paddle` to your INSTALLED_APPS

```python
INSTALLED_APPS = [
        # ...
        'django_paddle',
        # ...
]
```

3. In your `settings.py`, add the following settings:

```python
PADDLE_VENDOR_ID = '123'
PADDLE_AUTH_CODE = 'your-auth-code-here'
PADDLE_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
your
public
key
here
-----END PUBLIC KEY-----"""
PADDLE_ACCOUNT_MODEL = 'auth.User'
```

If you are using the default Django User model, set `PADDLE_ACCOUNT_MODEL` to `auth.User`. If you are using a custom User model adjust this setting accordingly, for example `your_custom_app.YourUserModel`.

5. In your projects main `urls.py` add the URL to receive webhooks:

```python
urlpatterns = [
    path('', include('django_paddle.urls')),
]
```

This will result in an absolute webhook URL `https://example.com/webhook`. Make sure this is the Webhook URL you set in your Paddle settings.

4. Run migrations

`python manage.py migrate`

The User Model specified in `PADDLE_ACCOUNT_MODEL` will now have a back-reference to the PaddleSubscription and vice versa.

Example:

```python
sub = PaddleSubscription.objects.all()[0]
print(sub.account)  # <User: johndoe@example.com>
```

or

```python
user = User.objects.get(username='johndoe@example.com')
print(u.subscriptions.all())  # <QuerySet [<PaddleSubscription: PaddleSubscription object (123456)>]>
```

5. Done!


### Django Management Commands

* `manage.py paddle_sync_plans` - Syncs Subscription Plans
* `manage.py paddle_sync_subscriptions` - Syncs Subscriptions
* `manage.py paddle_sync_payments` - Syncs payments for all subscriptions


### What works

Currently this package includes:

* Django Models for Plans, Plan prices, Subscriptions, Payments (Invoices)
* Django management commands for sycing plans, subscriptions, payments
* Webhook receivers for subscription creation, subscription cancellation 


### Run tests

```
python runtests.py
```
