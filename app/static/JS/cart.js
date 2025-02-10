// Načtení CSRF tokenu z meta tagu
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");

// Přidání event listeneru na všechna tlačítka "Koupit"
document.querySelectorAll(".buy-button").forEach((button) => {
  button.addEventListener("click", function () {
    const productId = this.dataset.productId; // Načtení ID produktu

    fetch("/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken, // Ochrana proti CSRF
      },
      body: JSON.stringify({ product_id: productId }), // Odeslání ID produktu
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Chyba při přidávání do košíku.");
        }
        return response.json();
      })
      .then((data) => {
        alert(data.message); // Zobrazení zprávy o úspěchu
        updateCartCount(); // Aktualizace počtu položek v košíku
      })
      .catch((error) => {
        console.error("Chyba:", error);
        alert("Došlo k chybě při přidávání do košíku.");
      });
  });
});

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
      document.getElementById("cart-count").innerText = data.cart_item_count; // Aktualizace počtu v navbaru
    });
}
// Funkce pro aktualizaci počtu položek v košíku
function updateCartCount() {
  fetch("/cart/count", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("cart-count").innerText = data.cart_item_count;
    });
}

// Přidání položky do košíku
document.querySelectorAll(".buy-button").forEach((button) => {
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
        updateCartCount(); // Okamžitá aktualizace počtu položek
      })
      .catch((error) => {
        console.error("Chyba:", error);
        alert("Došlo k chybě při přidávání do košíku.");
      });
  });
});
