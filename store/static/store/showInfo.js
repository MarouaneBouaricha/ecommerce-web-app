var Btns = document.getElementsByClassName('showInfo')

for (i = 0; i < Btns.length; i++) {
	Btns[i].addEventListener('click', function(){
        console.log('Product clicking ....')
		var prodId = this.dataset.product
        var url = '/product/'
        console.log('id', prodId)
        fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':getToken('csrftoken'),
			}, 
			body: JSON.stringify({'productId':prodId}),
		})
		.then((response) => {
			return response.json();
		 })
		.then((data) => {
			console.log("Success:", data);

			window.location.href = "{% url 'store-product' %}";
		});
	})
}
