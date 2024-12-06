logincancel = document.querySelector(".login")
filterSort = document.querySelector(".filter-sort")

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

stars.forEach(star => {
  star.addEventListener('click', () => {
    const rating = star.getAttribute('data-value');
    highlightStars(rating);
  });
});

function highlightStars(rating) {
  stars.forEach(star => {
    if (star.getAttribute('data-value') <= rating) {
      star.style.color = 'gold';
    } else {
      star.style.color = 'lightgray';
    }
  });
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
      container: this.querySelector('div'),
      track: this.querySelector('div > div'),
      from: this.querySelector('input:first-of-type'),
      to: this.querySelector('input:last-of-type'),
      output: this.querySelector('output')
    }

    // Event listeners
    this.elements.from.addEventListener('input', this.handleInput.bind(this));
    this.elements.to.addEventListener('input', this.handleInput.bind(this));

    // Properties
    this.currency = (this.hasAttribute('currency') &&
                     this.getAttribute('currency') !== undefined &&
                     this.getAttribute('currency') !== '') ? this.getAttribute('currency') : '£';
          
    // Update the DOM
    this.updateDom();

    console.log('Price Range: Connected', this);
  }

  disconnectedCallback() {
    delete this.elements;
    delete this.currency;

    console.log('Price Range: Disconnected', this);
  }
  
  get from() {
    return parseInt(this.elements.from.value);
  }
  get to() {
    return parseInt(this.elements.to.value);
  }
  
  handleInput(event) {
    if (parseInt(this.elements.to.value) - parseInt(this.elements.from.value) <= 1) {
      if (event.target === this.elements.from) {
        this.elements.from.value = (parseInt(this.elements.to.value) - 1);
      } else if (event.target === this.elements.to) {
        this.elements.to.value = (parseInt(this.elements.from.value) + 1);
      }
    }

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
    this.elements.output.textContent = `${this.elements.from.value}000 so'mdan - ${this.elements.to.value}000 so'mgacha`;
  }
}

customElements.define('price-range', PriceRange);




nnactive = document.querySelector(".unactive")

function SortFilter(){
  filterSort.classList.toggle("filter-sort-activate");
  nnactive.classList.toggle("nnactive");
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













function addToCart(isSuccess) {
  var toast;
  if (isSuccess) {
      toast = document.getElementById("successToast");
      toast.className = "toast success show";
      setTimeout(function() {
          toast.className = toast.className.replace("show", "");
      }, 2500); 
  } else {
      toast = document.getElementById("errorToast");
      toast.className = "toast error show";
      setTimeout(function() {
          toast.className = toast.className.replace("show", "");
      }, 2500);
  }
  
}





