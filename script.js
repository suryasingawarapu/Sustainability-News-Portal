const newsContainer = document.getElementById("news-container");

fetch("http://127.0.0.1:8000/news")
  .then(response => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
  })
  .then(data => {
      newsContainer.innerHTML = "";
      data.forEach(item => {
          const card = document.createElement("div");
          card.className = "news-card";
          card.innerHTML = `
            <h2>${item.title}</h2>
            <p><strong>Source:</strong> ${item.source}</p>
            <p>${item.summary}</p>
            <p><em>${item.published_at}</em></p>
            <a href="${item.link || '#'}" target="_blank">Read more</a>
          `;
          newsContainer.appendChild(card);
      });
  })
  .catch(err => {
      console.error(err);
      newsContainer.innerHTML = "Error loading news.";
  });
