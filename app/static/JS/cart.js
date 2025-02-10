// Načtení CSRF tokenu z meta tagu
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  ?.getAttribute("content");

// Funkce pro aktualizaci počtu položek v košíku v navbaru
function updateCartCount() {
  fetch("/cart/count", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const cartCountElement = document.getElementById("cart-count");
      if (cartCountElement) {
        cartCountElement.innerText = data.cart_item_count;
      }
    })
    .catch((error) =>
      console.error("Chyba při aktualizaci počtu položek:", error)
    );
}

// Přidání produktu do košíku s kontrolou dostupnosti
document.querySelectorAll(".buy-button").forEach((button) => {
  button.addEventListener("click", function () {
    const productId = this.dataset.productId;

    fetch("/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(csrfToken && { "X-CSRFToken": csrfToken }),
      },
      body: JSON.stringify({ product_id: productId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error); // Zobrazení chyby, pokud není produkt skladem
        } else {
          alert(data.message); // Zobrazení zprávy o úspěšném přidání
          updateCartCount(); // Aktualizace počtu položek v košíku
        }
      })
      .catch((error) => {
        console.error("Chyba:", error);
        alert("Došlo k chybě při přidávání do košíku.");
      });
  });
});

// Odebrání produktu z košíku
document.querySelectorAll(".remove-from-cart").forEach((button) => {
  button.addEventListener("click", function () {
    const productId = this.dataset.productId;

    fetch("/cart/remove", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(csrfToken && { "X-CSRFToken": csrfToken }),
      },
      body: JSON.stringify({ product_id: productId }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        updateCartCount(); // Aktualizace počtu položek v navbaru

        const productRow = document.querySelector(
          `tr[data-product-id="${productId}"]`
        );
        if (productRow) {
          productRow.remove();
        }

        // Zkontrolovat, zda košík zůstal prázdný
        const remainingItems = document.querySelectorAll(".cart-item-row");
        if (remainingItems.length === 0) {
          document.querySelector(".cart-container").innerHTML =
            "<p>Váš košík je prázdný.</p>";
        }
      })
      .catch((error) => {
        console.error("Chyba:", error);
        alert("Došlo k chybě při odebírání z košíku.");
      });
  });
});

// Automatická aktualizace počtu položek při načtení stránky
document.addEventListener("DOMContentLoaded", updateCartCount);
