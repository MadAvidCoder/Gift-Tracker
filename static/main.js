const form = document.getElementById("giftForm")

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const name = form.elements.name.value;
    const gift = form.elements.gift.value;

    await fetch('/gifts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, gift })
    });

    form.reset();
    await alert("Gift submitted successfully!");
});