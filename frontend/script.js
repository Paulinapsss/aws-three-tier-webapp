const apiBaseUrl = "https://aev2kxuy99.execute-api.eu-north-1.amazonaws.com/prod"; 
let currentBook = null;

// Search for a book
async function searchBook() {
  const title = document.getElementById("bookTitle").value;

  try {
    const response = await fetch(`${apiBaseUrl}/books?title=${encodeURIComponent(title)}`);
    const data = await response.json();

    if (response.ok) {
      currentBook = data;
      document.getElementById("results").innerHTML = `
        <h3>${data.Title}</h3>
        <p><strong>Author:</strong> ${data.Author}</p>
        <p><strong>Description:</strong> ${data.Description}</p>
      `;
      document.getElementById("translation").innerHTML = "";
    } else {
      document.getElementById("results").innerHTML = `<p>${data.message}</p>`;
    }
  } catch (error) {
    console.error("Error fetching book:", error);
    document.getElementById("results").innerHTML = `<p>Something went wrong. Please try again.</p>`;
  }
}

// Translate description
async function translateDescription() {
  if (!currentBook) {
    alert("Search for a book first!");
    return;
  }

  const targetLang = document.getElementById("language").value;

  try {
    const response = await fetch(`${apiBaseUrl}/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: currentBook.Description,
        targetLang: targetLang
      })
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("translation").innerHTML = `
        <p><strong>Translated description:</strong></p>
        <p>${data.translatedText}</p>
      `;
    } else {
      document.getElementById("translation").innerHTML = `<p>${data.message}</p>`;
    }
  } catch (error) {
    console.error("Error translating:", error);
    document.getElementById("translation").innerHTML = `<p>Translation failed.</p>`;
  }
}

