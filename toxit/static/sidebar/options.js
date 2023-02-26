const chk = document.getElementById('chk');

chk.addEventListener('change', () => {
	document.body.classList.toggle('dark');
});
 function handleOption(option) {
    switch (option) {
      case 'Wood':
        // Do something for Wood option
        document.documentElement.style.setProperty("--node-bkg-img", "url(/static/img/wood.jpg)");
        break;
      case 'Space':
        // Do something for Space option
        document.documentElement.style.setProperty("--node-bkg-img", "url(/static/img/space.jpg)");
        break;
      case 'Sky':
        // Do something for Sky option
        document.documentElement.style.setProperty("--node-bkg-img", "url(/static/img/sky.jpg)");
        break;
      case 'Blue':
        // Do something for Blue option
        document.documentElement.style.setProperty("--node-bkg-img", "url(/static/img/blue.jpg)");
        break;
      default:
        // Do something for other options
        break;
    }
  }