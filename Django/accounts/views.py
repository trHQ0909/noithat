from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Account
from customers.models import Customer
from .models import Account
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .services import *
from customers.services import *

def MyAccount(request):
    return render(request, "accounts/myaccount.html")
def Login(request):
    return render(request, "accounts/login.html")
def Register(request):
    return render(request, "accounts/register.html")
def logout_view(request):
    request.session.flush()  
    return redirect("product-home") 
def login_view(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Gọi hàm check_login để kiểm tra
        if check_login(username, password):
            account=get_account(username,password)
            if account.role=="admin":       
                return redirect("product-list")
            else :
                customerid=get_customer_id_by_account_id(account.accountid)
                set_session_data(request,"customerid",customerid)
                print("Customer ID:", request.session.get("customerid"))
                return redirect("product-home")
        else:
            # Đăng nhập thất bại
            return render(request, 'accounts/myaccount.html', {'message': 'Tài khoản hoặc mật khẩu không đúng!'})
        
    else:
        # Nếu không phải POST, hiển thị trang login
        return redirect("MyAccount")
def register_view(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.POST.get('username')
        password = request.POST.get('password')
        sess=get_session_data(request,'customerid')

        # Kiểm tra thông tin đăng ký
        if check_register(username):
            # Tạo tài khoản mới
            account=Account.objects.create(
                username=username,
                password=password,  # Lưu ý: Nên mã hóa mật khẩu trong thực tế
            )
            customer=Customer.objects.create(
                accountid=account,
            )
            # Đăng ký thành công, chuyển hướng đến trang đăng nhập
            return redirect('inputInfo', customerid=customer.customerid)
        elif sess is not None:
            return render(request, 'accounts/myaccount.html', {'message': 'Đăng xuất để đăng ký tài khoản mới '})
        else:
            # Đăng ký thất bại (username hoặc email đã tồn tại)
            return render(request, 'accounts/myaccount.html', {'message': 'Username hoặc email đã tồn tại!'})
    else:
        # Nếu không phải POST, hiển thị trang đăng ký
        return redirect("register")
def update_password(request):
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_new_password = request.POST.get('confirm_new_password')

    if not current_password or not new_password or not confirm_new_password:
        return JsonResponse({'status': 'error', 'message': 'Vui lòng điền đầy đủ thông tin.'})

    if new_password != confirm_new_password:
        return JsonResponse({'status': 'error', 'message': 'Mật khẩu mới không khớp.'})

    customerid = get_session_data(request, 'customerid')
    customer = get_customer_by_id(customerid)
    account = customer.accountid

    if not customer:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy người dùng.'})

    # Assuming 'accountid' is a ForeignKey to your Account model
    if current_password!= account.password:
        return JsonResponse({'status': 'error', 'message': 'Mật khẩu hiện tại không đúng.'})

    if updatePassword(account.accountid, new_password): # Use customer.id as user_id
        return JsonResponse({'status': 'success', 'message': 'Cập nhật mật khẩu thành công.'}) # Sửa status code
    else:
        return JsonResponse({'status': 'error', 'message': 'Đã xảy ra lỗi khi cập nhật mật khẩu.'}) # Lỗi server
