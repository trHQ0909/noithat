from .models import Account
from django.core.exceptions import ObjectDoesNotExist
def check_login(username, password):
    try:
        # Tìm tài khoản theo username
        account = Account.objects.get(username=username)
        # So sánh mật khẩu
        if account.password == password:
            return True
        return False
    except Account.DoesNotExist:
        # Trả về False nếu không tìm thấy username
        return False
def get_account(username, password):
    """
    Lấy đối tượng Account dựa trên username và password.
    Args:
        username (str): Tên người dùng.
        password (str): Mật khẩu.
    Returns:
        Account: Đối tượng Account nếu tìm thấy và đúng mật khẩu, None nếu không.
    """
    try:
        # Truy vấn Account dựa trên username
        account = Account.objects.get(username=username)
        # Kiểm tra mật khẩu
        if account.password == password:
            return account
        return None  # Mật khẩu không đúng
    except Account.DoesNotExist:
        # Trả về None nếu không tìm thấy username
        return None
def updatePassword(accountid, newPassword):
    try:
        account = Account.objects.get(accountid=accountid)
        account.password=newPassword
        account.save()
        return True
    except ObjectDoesNotExist:
        return False
    except Exception as e:
        print(f"Lỗi khi cập nhật mật khẩu: {e}")
        return False
def check_register(username):
    """
    Kiểm tra xem username hoặc email đã tồn tại chưa.
    Trả về True nếu có thể đăng ký, False nếu không.
    """
    if Account.objects.filter(username=username).exists():
        return False  # Username đã tồn tại
    return True  # Có thể đăng kýcount.objects.filter(email=email).exists():
    #     return False  # Email đã tồn tại
def set_session_data(request, key, value):
    request.session[key] = value
    request.session.modified = True  # Đảm bảo session được cập nhật

def get_session_data(request, key):
    return request.session.get(key, None)