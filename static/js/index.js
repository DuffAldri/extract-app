const navElement = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.nav-link, .nav-button, #logo');
const navbarHeight = document.querySelector('.navbar').offsetHeight; 

window.addEventListener('scroll', () => {
    if(window.scrollY > navbarHeight) {
        navElement.classList.add('scrolled');
        navElement.classList.remove('text-white');
        navElement.classList.add('text-purple');
        navLinks.forEach(link => {
            link.classList.remove('text-white');
            link.classList.add('text-purple');
        });
    } else {
        navElement.classList.remove('scrolled');
        navElement.classList.remove('text-purple');
        navElement.classList.add('text-white');
        navLinks.forEach(link => {
            link.classList.remove('text-purple');
            link.classList.add('text-white');
        });
    }
});

// document.getElementById('nav-ekstraksi').onclick = () => { 
//     document.getElementById('ekstraksi-section').scrollIntoView({ behavior: 'smooth' });
// }


// document.getElementById('nav-tentang').onclick = () => { 
//     document.getElementById('tentang-section').scrollIntoView({ behavior: 'smooth' });
// }

// document.getElementById('nav-').onclick = () => { 
//     document.getElementById('tentang-section').scrollIntoView({ behavior: 'smooth' });
// }

// console.log(navbarHeight);

// scrollFromTo('nav-tentang', '#tentang-section');
// function scrollFromTo(from_id, to_id, offset ) {
//     const fromElement = document.getElementById(from_id);

//     console.log('From id:', from_id);
//     console.log('From element:', fromElement);

//     fromElement.addEventListener("click", () => {
//         const targetElement = document.getElementById(to_id);
//         const elementPosition = targetElement.getBoundingClientRect().top; // Posisi elemen terhadap viewport
//         const offsetPosition = elementPosition + window.scrollY - offset; // Hitung posisi dengan offset

//         window.scrollTo({
//             top: offsetPosition,
//             behavior: 'smooth'
//         });

//         console.log('scroll')
//     }
// )};
// scrollFromTo('nav-beranda', '#hero-section', 0);
// scrollFromTo('nav-ekstraksi', '#ekstraksi-section',72);
// scrollFromTo('nav-kontributor', '#kontributor-section');
