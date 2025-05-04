handleImageUpload("update-images", "update-image-preview", "updateForm");

window.uploadedFiles = window.uploadedFiles || [];

function handleImageUpload(inputId, previewId, formId) {
  const imageInput = document.getElementById(inputId);
  const previewContainer = document.getElementById(previewId);

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
      imgContainer.remove();
      window.uploadedFiles = window.uploadedFiles.filter((f) => f.name !== file.name);
      updateImageOrder();
    };

    imgContainer.appendChild(img);
    imgContainer.appendChild(deleteBtn);
    container.appendChild(imgContainer);

    window.uploadedFiles.push(file);
    enableDragAndDrop(container);
  }

  document.getElementById(formId).addEventListener("submit", function (event) {
    updateImageOrder();
    
    const dataTransfer = new DataTransfer();
    window.uploadedFiles.forEach((file) => {
      if (file instanceof File) {
        dataTransfer.items.add(file);
      }
    });

    document.getElementById(inputId).files = dataTransfer.files;
  });
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
  const previewContainer = document.getElementById("update-image-preview");
  
  // Lấy danh sách tên file theo thứ tự mới
  const newOrder = Array.from(previewContainer.children).map((imgContainer) => {
    return imgContainer.getAttribute("data-file-name");
  });

  // Cập nhật thứ tự trong uploadedFiles
  window.uploadedFiles = newOrder
    .map((name) => window.uploadedFiles.find((file) => file.name === name))
    .filter(Boolean);

  console.log("Updated Order:", window.uploadedFiles.map((f) => f.name));
}

document.addEventListener("DOMContentLoaded", function () {
  const previewContainer = document.getElementById("update-image-preview");
  if (!previewContainer) return;

  const existingImages = previewContainer.querySelectorAll(".image-container");

  existingImages.forEach((imgContainer) => {
    const fileName = imgContainer.getAttribute("data-file-name");

    if (fileName && !window.uploadedFiles.some((f) => f.name === fileName)) {
      fetch(imgContainer.querySelector("img").src)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], fileName, { type: blob.type });
          window.uploadedFiles.push(file);
          console.log("Đã thêm ảnh từ server:", fileName);
        });

      const deleteBtn = imgContainer.querySelector(".delete-btn");
      if (deleteBtn) {
        deleteBtn.onclick = function () {
          imgContainer.remove();
          window.uploadedFiles = window.uploadedFiles.filter((f) => f.name !== fileName);
          updateImageOrder();
        };
      }
    }
  });

  setTimeout(() => {
    enableDragAndDrop(previewContainer);
    console.log("Kéo thả đã được kích hoạt!");
  }, 100);
});

function goToProductDetail(productId) {
  window.location.href = `/product/${productId}/`;
}
