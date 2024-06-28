document.addEventListener('DOMContentLoaded', () => {
    const listOfServers = document.getElementById('listOfServers');
    if (listOfServers) {
        const links = listOfServers.getElementsByTagName('a');
        for (let i = links.length - 1; i >= 0; i--) {
            const link = links[i];
            const href = link.getAttribute('href');
            if (!href || href === '#' || href === 'null' || href.includes('{{ data[')) {
                link.parentNode.remove();
            }
        }
    }
});

// Add this function for posts page
function filterPosts() {
    const input = document.getElementById('searchBar');
    const filter = input.value.toLowerCase();
    const grid = document.getElementById("postsGrid");
    const items = grid.getElementsByClassName('grid-item');

    for (let item of items) {
        const text = item.textContent || item.innerText;
        item.style.display = text.toLowerCase().includes(filter) ? "" : "none";
    }
}