const giftsContainer = document.getElementById("gifts-body");

async function loadGifts() {
    const response = await fetch('/gifts');
    const gifts = await response.json();
    
    giftsContainer.innerHTML = '';
    gifts.forEach(gift => {
        const item = document.createElement("tr");
        const nameCell = document.createElement('td');
        nameCell.className = 'table-body';
        nameCell.textContent = gift.name;
        const giftCell = document.createElement('td');
        giftCell.className = 'table-body';
        giftCell.textContent = gift.gift;
        item.appendChild(nameCell);
        item.appendChild(giftCell);
        giftsContainer.appendChild(item);
    });
}

loadGifts();