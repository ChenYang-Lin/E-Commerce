let updateBtns = document.querySelectorAll(".update-cart");

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", () => {
    let productId = updateBtns[i].dataset.product;
    let action = updateBtns[i].dataset.action;

    // console.log("USER: ", user);
    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log("Not logged in");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;
    if (cart[productId]["quantity"] <= 0) {
      console.log("remove item");
      delete cart[productId];
    }
  }

  location.reload();
  console.log("Cart: ", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain;path=/";
}

function updateUserOrder(productId, action) {
  console.log("user is logged in. Sending data..");

  let url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // $("#cart-total").text(data);
      location.reload();
    });
}
