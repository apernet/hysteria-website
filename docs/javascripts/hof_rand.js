document.addEventListener("DOMContentLoaded", function () {
    const heading = document.getElementById('hof-start');
    if (heading && heading.nextElementSibling.tagName === 'UL') {
        const list = heading.nextElementSibling;
        let items = Array.from(list.querySelectorAll('li'));
        for (let i = items.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i)) + 1; // Apernet should always stay at the top
            [items[i], items[j]] = [items[j], items[i]];
        }
        items.forEach(item => list.appendChild(item));
    }
});
