var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'Action', action)
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}

//Based on the productId and action manage the cart for an unauthenticated user
function addCookieItem(productId, action) {
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'remove' && cart[productId] != undefined) {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

//Based on the productId and action make a request to an endpoint
//that manages the updates of an authenticated user
function updateUserOrder(productId, action) {
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data', data.cart_total)
            location.reload()
        })
}