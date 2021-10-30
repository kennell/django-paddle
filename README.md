# django-paddle

Django models and helpers for integrating Paddle.com subscriptions with your Django app

<sub>⚠️This library is very much **WORK IN PROGRESS**, please read this document carefully to understand what is currently supported.</sub>
             
Currently this package includes:

* Django Models for plans, plan prices, subscriptions, payments (invoices)
* Django management commands for sycing plans, subscriptions, payments
* Webhook receivers that handle subscription creation, subscription cancellation         

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

3. In your `settings.py` add the following settings:

```python
PADDLE_VENDOR_ID = 'your-vendor-id-here'  # https://vendors.paddle.com/authentication
PADDLE_AUTH_CODE = 'your-auth-code-here'  # https://vendors.paddle.com/authentication
PADDLE_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
your
public
key
here
-----END PUBLIC KEY-----"""  # https://vendors.paddle.com/public-key
PADDLE_ACCOUNT_MODEL = 'auth.User'
```

<sub>ℹ️ If you are using the default Django User model, set `PADDLE_ACCOUNT_MODEL` to `auth.User`. If you are using a custom User model set this to something like `your_custom_app.YourUserModel`.</sub>

5. In your projects main `urls.py` add the `django_paddle` URLs for receiving webhooks:

```python
urlpatterns = [
    path('', include('django_paddle.urls')),
]
```

<sub>ℹ️ This will result in an absolute webhook URL `https://example.com/webhook`. Make sure this is the Webhook URL you set in your Paddle settings (https://vendors.paddle.com/alerts-webhooks).</sub>

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


### Automatically connecting Users and Subscriptions

We need a shared identifier between the User model and the PaddleSubscription model. This needs to be provided when we redirect a user to the Paddle checkout. If you are using the default Django User model you can provide a unique user ID as a passthrough value. The `subscription_created` webook will check the passtrough field and see if a User with this ID exists and automatically connect it to the newly created subscription.

Example:

```html
<script src="https://cdn.paddle.com/paddle/paddle.js"></script>
<script>
  Paddle.Setup({ vendor: your-vendor-id-here });
  var uid = "{{ request.user.id }}";  
  Paddle.Checkout.open({
    product: 'your-plan-id-here',
    passthrough: uid
  });
</script>
```    

### Django Management Commands

* `manage.py paddle_sync_plans` - Syncs Subscription Plans
* `manage.py paddle_sync_subscriptions` - Syncs Subscriptions
* `manage.py paddle_sync_payments` - Syncs payments for all subscriptions

### Run tests

```
python runtests.py
```
