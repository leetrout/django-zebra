import stripe

# # # # # # #
# Note
# Mixins purposely do not use the property decorator syntax so the
# getter method can be overridden or extended easily.

def _get_attr_value(instance, attr, default=None):
    """
    Simple helper to get the value of an instance's attribute if it exists.
    
    If the instance attribute is callable it will be called and the result will
    be returned.
    
    Optionally accepts a default value to return if the attribute is missing.
    Defaults to `None`
    
    >>> class Foo(object):
    ...     bar = 'baz'
    ...     def hi(self):
    ...         return 'hi'
    >>> f = Foo()
    >>> _get_attr_value(f, 'bar')
    'baz'
    >>> _get_attr_value(f, 'xyz')
    
    >>> _get_attr_value(f, 'xyz', False)
    False
    >>> _get_attr_value(f, 'hi')
    'hi'
    """
    value = default
    if hasattr(instance, attr):
        value = getattr(instance, attr)
        if callable(value):
            value = value()
    return value


class StripeSyncMixin(object):
    """
    Provides 3 properties to help with syncing data with Stripe.
    
    stripe_sync_kwargs should be a dictionary of arguments to pass to
    stripe_create_method.
    
    stripe_create_method can be a string or callable. If a string is provided
    it should start with the stripe method and not include the stripe instance.
    e.g.
        self.stripe_sync_method = self.stripe.Customer.create
        or
        self.stripe_sync_method = 'Customer.create'
    
    """
    stripe_sync_enabled = False
    stripe_sync_kwargs = {}
    stripe_sync_method = ''
    
    def stripe_sync(self):
        if self.stripe_sync and self.stripe_sync_kwargs and self.stripe_sync_method:
            stripe_method = self.stripe_method
            if not callable(stripe_method):
                stripe_method = self.stripe
                for method_part in self.stripe_sync_method.split('.'):
                    stripe_method = getattr(stripe_method, method_part)
            if callable(stripe_method):
                stripe_method(**self.stripe_sync_kwargs)


class StripeMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module.
    
    It optionally supports the ability to set `stripe.api_key` if your class
    has a `stripe_api_key` attribute (method or property).
    """
    def _get_stripe(self):
        if hasattr(self, 'stripe_api_key'):
            stripe.api_key = _get_attr_value(self, 'stripe_api_key')
        return stripe
    stripe = property(_get_stripe)


class StripeCustomerMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module &
    additionally adds a property `stripe_customer` that returns a stripe
    customer instance.
    
    Your class must have an attribute `stripe_customer_id` (method or property)
    to provide the customer id for the returned instance.
    """
    def _get_stripe_customer(self):
        return self.stripe.Customer.retrieve(_get_attr_value(self,
                                        'stripe_customer_id'))
    stripe_customer = property(_get_stripe_customer)


class StripeSubscriptionMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module &
    additionally adds a property `stripe_subscription` that returns a stripe
    subscription instance.
    
    Your class must have an attribute `stripe_customer` (method or property)
    to provide a customer instance with which to lookup the subscription.
    """
    def _get_stripe_subscription(self):
        subscription = None
        customer = _get_attr_value(self, 'stripe_customer')
        if hasattr(customer, 'subscription'):
            subscription = customer.subscription
        return subscription
    stripe_subscription = property(_get_stripe_subscription)


class StripePlanMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module &
    additionally adds a property `stripe_plan` that returns a stripe plan
    instance.
    
    Your class must have an attribute `stripe_plan_id` (method or property)
    to provide the plan id for the returned instance.
    """
    def _get_stripe_plan(self):
        return stripe.Plan.retrieve(_get_attr_value(self, 'stripe_plan_id'))
    stripe_plan = property(_get_stripe_plan)


class StripeInvoiceMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module &
    additionally adds a property `stripe_invoice` that returns a stripe invoice
    instance.
    
    Your class must have an attribute `stripe_invoice_id` (method or property)
    to provide the invoice id for the returned instance.
    """
    def _get_stripe_invoice(self):
        return stripe.Invoice.retrieve(_get_attr_value(self,
                                                        'stripe_invoice_id'))
    stripe_invoice = property(_get_stripe_invoice)


class StripeInvoiceItemMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module &
    additionally adds a property `stripe_invoice_item` that returns a stripe
    invoice item instance.
    
    Your class must have an attribute `stripe_invoice_item_id` (method or
    property) to provide the invoice id for the returned instance.
    """
    def _get_stripe_invoice(self):
        return stripe.Invoice.retrieve(_get_attr_value(self,
                                                    'stripe_invoice_item_id'))
    stripe_invoice = property(_get_stripe_invoice)


class StripeChargeMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module &
    additionally adds a property `stripe_invoice_item` that returns a stripe
    invoice item instance.
    
    Your class must have an attribute `stripe_invoice_item_id` (method or
    property) to provide the invoice id for the returned instance.
    """
    def _get_stripe_charge(self):
        return stripe.Charge.retrieve(_get_attr_value(self, 'stripe_charge_id'))
    stripe_charge = property(_get_stripe_charge)


class ZebraMixin(StripeMixin, StripeCustomerMixin, StripeSubscriptionMixin,
                StripePlanMixin, StripeInvoiceMixin, StripeInvoiceItemMixin,
                StripeChargeMixin):
    """
    Provides all available Stripe mixins in one class.
    
    `self.stripe`
    `self.stripe_customer`
    `self.stripe_subscription`
    `self.stripe_plan`
    """
    pass

