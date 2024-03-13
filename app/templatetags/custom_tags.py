from django import template
import math

register = template.Library()

@register.simple_tag
def calculate_due_amount(total_amount, paid_amount):
    try:
        total_amount = int(total_amount)
        paid_amount = int(paid_amount)
        due_amount = total_amount - paid_amount
        return due_amount if not math.isnan(due_amount) else 'N/A'
    except (TypeError, ValueError):
        return 'N/A'
    
@register.simple_tag
def calculate_total_amount(list):
    total_amount=0
    for item in list:
        amount = int(item.total_amount)
        total_amount+=amount

    total_amount = (format (total_amount, ',d')) 

    return total_amount


@register.simple_tag
def calculate_paid_amount(list):
    paid_amount=0
    for item in list:
        amount = int(item.paid_amount)
        paid_amount+=amount

    paid_amount = (format (paid_amount, ',d')) 

    return paid_amount


@register.simple_tag
def calculate_total_due_amount(list):
    total_amount=0
    paid_amount=0
    due_amount=0
    for item in list:
        total_amount = int(item.total_amount)
        paid_amount = int(item.paid_amount)

        due_amount +=  (total_amount - paid_amount)

    due_amount = (format (due_amount, ',d')) 

    return due_amount