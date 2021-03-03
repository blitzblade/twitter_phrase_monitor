// Fetch the header and the footer

fetch("../inc/header.html")
  .then(response => {
    return response.text()
  })
  .then(data => {
    document.getElementById("siteHeader").innerHTML = data;
  });

fetch("../inc/footer.html")
  .then(response => {
    return response.text()
  })
  .then(data => {
    document.querySelector("footer").innerHTML = data;
  });



// Email newsletter toggle

document.getElementById('mce-EMAIL').onclick = function(){
  document.getElementById('gdpr').classList.toggle("gdpr-open");
}

// Site menu toggle

document.getElementById('menuToggle').onclick = function(){
  document.getElementsByTagName("body")[0].classList.toggle("menu-open");
}
