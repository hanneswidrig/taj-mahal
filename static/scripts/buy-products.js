$(document).ready(function() {
	buyProductPage();
	subtractFromPurchase();
	addToPurchase();

	function buyProductPage() {
		availableQuantity = document.querySelector('.purchase-quantity-total').innerHTML;
		submitButton = document.querySelector('#submit');

		if(parseInt(availableQuantity) === 0) {
			plusMinusButtons = document.querySelectorAll('.quantity-button');
			plusMinusButtons[0].disabled = true;
			plusMinusButtons[0].style.backgroundColor = '#a6a6a6';
			plusMinusButtons[1].disabled = true;
			plusMinusButtons[1].style.backgroundColor = '#a6a6a6';
			submitButton.disabled = true;
			submitButton.style.backgroundColor = '#757575';
			submitButton.style.borderColor = '#757575';
		}
	}

	function getQuantityBox() {
		return document.querySelector('#quantity');
	}

	function subtractFromPurchase() {
		subtractButton = document.querySelector('.subtract-button');
		quantityBox = getQuantityBox();
		
		subtractButton.addEventListener("click", function() {
			quantity = parseInt(quantityBox.value);
			if (quantity > 0) {
				quantityBox.value = parseInt(quantity) - 1;
			}
		});
	}
	
	function addToPurchase() {
		addButton = document.querySelector('.add-button');
		availableQuantity = parseInt(document.querySelector('.purchase-quantity-total').innerHTML);
		quantityBox = getQuantityBox();
		
		addButton.addEventListener("click", function() {
			quantity = parseInt(quantityBox.value);
			if (quantity < availableQuantity) {
				quantityBox.value = parseInt(quantity) + 1;
			}
		});
	}
});