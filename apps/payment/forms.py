from django.core.exceptions import ValidationError
from muscn.utils.forms import HTML5BootstrapModelForm as form
from django import forms
from .models import BankDeposit, Payment, BankAccount, DirectPayment
from apps.users.models import User


class BankDepositForm(form):
    class Meta:
        model = BankDeposit
        exclude = ('payment', )

    def __init__(self, *args, **kwargs):
        super(BankDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank'].empty_label = None


class PaymentFormMixin(object):
    pass


class BankDepositPaymentForm(form):
    user = forms.ModelChoiceField(User.objects.all(), empty_label=None)
    date_time = forms.DateTimeField()
    amount = forms.FloatField()
    # verified_by = forms.ModelChoiceField(User.objects.all(), empty_label=None)
    remarks = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, commit=True, user=None):
        obj = self.instance
        if not user:
            user = self.cleaned_data['user']
        if not obj.payment_id:
            payment = Payment()
        else:
            payment = obj.payment
        payment.user = user
        payment.amount = self.cleaned_data['amount']
        payment.remarks = self.cleaned_data['remarks']
        payment.date_time = self.cleaned_data['date_time']
        payment.save()
        obj.payment_id = payment.id
        obj.save()
        return super(BankDepositPaymentForm, self).save(commit=True)

    def __init__(self, *args, **kwargs):
        super(BankDepositPaymentForm, self).__init__(*args, **kwargs)
        self.fields['bank'].empty_label = None
        if self.instance.payment_id:
            self.initial['amount'] = self.instance.payment.amount
            self.initial['date_time'] = self.instance.payment.date_time
            self.initial['user'] = self.instance.payment.user
            self.initial['remarks'] = self.instance.payment.remarks

    class Meta:
        model = BankDeposit
        exclude = ('payment', )


class DirectPaymentPaymentForm(form):
    user = forms.ModelChoiceField(User.objects.all(), empty_label=None)
    date_time = forms.DateTimeField()
    amount = forms.FloatField()
    # verified_by = forms.ModelChoiceField(User.objects.all(), empty_label=None)
    remarks = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, commit=True, user=None):
        obj = self.instance
        if not user:
            user = self.cleaned_data['user']
        if not obj.payment_id:
            payment = Payment()
        else:
            payment = obj.payment
        payment.user = user
        payment.amount = self.cleaned_data['amount']
        payment.remarks = self.cleaned_data['remarks']
        payment.date_time = self.cleaned_data['date_time']
        payment.save()
        obj.payment_id = payment.id
        obj.save()
        return super(DirectPaymentPaymentForm, self).save(commit=True)

    def __init__(self, *args, **kwargs):
        super(DirectPaymentPaymentForm, self).__init__(*args, **kwargs)
        # self.fields['received_by'].empty_label = None
        if self.instance.payment_id:
            self.initial['amount'] = self.instance.payment.amount
            self.initial['date_time'] = self.instance.payment.date_time
            self.initial['user'] = self.instance.payment.user
            self.initial['remarks'] = self.instance.payment.remarks

    def clean_receipt_no(self):
        receipt_no = self.cleaned_data['receipt_no']
        if receipt_no == 0:
            raise ValidationError("Receipt no. should not be 0 (zero)")
        return receipt_no

    class Meta:
        model = DirectPayment
        exclude = ('payment', )


class DirectPaymentReceiptForm(form):

    def save(self, commit=True, user=None, payment=None):
        obj = self.instance
        payment.user = user
        payment.remarks = 'R#:' + str(obj.receipt_no)
        payment.save()
        obj.payment_id = payment.id
        obj.save()
        return super(DirectPaymentReceiptForm, self).save(commit=True)

    def __init__(self, *args, **kwargs):
        super(DirectPaymentReceiptForm, self).__init__(*args, **kwargs)
        if self.instance.payment_id:
            self.initial['amount'] = self.instance.payment.amount
            self.initial['date_time'] = self.instance.payment.date_time
            self.initial['user'] = self.instance.payment.user
            self.initial['remarks'] = self.instance.payment.remarks

    class Meta:
        model = DirectPayment
        exclude = ('payment', 'received_by')



class PaymentForm(form):
    class Meta:
        model = Payment
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = None
        self.fields['user'].widget.choices = self.fields['user'].choices


class BankAccountForm(form):
    class Meta:
        model = BankAccount
        exclude = ()