handleImageUpload("update-images", "update-image-preview", "updateForm");
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
    const newOrder = Array.from(previewContainer.children).map(
      (imgContainer) => {
        return imgContainer.getAttribute("data-file-name");
      }
    );

    uploadedFiles.sort((a, b) => {
      return newOrder.indexOf(a.name) - newOrder.indexOf(b.name);
    });

    console.log(
      `Updated Order in ${formId}:`,
      uploadedFiles.map((f) => f.name)
    );
  }

  document.getElementById(formId).addEventListener("submit", function (event) {
    updateImageOrder();
    const dataTransfer = new DataTransfer();
    uploadedFiles.forEach((file) => dataTransfer.items.add(file));
    document.getElementById(inputId).files = dataTransfer.files;
  });
  enableDragAndDrop(previewContainer);
}

document.addEventListener("DOMContentLoaded", function () {
    const previewContainer = document.getElementById("update-image-preview");

    if (!previewContainer) return;

    // Lấy tất cả các nút xóa của ảnh cũ
    const deleteButtons = previewContainer.querySelectorAll(".delete-btn");

    deleteButtons.forEach((deleteBtn) => {
        deleteBtn.onclick = function () {
            const imgContainer = deleteBtn.parentElement; // Lấy div chứa ảnh
            const fileName = imgContainer.getAttribute("data-file-name"); // Lấy tên file
            imgContainer.remove(); // Xóa ảnh khỏi giao diện

            // Xóa ảnh khỏi danh sách uploadedFiles nếu có
            uploadedFiles = uploadedFiles.filter((f) => f.name !== fileName);

            updateImageOrder();
        };
    });
    enableDragAndDrop(previewContainer);
});


function goToProductDetail(productId) {
  window.location.href = `/product/${productId}/`; // Điều hướng đến trang chi tiết sản phẩm
}
