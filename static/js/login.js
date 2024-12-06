const phoneInput = document.getElementById("phone");
const errorMessage = document.getElementById("error-message");
const logincancel = document.querySelector(".login")
const smslogin = document.querySelector(".codelogin")
let userId;


// Telefon raqamining formatlash va O'zbekiston raqamiga mosligini tekshirish
phoneInput.addEventListener("input", function (e) {
  let input = e.target.value.replace(/\D/g, ""); // Faqat raqamlarni olib qolamiz

  // +998 ni saqlab qolish
  if (input.startsWith("998")) {
    input = input.substring(3); // 998 ni olib tashlaymiz
  }

  // Formatlash
  let formattedNumber = "+998";
  if (input.length > 0) {
    formattedNumber += " (" + input.substring(0, 2); // 90-99 kodlar uchun
  }
  if (input.length >= 3) {
    formattedNumber += ") " + input.substring(2, 5);
  }
  if (input.length >= 6) {
    formattedNumber += "-" + input.substring(5, 7);
  }
  if (input.length >= 8) {
    formattedNumber += "-" + input.substring(7, 9);
  }

  // Inputni yangilash
  e.target.value = formattedNumber;

  // Xatoni yashirish (to'g'ri format kiritilganda)
  errorMessage.style.display = "none";
});

// O'zbekiston raqamini tekshirish funksiyasi
function validateUzbekNumber() {
  const phoneValue = phoneInput.value.replace(/\D/g, ""); // Faqat raqamlarni saqlaymiz

  // Agar maydon bo'sh bo'lsa
  if (phoneInput.value === "+998" || phoneInput.value.trim() === "") {
    errorMessage.style.display = "block";
    errorMessage.textContent = "Iltimos, nomeringizni kiriting!";
    return false;
  }

  // O'zbekiston raqamiga mos keladigan pattern
  const uzbekNumberPattern = /^998[0-9]{9}$/;

  // O'zbekiston raqamiga mos emas
  if (!uzbekNumberPattern.test(phoneValue)) {
    // Xato xabarini chiqarish
    errorMessage.style.display = "block";
    errorMessage.textContent =
      "Iltimos, to'g'ri O'zbekiston raqamini kiriting!";
    return false; // Forma yuborilmasin
  }
  logincancel.classList.toggle("login-dn")
  smslogin.querySelector("div strong").innerText = formatPhoneNumber(phoneValue)
  submitForm(phoneValue)
  smslogin.classList.toggle("login-dn")
  return true; // Forma yuborilsin
}
function formatPhoneNumber(phoneNumber) {
  // Telefon raqamini formatlash
  return `+${phoneNumber.slice(0, 3)} ${phoneNumber.slice(3, 5)} ${phoneNumber.slice(5, 8)} ${phoneNumber.slice(8, 10)} ${phoneNumber.slice(10)}`;
}
function formatPhoneNumber2(input) {
  // Telefon raqamini tozalash
  return input.replace(/\D/g, ''); // Faqat raqamlarni olib, qolganlarini o'chirib tashlaydi
}
function submitForm(phoneNumber) {
  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  fetch('/account/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken // JSON formatida yuborish
      },
      body: JSON.stringify({ phone_number: phoneNumber }) // JSON formatida yuboriladigan ma'lumot
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json(); // Javobni JSON formatida o'qish
  })
  .then(data => {
      console.log('Success:', data); // Muvaffaqiyatli javob
      userId = data.user_id;
      form = smslogin.querySelector("div")
      form.setAttribute("action", form.getAttribute("action").replace(/\/0\/$/, `/${userId}/`))
      console.log(form.getAttribute("action"))

  })
  .catch((error) => {
      console.error('Error:', error); // Xatolik yuzaga keldi
  });
}
phoneInput.addEventListener("keydown", function (e) {
  // Agar foydalanuvchi +998 qismini o'chirishga harakat qilsa, to'xtatish
  if (e.key === "Backspace" && phoneInput.value.length <= 5) {
    e.preventDefault();
  }
});
// DOM elementlarini olish
const sendButton = document.getElementById('sendButton');
const timerElement = document.getElementById('timer');
const codeInput = document.getElementById('code');
const errorMessage1 = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');

let countdown = 60; // 60 soniya
let correctCode = "123456"; // To'g'ri kod (namuna sifatida)
let timer; // Timerni ushlab turish uchun o'zgaruvchi

// Timerni ishga tushirish
function startTimer() {
    countdown = 60; // Har safar qayta boshlash uchun 60 ga qaytarish
    timerElement.innerText = `Agar kod kelmasa, siz  ${countdown} soniya orqali yangisini olishingiz mumkin`;

    // Timer ishlashini ta'minlash
    timer = setInterval(() => {
        countdown--;
        timerElement.innerText = `Agar kod kelmasa, siz  ${countdown} soniya orqali yangisini olishingiz mumkin`;
        
        if (countdown <= 0) {
            clearInterval(timer);
            timerElement.innerText = '';
            switchToResendButton(); // Tugmani "Qayta jo'natish" ga o'zgartirish
        }
    }, 1000);
}

// Jo'natish tugmasini "Qayta jo'natish" ga o'zgartirish
function switchToResendButton() {
    sendButton.innerText = "Qayta jo'natish"; // Tugma matni o'zgaradi
    sendButton.classList.add('disabled');
    sendButton.removeEventListener('click', checkCode);
    sendButton.addEventListener('click', resendCode);
}

// Kodni tekshirish funksiyasi
function checkCode() {
    const enteredCode = codeInput.value;
    console.log(enteredCode)
    form = smslogin.querySelector("div")
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(form.getAttribute("action"), {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded', // yoki 'application/json' agar JSON yuborayotgan bo'lsangiz
          'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ verification_code: enteredCode }) // JSON formatida yuboriladigan ma'lumot

  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.text(); // Yana HTML yoki JSON bo'lishi mumkin
  })
  .then(data => {
      console.log(data) // Javobni ko'
      if (data == "Tasdiqlash muvaffaqiyatli amalga oshirildi!") {
        errorMessage1.style.display = 'none'; // Xato xabar yashiriladi
        successMessage.style.display = 'block'; // To'g'ri xabar ko'rsatiladi
        window.location.href = "/account/profile#profile";
    } else {
        successMessage.style.display = 'none'; // To'g'ri xabar yashiriladi
        errorMessage1.style.display = 'block'; // Xato xabar ko'rsatiladi
    }
  })
  .catch((error) => {
      console.error('Xatolik:', error);
  });
}

// Qayta kod jo'natish funksiyasi
function resendCode() {
    // Kod qayta jo'natilganda xabarni interfeysda ko'rsatish
    submitForm(formatPhoneNumber2(smslogin.querySelector("div strong").innerText))
    successMessage.style.display = 'none';
    errorMessage1.style.display = 'none';
    sendButton.innerText = "Jo'natish";
    sendButton.classList.remove('disabled');
    sendButton.removeEventListener('click', resendCode);
    sendButton.addEventListener('click', checkCode);
    startTimer(); // Timer qayta boshlanadi
}

// Jo'natish tugmasiga bosilganda
sendButton.addEventListener('click', checkCode);

// Boshlanishida timerni ishga tushirish
startTimer();
