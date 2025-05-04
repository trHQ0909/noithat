// Lắng nghe sự kiện click trên các menu item (giữ nguyên)
document.querySelectorAll(".menu-item2").forEach((item) => {
  item.addEventListener("click", function (event) {
      event.preventDefault();
      const section = this.getAttribute("data-section");
      document
          .querySelectorAll(".section")
          .forEach((sec) => sec.classList.remove("active"));
      document
          .querySelectorAll(".menu-item2")
          .forEach((menuItem) => menuItem.classList.remove("active"));
      document.getElementById(`${section}-section`).classList.add("active");
      this.classList.add("active");
  });
});

// Hiển thị section đầu tiên mặc định (giữ nguyên)
document.getElementById("account-section").classList.add("active");
document
  .querySelector('.menu-item2[data-section="account"]')
  .classList.add("active");

// Lưu nội dung ban đầu của account-information (giữ nguyên)
const accountInformation = document.querySelector(".account-information");
const originalContent = accountInformation.innerHTML;

// Hàm hiển thị thông báo
function showMessage(message, type) {
  const messageDiv = document.querySelector('.form-edit-account .message');
  const messageTextDiv = messageDiv.querySelector('.message-text');

  messageDiv.classList.remove('message-type-error', 'message-type-success', 'undefined');
  messageTextDiv.textContent = message;
  messageDiv.classList.remove('undefined');

  if (type === 'success') {
      messageDiv.classList.add('message-type-success');
  } else if (type === 'error') {
      messageDiv.classList.add('message-type-error');
  }
}
// Hàm hiển thị thông báo cho form tài khoản
// Hàm showAccountMessage
function showAccountMessage(message, type) {
  const messageDiv = document.querySelector('.form-edit-account .form-account .message');
  const messageTextDiv = messageDiv.querySelector('.message-text');
  const messageIconContainer = messageDiv.querySelector('.message-icon > div'); // Lấy div chứa SVG

  messageDiv.classList.remove('message-type-error', 'message-type-success', 'hidden');
  messageTextDiv.textContent = message;
  messageDiv.classList.remove('undefined');

  if (type === 'success') {
      messageDiv.classList.add('message-type-success');
      if (messageIconContainer) {
          messageIconContainer.style.backgroundColor = '#155724'; // Màu xanh lá cây cho thành công
      }
  } else if (type === 'error') {
      messageDiv.classList.add('message-type-error');
      if (messageIconContainer) {
          messageIconContainer.style.backgroundColor = '#DC063A'; // Màu đỏ tươi cho lỗi
      }
  }
}

// Hàm showPasswordMessage
function showPasswordMessage(message, type) {
  const messageDiv = document.querySelector('.form-edit-account .form-change-pass .message');
  const messageTextDiv = messageDiv.querySelector('.message-text');
  const messageIconContainer = messageDiv.querySelector('.message-icon > div'); // Lấy div chứa SVG

  messageDiv.classList.remove('message-type-error', 'message-type-success', 'hidden');
  messageTextDiv.textContent = message;
  messageDiv.classList.remove('undefined');

  if (type === 'success') {
      messageDiv.classList.add('message-type-success');
      if (messageIconContainer) {
          messageIconContainer.style.backgroundColor = '#155724'; // Màu xanh lá cây cho thành công
      }
  } else if (type === 'error') {
      messageDiv.classList.add('message-type-error');
      if (messageIconContainer) {
          messageIconContainer.style.backgroundColor = '#DC063A'; // Màu đỏ tươi cho lỗi
      }
  }
}

// Hàm gắn sự kiện cho nút "Chỉnh sửa thông tin" (giữ nguyên)
function attachEditEvent() {
  const editButton = document.querySelector(".account-information button");
  if (editButton) {
      editButton.addEventListener("click", editAccount);
  }
}

// Hàm xử lý khi nhấn "Chỉnh sửa thông tin" (giữ nguyên)
function editAccount() {
  fetch('/customers/geteditform', {
      headers: {
          'X-Requested-With': 'XMLHttpRequest' // Đánh dấu là AJAX request
      }
  })
  .then(response => {
      if (!response.ok) throw new Error('Lỗi tải form: ' + response.status);
      return response.text();
  })
  .then(html => {
      accountInformation.innerHTML = html;
      const changePassCheckbox = document.getElementById(":ru:-form-item");
      const changePassSection = document.querySelector(".form-change-pass");
      // Hiển thị hoặc ẩn form đổi mật khẩu dựa trên trạng thái checkbox
      if (changePassCheckbox.checked) {
          changePassSection.classList.remove("hidden");
      } else {
          changePassSection.classList.add("hidden");
      }
      // Lắng nghe sự kiện thay đổi trên checkbox
      changePassCheckbox.addEventListener("change", function () {
          if (this.checked) {
              changePassSection.classList.remove("hidden");
          } else {
              changePassSection.classList.add("hidden");
          }
      });
  })
  .catch(error => console.error("Lỗi khi tải form:", error));
}

// Hàm xử lý khi nhấn "Lưu"
function saveForm() {
  const changePassCheckbox = document.getElementById(":ru:-form-item");
  const accountForm = document.getElementById("account-form");
  const passwordForm = document.getElementById("password-form");

  // Thu thập dữ liệu từ form thông tin tài khoản
  const accountData = new FormData(accountForm);

  // Gửi form thông tin tài khoản
  console.log("Gửi dữ liệu thông tin tài khoản:", Object.fromEntries(accountData.entries()));
  fetch(accountForm.action, {
      method: 'POST',
      body: accountData,
      headers: {
          'X-CSRFToken': accountData.get('csrfmiddlewaretoken'),
          'X-Requested-With': 'XMLHttpRequest'
      }
  })
  .then(response => {
      if (!response.ok) throw new Error('Lỗi gửi form tài khoản: ' + response.status);
      return response.json();
  })
  .then(data => {
      console.log("Account update response:", data);
      if (data.status === 'success') {
        showAccountMessage(data.message, 'success');

          if (data.redirect_url) {
            setTimeout(function() {
              window.location.href = data.redirect_url;
          }, 2000);
              // window.location.href = data.redirect_url; // Thực hiện redirect ở client
          }
      } else {
          showMessage(data.message, 'error');
      }
  })
  .catch(error => {
      console.error("Lỗi khi gửi form tài khoản:", error);
      showMessage("Đã có lỗi xảy ra khi gửi form tài khoản.", 'error');
  });

  // Nếu checkbox đổi mật khẩu được chọn, gửi thêm form đổi mật khẩu
  if (changePassCheckbox.checked) {
      const passwordData = new FormData(passwordForm);
      const passwordObj = Object.fromEntries(passwordData.entries());

      // Kiểm tra mật khẩu mới và xác nhận mật khẩu
      if (passwordObj.new_password !== passwordObj.confirm_new_password) {
          showMessage("Mật khẩu mới và xác nhận mật khẩu không khớp!", 'error');
          return;
      }
      console.log("Gửi dữ liệu đổi mật khẩu:", passwordObj);
      fetch(passwordForm.action, {
          method: 'POST',
          body: passwordData,
          headers: {
              'X-CSRFToken': passwordData.get('csrfmiddlewaretoken'),
              'X-Requested-With': 'XMLHttpRequest'
          }
      })
      .then(response => {
          if (!response.ok) throw new Error('Lỗi gửi form mật khẩu: ' + response.status);
          return response.json();
      })
      .then(data => {
          console.log("Password update response:", data);
          if (data.status === 'success') {
            showPasswordMessage("Cập nhật mật khẩu thành công!", 'success');
              // Có thể muốn làm gì đó sau khi đổi mật khẩu thành công, ví dụ: ẩn form đổi mật khẩu
              // document.querySelector(".form-change-pass").classList.add("hidden");
              // changePassCheckbox.checked = false;
          } else {
            showPasswordMessage(data.message, 'error');
          }
      })
      .catch(error => {
          console.error("Lỗi khi gửi form mật khẩu:", error);
          showMessage("Đã có lỗi xảy ra khi gửi form mật khẩu.", 'error');
      });
  }
}

// Hàm xử lý khi nhấn "Hủy" (giữ nguyên)
function cancelEdit() {
  accountInformation.innerHTML = originalContent;
  attachEditEvent();
}

// Gán sự kiện ban đầu cho nút "Chỉnh sửa thông tin" (giữ nguyên)
attachEditEvent();
//Ânr hiện pass
document.addEventListener('DOMContentLoaded', function () {
    // Hàm gắn sự kiện hiển thị/ẩn mật khẩu
    function attachPasswordToggleEvents() {
        const showPassIcons = document.querySelectorAll('.show-pass-icon');
        
        showPassIcons.forEach(icon => {
            // Xóa sự kiện cũ để tránh trùng lặp
            icon.removeEventListener('click', togglePasswordVisibility);
            icon.addEventListener('click', togglePasswordVisibility);
        });
    }

    // Hàm xử lý chuyển đổi hiển thị/ẩn mật khẩu
    function togglePasswordVisibility(event) {
        const icon = event.currentTarget;
        const formGroup = icon.closest('.form-group');
        if (!formGroup) return; // Thoát nếu không tìm thấy form-group
        
        const passwordInput = formGroup.querySelector('input[type="password"], input[type="text"]');
        const eyeIcon = icon.querySelector('.eye-icon');

        if (!passwordInput || !eyeIcon) return; // Thoát nếu không tìm thấy input hoặc icon

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            eyeIcon.classList.remove('lucide-eye-off');
            eyeIcon.classList.add('lucide-eye');
            eyeIcon.innerHTML = `
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                <circle cx="12" cy="12" r="3"></circle>
            `;
        } else {
            passwordInput.type = 'password';
            eyeIcon.classList.remove('lucide-eye');
            eyeIcon.classList.add('lucide-eye-off');
            eyeIcon.innerHTML = `
                <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"></path>
                <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"></path>
                <line x1="2" x2="22" y1="2" y2="22"></line>
            `;
        }
    }

    // Gắn sự kiện ban đầu
    attachPasswordToggleEvents();

    // Lắng nghe sự thay đổi của checkbox "Thay Đổi Mật Khẩu"
    const changePassCheckbox = document.getElementById(':ru:-form-item');
    if (changePassCheckbox) {
        changePassCheckbox.addEventListener('change', function () {
            if (this.checked) {
                // Đợi DOM cập nhật và gắn lại sự kiện
                setTimeout(attachPasswordToggleEvents, 100);
            }
        });
    }

    // Lắng nghe thay đổi nội dung form động (nếu form được tải qua AJAX)
    const accountInformation = document.querySelector('.account-information');
    if (accountInformation) {
        const observer = new MutationObserver(() => {
            attachPasswordToggleEvents();
        });
        observer.observe(accountInformation, { childList: true, subtree: true });
    }
});