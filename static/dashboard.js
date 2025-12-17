const giftsContainer = document.getElementById("gifts-body");

async function loadGifts() {
    const response = await fetch('/gifts');
    const gifts = await response.json();
    
    giftsContainer.innerHTML = '';
    gifts.forEach(gift => {
        const item = document.createElement("tr");
        item.innerHTML = `<td class="table-body">${gift.name}</td><td class="table-body">${gift.gift}</td>`;
        giftsContainer.appendChild(item);
    });
}

loadGifts();