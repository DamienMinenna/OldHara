window.addEventListener('DOMContentLoaded', (event) => {
    console.log('coucou')
    document.querySelectorAll('.scroll-reveal-item').forEach(function (item) {
        console.log('setting listner on ', item)
        item.addEventListener('scroll', testScrollPosition(item))

    });
});


function testScrollPosition(item) {
    console.log('testing screen pos', item.getBoundingClientRect().y)
    if (item.getBoundingClientRect().y < 50) {
        item.classList.add('scroll-revealed')
    } else {
        item.classList.remove('scroll-revealed')
    }
}