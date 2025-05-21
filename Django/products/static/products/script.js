document.getElementById("buy-now-button").addEventListener("click", function (event) {
  event.stopImmediatePropagation(); // Ngăn tất cả sự kiện click khác
  event.preventDefault(); // Ngăn hành vi mặc định (nếu cần)

  const quantity = document.querySelector(".qty").value;
  const pathArray = window.location.pathname.split("/");
  const productid = pathArray[2];
  window.location.href = `/order/buyProduct/${productid}/${quantity}/`;
}, true); // `true` để xử lý sự kiện ở pha capturing (nếu cần)
function Cart() {
  const pathArray = window.location.pathname.split("/");
  const productid = pathArray[2];
  const quantity = document.querySelector(".qty").value;
  window.location.href = `/order/addCart/${productid}/${quantity}/`;
}
const waitForStars = setInterval(() => {
    console.log("⏳ Đang kiểm tra phần tử p.stars span...");

    const starsContainer = document.querySelector("p.stars span");
    const ratingSelect = document.getElementById("rating");

    if (!ratingSelect) {
        console.warn("⚠️ Không tìm thấy thẻ select có id='rating'");
    }

    if (starsContainer && ratingSelect) {
        console.log("✅ Đã tìm thấy phần tử stars và select rating!");

        clearInterval(waitForStars); // Ngừng kiểm tra sau khi tìm thấy

        const stars = starsContainer.querySelectorAll("a");
        console.log(`🔢 Số lượng sao tìm thấy: ${stars.length}`);

        stars.forEach((star, index) => {
            console.log(`⭐ Gán sự kiện click cho sao số ${index + 1}`);

            star.addEventListener("click", function (e) {
                e.preventDefault();

                console.log(`🖱️ Click vào sao ${index + 1}`);

                // Xóa tất cả class active
                stars.forEach(s => s.classList.remove("active"));

                // Thêm active cho sao được chọn
                star.classList.add("active");

                // Gán giá trị cho select
                ratingSelect.value = index + 1;

                console.log("✅ Giá trị rating được gán vào select:", ratingSelect.value);
                alert("Bạn đã chọn số sao: " + ratingSelect.value);
            });
        });
    } else {
        console.log("🚫 starsContainer hoặc ratingSelect chưa tồn tại.");
    }
}, 300); // Kiểm tra mỗi 300ms
