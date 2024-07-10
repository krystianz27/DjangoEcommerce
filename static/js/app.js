// Function to get CSRF token from cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Hide flash messages after a timeout (referenced globally)
var messageTimeoutElements = document.getElementsByClassName("message-timer");

setTimeout(function () {
  for (var i = 0; i < messageTimeoutElements.length; i++) {
    messageTimeoutElements[i].style.display = "none";
  }
}, 2500);

// CRUD in product-info.html
document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("cart-minus-btn")
    .addEventListener("click", function () {
      var quantityInput = document.getElementById("add-to-cart-quantity");
      var currentQty = parseInt(quantityInput.value);
      if (currentQty > 1) {
        quantityInput.value = currentQty - 1;
      }
    });

  document
    .getElementById("cart-plus-btn")
    .addEventListener("click", function () {
      var quantityInput = document.getElementById("add-to-cart-quantity");
      var currentQty = parseInt(quantityInput.value);
      quantityInput.value = currentQty + 1;
    });

  document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "add-to-cart-button") {
      e.preventDefault();

      var product_id = e.target.value;
      var product_quantity = document.getElementById(
        "add-to-cart-quantity"
      ).value;

      var csrftoken = getCookie("csrftoken");

      var requestBody = {
        product_id: product_id,
        product_quantity: product_quantity,
        action: "post",
      };

      fetch(e.target.dataset.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          // "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: new URLSearchParams({
          product_id: product_id,
          product_quantity: product_quantity,
          action: "post",
        }),
        // body: JSON.stringify(requestBody),
      })
        .then((response) => response.json())
        .then((json) => {
          document.getElementById("cart-qty").textContent = json.qty;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  });
});

// Performing CRUD in a cart (referenced in cart-summary.html)
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".cart-minus-btn").forEach((button) => {
    button.addEventListener("click", function () {
      var productId = this.dataset.index;
      var quantityInput = document.getElementById(
        "add-to-cart-quantity-" + productId
      );
      var currentQty = parseInt(quantityInput.value);
      if (currentQty > 1) {
        quantityInput.value = currentQty - 1;
      }
    });
  });

  document.querySelectorAll(".cart-plus-btn").forEach((button) => {
    button.addEventListener("click", function () {
      var productId = this.dataset.index;
      var quantityInput = document.getElementById(
        "add-to-cart-quantity-" + productId
      );
      var currentQty = parseInt(quantityInput.value);
      quantityInput.value = currentQty + 1;
    });
  });

  // Update for each item in a cart
  document.querySelectorAll(".update-cart-button").forEach((button) => {
    button.addEventListener("click", function () {
      var productId = this.dataset.index;
      var productQuantity = parseInt(
        document.getElementById("add-to-cart-quantity-" + productId).value
      );
      var csrftoken = getCookie("csrftoken");

      fetch(this.dataset.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: new URLSearchParams({
          product_id: productId,
          product_quantity: productQuantity,
          action: "post",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          location.reload(true);
          document.getElementById("cart-qty").textContent = json.qty;
          document.getElementById("total").textContent = json.total;
          // var productPriceElement = document.getElementById(
          //   "product-price-" + productId
          // );
          // productPriceElement.textContent = "$ " + json.updated_price;
          // var productPriceElement =
          // this.closest(".product-item").querySelector(".product-price");
          // productPriceElement.textContent = "$ " + json.product_price;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });

  document.querySelectorAll(".delete-from-cart-button").forEach((button) => {
    button.addEventListener("click", function () {
      var product_id = this.dataset.index;
      var csrftoken = getCookie("csrftoken");
      var url = this.dataset.url;

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: new URLSearchParams({
          product_id: product_id,
          action: "post",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          location.reload(); // Przeładuj stronę
          document.getElementById("cart-qty").textContent = json.qty;
          document.getElementById("total").textContent = json.total;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
});

// paypal.js referenced in checkout.html

document.addEventListener("DOMContentLoaded", function () {
  const paypalData = document.getElementById("paypal-button-container");

  const completeOrderUrl = paypalData.dataset.completeOrderUrl;
  const paymentSuccessUrl = paypalData.dataset.paymentSuccessUrl;
  const paymentFailUrl = paypalData.dataset.paymentFailUrl;
  const csrfToken = getCookie("csrftoken");
  const totalPrice = paypalData.dataset.totalPrice;

  const paypalButtonsComponent = paypal.Buttons({
    // Optional styling for buttons
    style: {
      color: "gold",
      shape: "pill",
      layout: "vertical",
    },

    // Initialization function
    onInit: function (data, actions) {
      actions.disable();

      // Event listener to enable/disable buttons based on form validation
      document.querySelectorAll(".validate").forEach((item) => {
        item.addEventListener("keyup", (event) => {
          // Function to check if required fields are filled out
          function checkInputs() {
            var order_verified = true;
            $(":input[required]").each(function () {
              if ($(this).val() === "") {
                order_verified = false;
                return false;
              }
            });
            return order_verified;
          }

          var isOrderVerified = checkInputs();

          if (isOrderVerified === true) {
            actions.enable();
          } else {
            actions.disable();
          }
        });
      });

      // Check inputs on initialization
      function checkInputs() {
        var order_verified = true;
        $(":input[required]").each(function () {
          if ($(this).val() === "") {
            order_verified = false;
            return false;
          }
        });
        return order_verified;
      }

      var isOrderVerified = checkInputs();

      if (isOrderVerified === true) {
        actions.enable();
      } else {
        actions.disable();
      }
    },

    // Set up the transaction
    createOrder: function (data, actions) {
      // https://developer.paypal.com/api/orders/v2/#orders-create-request-body
      var createOrderPayload = {
        purchase_units: [
          {
            amount: {
              value: totalPrice,
            },
          },
        ],
      };
      return actions.order.create(createOrderPayload);
    },

    // Finalize the transaction
    onApprove: function (data, actions) {
      var captureOrderHandler = function (details) {
        var payerName = details.payer.name.given_name;

        // Form data to be sent with the POST request
        var formData = {
          name: $("#name").val(),
          email: $("#email").val(),
          phone_number: $("#phone-number").val(),
          address1: $("#address1").val(),
          number: $("#number").val(),
          city: $("#city").val(),
          state: $("#state").val(),
          zipcode: $("#zipcode").val(),
          csrfmiddlewaretoken: csrfToken,
          action: "post",
        };

        var requestOptions = {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken,
          },
          body: new URLSearchParams(formData),
        };

        fetch(completeOrderUrl, requestOptions)
          .then(function (response) {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Network response was not ok");
            }
          })
          .then(function (data) {
            console.log("Data received:", data);
            // Check if there is a 'success: true' in the response
            if (data && data.success && data.order_id) {
              // Redirect to the payment-success page with order_id in the URL
              window.location.replace(
                paymentSuccessUrl + "?order_id=" + data.order_id
              );
            } else {
              throw new Error("Order creation failed");
            }
          })
          .catch(function (error) {
            console.error(
              "There has been a problem with your fetch operation:",
              error
            );
            window.location.replace(paymentFailUrl);
          });
      };

      return actions.order.capture().then(captureOrderHandler);
    },

    onError: function (err) {
      console.error(
        "An error prevented the buyer from checking out with PayPal"
      );
    },
  });

  paypalButtonsComponent
    .render("#paypal-button-container")
    .catch(function (err) {
      console.error("PayPal Buttons failed to render");
    });
});
