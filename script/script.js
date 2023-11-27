document.addEventListener("DOMContentLoaded", function () {
    const controls = document.querySelectorAll('.prev, .next');

    controls.forEach(control => {
        control.addEventListener('click', function handleClick(event) {
            if (control.classList.contains('prev')) {
                move(event.target, 'left');
            } else {
                move(event.target, 'right')
            }
        });
    });

    const controls2 = document.querySelectorAll('.start, .end');

    controls2.forEach(control => {
        control.addEventListener('click', function handleClick(event) {
            if (control.classList.contains('start')) {
                move(event.target, 'left', 0);
            } else {
                move(event.target, 'right', 999999999)
            }
        });
    });
});

const move = (control, direction, coord = false) => {
    carousel = control.parentElement.parentElement.querySelector('.carousel')

    if (coord !== false) {
        carousel.scroll(coord, 0)
    } else {
        if (direction == 'left') {
            carousel.scrollLeft -= 400
        } else {
            carousel.scrollLeft += 400
        }
    }
}