// let plusCart = document.querySelector('.plus-cart');
// let minusCart = document.querySelector('.minus-cart');
//
// console.log('begin script')
//
// plusCart.addEventListener('click', () => {
// 	console.log('plus cart clicked')
// });
//
// minusCart.addEventListener('click', () => {
// 	console.log('minus cart clicked')
// });

// convert working of this to above.
$('.plus-cart').click(function(){

	console.log('plus-cart clicked')
	let id = $(this).attr('pid').toString()
	console.log(id)
	let quantity = this.parentNode.children[2]	// get quantity value

	// use AJAX to pass this value to backend
	$.ajax({
		// send data to backend
		type:'GET',
		url:'/plus-cart',
		data:{
			cart_id:id
		}
		// get data from Backend
		success:function(data){
			console.log(data)
			// update values in front based on back response
			quantity.innerText = data.quantity
			document.getElementById(`quantity${id}`).innerText = data.quantity
			document.getElementById('amount_tt').innerText = data.amount
			document.getElementById('total_amount').innerText = data.total

		}
	})
})
$('.minus-cart').click(function(){

	console.log('minus-cart clicked')
	let id = $(this).attr('pid').toString()
	console.log(id)
	let quantity = this.parentNode.children[2]	// get quantity value

	// use AJAX to pass this value to backend
	$.ajax({
		// send data to backend
		type:'GET',
		url:'/minus-cart',
		data:{
			cart_id:id
		}
		// get data from Backend
		success:function(data){
			console.log(data)
			// update values in front based on back response
			quantity.innerText = data.quantity
			document.getElementById(`quantity${id}`).innerText = data.quantity
			document.getElementById('amount_tt').innerText = data.amount
			document.getElementById('total_amount').innerText = data.total

		}
	})
})
