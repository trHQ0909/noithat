
handleImageUpload("images", "image-preview", "addForm");
function handleImageUpload(inputId, previewId, formId) {
  const imageInput = document.getElementById(inputId);
  const previewContainer = document.getElementById(previewId);
  let uploadedFiles = [];

  if (!imageInput || !previewContainer) {
      console.error(`Không tìm thấy input hoặc container cho ${formId}`);
      return;
  }

  imageInput.addEventListener("change", function (event) {
      const files = Array.from(event.target.files);
      files.forEach((file) => {
          if (file.type.startsWith("image/")) {
              const reader = new FileReader();
              reader.onload = function (e) {
                  addImageToPreview(e.target.result, file, previewContainer);
              };
              reader.readAsDataURL(file);
          }
      });

      setTimeout(() => (event.target.value = ""), 50);
  });

  function addImageToPreview(imageSrc, file, container) {
      const imgContainer = document.createElement("div");
      imgContainer.classList.add("image-container");
      imgContainer.setAttribute("data-file-name", file.name);

      const img = document.createElement("img");
      img.src = imageSrc;

      const deleteBtn = document.createElement("button");
      deleteBtn.classList.add("delete-btn");
      deleteBtn.innerHTML = "×";
      deleteBtn.onclick = function () {
          uploadedFiles = uploadedFiles.filter((f) => f !== file);
          imgContainer.remove();
          updateImageOrder();
      };

      imgContainer.appendChild(img);
      imgContainer.appendChild(deleteBtn);
      container.appendChild(imgContainer);

      uploadedFiles.push(file);
      enableDragAndDrop(container);
  }

  function enableDragAndDrop(container) {
      if (container) {
          new Sortable(container, {
              animation: 150,
              ghostClass: "sortable-ghost",
              onEnd: function () {
                  updateImageOrder();
              },
          });
      }
  }

  function updateImageOrder() {
      const newOrder = Array.from(previewContainer.children).map((imgContainer) => {
          return imgContainer.getAttribute("data-file-name");
      });

      uploadedFiles.sort((a, b) => {
          return newOrder.indexOf(a.name) - newOrder.indexOf(b.name);
      });

      console.log(`Updated Order in ${formId}:`, uploadedFiles.map((f) => f.name));
  }

  document.getElementById(formId).addEventListener("submit", function (event) {
      updateImageOrder();
      const dataTransfer = new DataTransfer();
      uploadedFiles.forEach(file => dataTransfer.items.add(file));
      document.getElementById(inputId).files = dataTransfer.files;
  });
}

// Gọi hàm cho từng form



// Code cũ vẫn giữ nguyên
function showSection(sectionId) {
  document.querySelectorAll(".section").forEach((section) => {
    section.classList.remove("active");
  });
  document.getElementById(sectionId).classList.add("active");
}

document.addEventListener("DOMContentLoaded", () => {
  showSection("dashboard");
});

function deleteProduct(button, name) {
  console.log("Tên sản phẩm:", name); // Kiểm tra xem name có giá trị đúng không
  const url = button.getAttribute("data-url"); // Lấy URL xóa

  if (!confirm(`Bạn có chắc chắn muốn xóa ${name} không?`)) return;

  fetch(url, { method: "DELETE" })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message || "Xóa thất bại!");
      button.closest(".product-box").remove(); // Xóa sản phẩm khỏi giao diện
    })
    .catch((error) => console.error("Lỗi:", error));
}
function goToProductDetail(productId) {
    window.location.href = `/product/${productId}/`;  // Điều hướng đến trang chi tiết sản phẩm
}

function updateProduct(productid) {
    window.location.href = `/admin_web/update-product/${productid}/`;
  }

  document.getElementById("category-filter").addEventListener("change", function () {
    let selectedOption = this.options[this.selectedIndex]; // Lấy option được chọn
    let category_id = selectedOption.getAttribute("data-url"); // Lấy URL từ thuộc tính data-url
    console.log(category_id)

    if (category_id && category_id !== "all") {
        console.log("category")
        window.location.href = `/admin_web/manageProduct/${category_id}/`;

    } else {
        window.location.href = `/admin_web/manageProduct/`; // Nếu chọn "Tất cả"
        console.log("all")
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const categoryFilter = document.getElementById("category-filter");
    const pathParts = window.location.pathname.split("/").filter(part => part !== ""); // Loại bỏ phần tử rỗng
    const categoryId = pathParts[pathParts.length - 1]; // Lấy phần cuối của URL

    let selectedValue = "all"; // Mặc định chọn "Tất cả"

    if (!isNaN(categoryId)) { // Nếu categoryId là số
        selectedValue = categoryId;
    }

    // Đặt option phù hợp thành "selected"
    for (let option of categoryFilter.options) {
        if (option.value === selectedValue) {
            option.selected = true;
            break;
        }
    }
});

