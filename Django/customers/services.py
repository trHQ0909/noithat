from django.core.exceptions import ObjectDoesNotExist
from .models import Customer

def get_customer_id_by_account_id(account_id):
    """
    Lấy customerID dựa vào accountID.
    Args:
        account_id (int): Giá trị accountID từ bảng Account.
    Returns:
        int: customerID nếu tìm thấy, None nếu không.
    """
    try:
        # Truy vấn Customer dựa trên accountid
        customer = Customer.objects.get(accountid=account_id)
        return customer.customerid
    except ObjectDoesNotExist:
        # Trả về None nếu không tìm thấy customer tương ứng
        return None

def get_customer_by_id(customer_id):
    """Trả về đối tượng Customer theo ID, nếu không tồn tại thì trả về None"""
    try:
        return Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return None
def update_customer(customerid, name, phone, address,date,gender):
    """
    Cập nhật thông tin khách hàng theo customerid.
    Nếu khách hàng không tồn tại, trả về False.
    Nếu cập nhật thành công, trả về True.
    """
    try:
        customer = Customer.objects.get(pk=customerid)
        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.date=date
        customer.gender=gender
        customer.save()
        return True
    except Customer.DoesNotExist:
        return False