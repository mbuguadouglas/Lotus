var sidebar = document.querySelector('.sidebar');
var toggleBtn = document.querySelector('.toggle-btn');

toggleBtn.addEventListener('click', () => {
	sidebar.classList.toggle('active');
});

// window.addEventListener('scroll', () => {
// 	sidebar.classList.toggle('active');
// });
