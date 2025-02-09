// Načtení CSRF tokenu z meta tagu
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");

document.querySelectorAll(".add-to-cart").forEach((button) => {
  button.addEventListener("click", function () {
    const productId = this.dataset.productId;

    fetch("/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ product_id: productId }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Chyba při přidávání do košíku.");
        }
        return response.json();
      })
      .then((data) => {
        alert(data.message);
      })
      .catch((error) => {
        console.error("Chyba:", error);
        alert("Došlo k chybě při přidávání do košíku.");
      });
  });
});
