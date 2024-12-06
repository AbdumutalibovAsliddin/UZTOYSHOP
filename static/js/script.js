logincancel = document.querySelector(".login")
filterSort = document.querySelector(".filter-sort")


function syncInputs(changedInput) {
  const inputs = document.querySelectorAll('.quantity');
  inputs.forEach(input => {
      if (input !== changedInput) {
          input.value = changedInput.value;
      }
  });
}
// CART SCRITPS

function CancelLogin() {
  logincancel.classList.toggle("login-dn");
}

const swiper = new Swiper('#swiper1', {
  autoplay: {
    delay: 10000, // 10 sekund
    disableOnInteraction: false, // Interaktsiyalardan so'ng davom etishi uchun
  },

  // Optional parameters
  loop: true,

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next1',
    prevEl: '.swiper-button-prev1',
  },

});


var swiper2 = new Swiper('.swiper-container', {
  slidesPerView: 6,   // Bir vaqtning o'zida oltita slayd ko'rsatiladi
  spaceBetween: 10,   // Slaydlar orasidagi masofa (istalgan qiymatga o'zgartiring)
  loop: true,         // Cheksiz slayder
  autoplay: {
    delay: 0,
    disableOnInteraction: false, // Interaktsiyalardan so'ng davom etishi uchun
  },
  speed: 5000,
  breakpoints: {
    290: {            // Mobil ekranlar
      slidesPerView: 3, // Bir vaqtning o'zida 3 slayd
      spaceBetween: 10
    },
    500: {            // Kichik ekranlar
      slidesPerView: 4, // Bir vaqtning o'zida 4 slayd
      spaceBetween: 10
    },
    650: {            // O'rta ekranlar
      slidesPerView: 6, // Bir vaqtning o'zida 6 slayd
      spaceBetween: 20
    },
    1024: {           // Katta ekranlar
      slidesPerView: 8, // Bir vaqtning o'zida 8 slayd
      spaceBetween: 30
    }
  }

});



var swiper2 = new Swiper('#swipper3', {
  slidesPerView: 6,   // Bir vaqtning o'zida oltita slayd ko'rsatiladi
  spaceBetween: 10,   // Slaydlar orasidagi masofa (istalgan qiymatga o'zgartiring)
  loop: true,         // Cheksiz slayder
  autoplay: {
    delay: 1000,
    disableOnInteraction: false, // Interaktsiyalardan so'ng davom etishi uchun
  },
  speed: 1000,
  breakpoints: {

    1200: {
      slidesPerView: 4,
      spaceBetween: 10
    },
    950: {
      slidesPerView: 3,
    },
    600: {
      slidesPerView: 2,
    },
    250: {
      slidesPerView: 1,
      spaceBetween: 35

    },
  },

});





const stars = document.querySelectorAll('.star');
const intvale = document.querySelector('#ratingvalue');
stars.forEach(star => {
  star.addEventListener('click', () => {
    const rating = star.getAttribute('data-value');
    intvale.value = rating;
    highlightStars(rating);
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch("http://127.0.0.1:8000/rate-product/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({
        "product_id": intvale.getAttribute("data-product-id"),
        "rating": intvale.value
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showMessage(true,"Baholaganingiz uchun tashakkur!");
      } else {
        showMessage(false,data.error);
      }
    })
    .catch(error => {
      // Xato bo'lganda xabar ko'rsatamiz
      alert(error.message);
    });
  });
});

function highlightStars(rating) {
  const isAuthenticated  = document.querySelector('meta[name="isAuthenticated"]').getAttribute('content');
  if(isAuthenticated == "true"){
    stars.forEach(star => {
      if (star.getAttribute('data-value') <= rating) {
        star.style.color = 'gold';
      } else {
        star.style.color = 'lightgray';
      }
    });
  }
}


function focusToStart(input) {
  console.log(input)
  input.focus(); // Inputga fokusni o'rnatadi
  input.setSelectionRange(0, 0); // Kursorni inputning boshiga o'rnatadi
}


var swiperproduct = new Swiper(".mySwiper", {
  direction: 'vertical',
  loop: true,
  spaceBetween: 10,
  slidesPerView: 5,
  freeMode: true,
  watchSlidesProgress: true,
  
});
var swiperprocuct2 = new Swiper(".mySwiper2", {
  loop: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false, // Interaktsiyalardan so'ng davom etishi uchun
  },
  speed: 1000,
  spaceBetween: 10,
  initialSlide: 1  ,
  thumbs: {
    swiper: swiperproduct,
  },

  
});












class PriceRange extends HTMLElement {
  constructor() {
    super();
    console.log('Price Range: Constructor', this);
  }

  connectedCallback() {
    // Elements
    this.elements = {
      container: this.querySelector('.filter-container'),
      track: this.querySelector('.track'),
      from: this.querySelector('input[type="range"]:first-of-type'),
      to: this.querySelector('input[type="range"]:last-of-type'),
      output: this.querySelector('output'),
      minInput: this.querySelector('#min-price'),
      maxInput: this.querySelector('#max-price')
    };

    // Event listeners
    this.elements.from.addEventListener('input', this.handleInput.bind(this));
    this.elements.to.addEventListener('input', this.handleInput.bind(this));
    this.elements.minInput.addEventListener('input', this.handleManualInput.bind(this));
    this.elements.maxInput.addEventListener('input', this.handleManualInput.bind(this));

    // Properties
    this.currency = this.getAttribute('currency') || 'so\'m';
          
    // Update the DOM
    this.updateDom();

    console.log('Price Range: Connected', this);
  }

  handleManualInput() {
    // Minimal va maksimal qiymatlarni cheklash
    this.elements.minInput.value = Math.min(Math.max(0, parseInt(this.elements.minInput.value) || 0), 10000000);
    this.elements.maxInput.value = Math.min(Math.max(0, parseInt(this.elements.maxInput.value) || 0), 10000000);

    // 1-chi input qiymati 2-chisidan katta bo'lmasligi uchun tekshirish
    if (parseInt(this.elements.minInput.value) >= parseInt(this.elements.maxInput.value)) {
      this.elements.minInput.value = parseInt(this.elements.maxInput.value) - 1000;
    }

    // Range inputlarni manual input bilan yangilash
    this.elements.from.value = this.elements.minInput.value / 1000;
    this.elements.to.value = this.elements.maxInput.value / 1000;

    // DOM ni yangilash
    this.updateDom();
  }

  handleInput(event) {
    // Ikkinchi inputdan kichik bo'lishini ta'minlash
    if (parseInt(this.elements.from.value) >= parseInt(this.elements.to.value)) {
      if (event.target === this.elements.from) {
        this.elements.from.value = parseInt(this.elements.to.value) - 1;
      } else if (event.target === this.elements.to) {
        this.elements.to.value = parseInt(this.elements.from.value) + 1;
      }
    }

    // Min va Max inputlarni range qiymatlari bilan yangilash
    this.elements.minInput.value = this.elements.from.value * 1000;
    this.elements.maxInput.value = this.elements.to.value * 1000;

    // Update the DOM
    this.updateDom();
    
    console.log('Price Range: Updated!!', {
      from: parseInt(this.elements.from.value),
      to: parseInt(this.elements.to.value)
    });
  }

  updateDom() {
    this.drawFill();
    this.drawOutput();
  }

  drawFill() {
    const percent1 = (this.elements.from.value / this.elements.from.max) * 100,
          percent2 = (this.elements.to.value / this.elements.to.max) * 100;

    this.elements.track.style.background = `linear-gradient(to right, var(--track-color) ${percent1}%, var(--track-highlight-color) ${percent1}%, var(--track-highlight-color) ${percent2}%, var(--track-color) ${percent2}%)`;
  }

  drawOutput() {
    const minValue = this.elements.from.value * 1000;
    const maxValue = this.elements.to.value * 1000;
    this.elements.output.textContent = `${minValue} so'mdan - ${maxValue} so'mgacha`;
  }
}

customElements.define('price-range', PriceRange);



function ChangeRangeInput(element){
  document.getElementsByName('price-from').value = element.value
  console.log(document.getElementsByName('price-from').value)
  console.log(element.value)
}

nnactive = document.querySelector(".unactive")

function SortFilter(){
  filterSort.classList.toggle("filter-sort-activate");
  nnactive.classList.toggle("nnactive");
}




// GENDER TENGLASH
function setGender() {
  // Jinsni aniqlash
  const maleCheckbox = document.getElementById("maleCheckbox");
  const femaleCheckbox = document.getElementById("femaleCheckbox");
  const genderInput = document.getElementById("gender");

  if (maleCheckbox.checked) {
      genderInput.value = maleCheckbox.value; // Erkakni tanlanganda
  } else if (femaleCheckbox.checked) {
      genderInput.value = femaleCheckbox.value; // Ayolni tanlanganda
  } else {
      genderInput.value = ""; // Ikkalasi tanlanmagan bo'lsa, bo'sh qoldiring
  }
}


function changeValue(button, step) {
  const input = button.parentElement.querySelector('input'); // inputni olish
  const currentValue = parseInt(input.value);
  const minValue = parseInt(input.min);
  // Yangi qiymatni hisoblash
  const newValue = currentValue + step;
  
  // Agar yangi qiymat minimal qiymatdan (1) kichik bo'lmasa, inputni yangilash
  if (newValue >= minValue) {
    input.value = newValue;
    syncInputs(input)
  }
}

function validateInput(input) {
  const minValue = parseInt(input.min);
  // Agar foydalanuvchi kiritgan qiymat minimal qiymatdan (1) kichik bo'lsa, uni 1 ga o'zgartirish
  if (parseInt(input.value) < minValue) {
      input.value = minValue;
  }
}



function checkAll(mainCheckbox) {
  var checkboxes = document.querySelectorAll('.cartinput');
  checkboxes.forEach(function(checkbox) {
      checkbox.checked = mainCheckbox.checked;
  });
}




const toggle = document.getElementById('toggle');
const div1 = document.getElementById('div1');
const div2 = document.getElementById('div2');
const div3 = document.getElementById('div3');
const div4 = document.getElementById('div4');




function viewsorder(){
  div1.classList.add('visible');
  div2.classList.remove('visible'); 
  div3.classList.remove('visible'); 
  div4.classList.remove('visible'); 


}



function viewsorder2(){
  div1.classList.remove('visible');
  div2.classList.add('visible'); 
  div3.classList.remove('visible'); 
  div4.classList.remove('visible'); 
}



function viewsorder3(){
  div1.classList.remove('visible');
  div2.classList.remove('visible'); 
  div3.classList.add('visible'); 
  div4.classList.remove('visible'); 

}



function viewsorder4(){
  div1.classList.remove('visible');
  div2.classList.remove('visible'); 
  div3.classList.remove('visible'); 
  div4.classList.add('visible'); 
}



document.querySelector(".focus-btn").addEventListener("click", function() {
  // Class orqali inputni topib, unga fokus berish
  document.querySelector(".search-intput").focus();
});



const order1 = document.getElementById('order1');
const order2 = document.getElementById('order2');




function viewsorderproduct(){
  order1.classList.add('visible');
  order2.classList.remove('visible'); 
}



function viewsorderproduct2(){
  order1.classList.remove('visible');
  order2.classList.add('visible'); 
}











function toggleDiv(number) {
  var div = document.getElementById('orderproduct' + number);
  if (div.style.display === "none") {
      div.style.display = "block";
  } else {
      div.style.display = "none";
  }
}

function toggleDiv1(number) {
  var div = document.getElementById('orderproductnow' + number);
  if (div.style.display === "none") {
      div.style.display = "block";
  } else {
      div.style.display = "none";
  }
}


document.querySelector(".lasttext").querySelector("p").textContent = `«${new Date().getFullYear()}© «UzToysShop». Barcha huquqlar himoyalangan»`;  // Masalan, 2024-ni qaytaradi




if (window.location.hash === '#profile') {
  const inputs = document.getElementsByName('proder');
  inputs[0].checked = false; 
  inputs[1].checked = true;
  viewsorder2();
}

if (window.location.hash === '#locate') {
  const inputs = document.getElementsByName('proder');
  inputs[0].checked = false; 
  inputs[2].checked = true;
  viewsorder3();
}

function checkHashTag(){
  window.location.href = "/account/profile/#profile"
  if (window.location.hash === '#profile') {
    console.log('profil');
    const inputs = document.getElementsByName('proder');
    inputs[0].checked = false; 
    inputs[1].checked = true;
    viewsorder2();
  }
}
if (window.location.hash === "#login"){
  CancelLogin()
}








document.addEventListener('DOMContentLoaded', function() {
  const showDiv = document.getElementById('showDiv');
  const hideDiv = document.getElementById('hideDiv');
  const myDiv = document.getElementById('myDiv');

  function toggleDiv() {
    if (showDiv.checked) {
      myDiv.style.display = 'flex';
    } else if (hideDiv.checked) {
      myDiv.style.display = 'none';
    }
  }

  // Boshlang'ich holat
  toggleDiv();

  // Radio tugmalarga "change" hodisasini qo'shish
  showDiv.addEventListener('change', toggleDiv);
  hideDiv.addEventListener('change', toggleDiv);
});






const inputs = document.querySelectorAll('#myForm input[type="text"], #myForm input[type="email"], #myForm input[type="number"],#myForm input[type="url"],#myForm input[type="radio"]');
const saveButton = document.getElementById('saveButton');

inputs.forEach(input => {
  input.addEventListener('input', function() {
    saveButton.style.display = 'block'; // Input qiymati o'zgarganda tugmani ko'rsatish
  });
});

saveButton.addEventListener('click', function() {
  // Tugma bosilganda, "Saqlash" tugmasini yashirish
  saveButton.style.display = 'none';
  console.log('Ma\'lumotlar saqlandi!'); // Olingan ma'lumotlar saqlandi degan xabar
});





function showMessage(isSuccess,message) {
  var toast;
  if (isSuccess) {
      toast = document.getElementById("successToast");
      toast.className = "toast success show";
      toast.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`
      setTimeout(function() {
          toast.className = toast.className.replace("show", "");
      }, 2500); 
  } else {
      toast = document.getElementById("errorToast");
      toast.className = "toast error show";
      toast.innerHTML = `<i class="fas fa-times-circle"></i> ${message}`
      setTimeout(function() {
          toast.className = toast.className.replace("show", "");
      }, 2500);
  }
  
}





function getCheckedColor() {
  // Barcha `.myCheckbox` classiga ega inputlarni olish
  const radios = document.querySelectorAll('.myCheckbox');
  
  // Checked holatidagi inputni topish
  let selectedColor = null;
  radios.forEach(radio => {
      if (radio.checked) {
          selectedColor = radio.value;
      }
  });
  
  // Tanlangan rangni konsolga chiqarish
  if (selectedColor) {
    return selectedColor
  } else {
    return false
  }
}




function addToCart(button) {
  if(getCheckedColor()){
    productId = button.getAttribute('data-product-id')
    quantity = document.querySelector('.quantity')
    quantity = quantity && quantity.value ? parseInt(quantity.value) : 1;
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/cart/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken// CSRF token olish
        },
        body: JSON.stringify({
          "product_id": productId,
          "quantity": quantity,
          "color_id":parseInt(getCheckedColor()),
        })
    })
    .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
        showMessage(true,data.message)
        const notes = document.querySelectorAll('.note');
        console.log(notes)
        // Har bir 'note' elementi qiymatini o‘zgartirish
        notes.forEach((note) => {
            note.innerText = data.cart_count;
            note.style = "display:block;"
        });
    })
    .catch(error => console.error('Error:', error));
  }
  else{
    showMessage(false,"Hech qanday rang tanlanmagan")
  } 
}

function addToCartHome(button) {
    productId = button.getAttribute('data-product-id')
    quantity = 1
    quantity = quantity && quantity.value ? parseInt(quantity.value) : 1;
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/cart/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken// CSRF token olish
        },
        body: JSON.stringify({
          "product_id": productId,
          "quantity": quantity,
          "color_id":document.querySelector('.myCheckbox'+productId).value,
        })
    })
    .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
        showMessage(true,data.message)
        const notes = document.querySelectorAll('.note');
        console.log(notes)
        // Har bir 'note' elementi qiymatini o‘zgartirish
        notes.forEach((note) => {
            note.innerText = data.cart_count;
            note.style = "display:block;"
        });
    })
    .catch(error => console.error('Error:', error));
}

function removeFromCart(cartItemId) {
  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  fetch('/cart/remove-to-cart/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken // CSRF tokenni olish funksiyasi kerak bo'ladi
      },
      body: JSON.stringify({
          'cart_item_id': cartItemId
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          showMessage(true,data.message)
          document.getElementById(`cart-item-${cartItemId}`).remove();
          document.getElementById("total_price").innerText = `${data.total_price} so'm`
          document.getElementById("total_quantity").innerText = `Mahsulotlar (${data.total_quantity}):`
      }
  })
  .catch(error => console.error('Xatolik yuz berdi:', error));
}

function updateCartItemQuantity(cartItemId) {
  const quantityInput = document.getElementById(`quantity-input-${cartItemId}`);
  const newQuantity = quantityInput.value;  // Yangilangan miqdorni olish
  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  fetch('/cart/update-cart-item/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken  // CSRF tokenini olish funksiyasi kerak bo'ladi
      },
      body: JSON.stringify({
          'cart_item_id': cartItemId,
          'quantity': newQuantity,
      })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
        showMessage(true,data.message)
        document.getElementById("total_price").innerText = `${data.total_price} so'm`
        document.getElementById("total_quantity").innerText = `Mahsulotlar (${data.total_quantity}):`
      }
      else {
        showMessage(false,data.message);
      }
  })
  .catch(error => console.error('Xatolik yuz berdi:', error));
}


function enterAdress(button){
  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/cart/create_address/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken  // CSRF tokenini olish funksiyasi kerak bo'ladi
      },
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
        showMessage(true,data.message)
        localStorage.setItem('address_code', data.address_code);
        const href = `https://t.me/UzToysShopbot?start=${data.address_code}`;
        document.getElementById("myModal").style.display = "flex";
        document.querySelector(".locatation-url").href = href;
        
      }
  })
  .catch(error => console.error('Xatolik yuz berdi:', error));
}
function openModal() {
  document.getElementById("myModal").style.display = "flex";

}
function openInNewTabAndHide(element) {
  element.style.display = 'none';

  // Ota elementning ichki HTML-ni o'zgartirish
  element.parentElement.innerHTML = '<button type="button" onclick="CheckAddress()" style="width: 100%; margin: 10px 0;" class="locate-open-btn">Joylashuvni kiritdim</button>';

  // Konsolda ota elementni ko‘rsatish
  window.open(element.href, '_blank');

  // A tagini yashirish

  // Default link harakatini oldini olish
  return false;
}
// Modalni yopish funksiyasi
function closeModal() {
  document.getElementById("myModal").style.display = "none";
}
function CheckAddress(){
  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  const addressCode = localStorage.getItem('address_code');
    fetch('/cart/get_address/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken  // CSRF tokenini olish funksiyasi kerak bo'ladi
      },
      body: JSON.stringify({ address_code: addressCode })

  })
  .then(response => response.json())
  .then(data => {
      if (data.message == "Manzil muvaffaqiyatlik kiritildi") {
        showMessage(true,data.message)
        closeModal()
        locatebtn = document.querySelector('.locate-open-btn')
        locatebtn.style.display = 'none'
        locatebtn.parentElement.innerHTML = `<p class="inp-name">manzili<span>*</span></p><a target="_blank" href="https://www.google.com/maps/search/${data.latitude}+${data.longitude}"><button type="button" style="width: 100%;margin: 10px 0;pointer-events: none;" class="locate-open-btn">Manzil kiritilgan</button></a><input type="hidden" name="addressCode" value="addressCode"></input>`
        localStorage.setItem('checkAddress', true);
        const address_Input = document.createElement("input");
        address_Input.type = "hidden"; 
        address_Input.name = "address_code";
        address_Input.value = addressCode
      
        const form = document.getElementById("CreateOrder")
        form.appendChild(address_Input);
      }
      else{
        showMessage(false,data.message)
        if(data.message == "Manzil kiritilmagan! Iltmos manzilni kiriting"){
          // location-url klassiga ega barcha elementlarni topish
          const elements = document.querySelectorAll('.location-url');

          elements.forEach(element => {
              const parent = element.parentElement; // Ota elementni olish
              if (parent) {
                  parent.remove(); // Ota elementni o'chirish
              }
          });

          const href = `https://t.me/UzToysShopbot?start=${addressCode}`;
          const newDiv = document.createElement('div');
          newDiv.className = 'mt-4'; // Klass qo'shish
          newDiv.innerHTML = `<a class="locatation-url" href="${href}" target="_blank">Joylashuvni Kiritish</a>`; // Ichki HTMLni belgilash

          // .modal-content ichiga qo'shish
          const modalContent = document.querySelector('.modal-content');
          modalContent.insertBefore(newDiv, modalContent.lastChild);
        }
        localStorage.setItem('checkAddress', false);
      }
  })
  .catch(error => console.error('Xatolik yuz berdi:', error));
}
function crateOreder(event) {
  event.preventDefault();
  const formData = new FormData(document.getElementById("CreateOrder"));
  const addressCode = formData.get('address_code')
  console.log("Address code in localStorage:", addressCode);  // LocalStorage ma'lumotini tekshirish
  btn = document.querySelector('.create-order')
  console.log(btn)
  if (addressCode) {

      // Form ma'lumotlarini olish
      const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
      fetch('/cart/creat_order/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken  // CSRF tokenini qo'shish
        },
        body: formData  // FormData obyekti
    })
    .then(response => response.json())  // Serverdan javobni JSON formatida qabul qilish
    .then(data => {
        console.log("Response from server:", data);  // Serverdan kelgan javob // Yangi URLga yo'naltirish
        if(data.success == "Buyurtma tekshiruvga yuborildi"){
          window.location.href = "/account/profile/";
        }
        else{
          console.log(data.success)
          showMessage(false, data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);  // Xatolikni ko'rsatish
    });
      
  } else {
      showMessage(false, 'Iltimos, manzilni kiritganingizga ishonch hosil qiling!');
  }
}


// Modal oynasini tashqi qismini bosganda yopish
window.onclick = function(event) {
  var modal = document.getElementById("myModal");
  if (event.target == modal) {
      closeModal();
  }
}