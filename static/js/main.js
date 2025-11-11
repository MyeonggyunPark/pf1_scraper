// Show loading animation by hiding search text and displaying loading indicator
function showLoading() {
  const cards = document.querySelectorAll("article");

  cards.forEach((card) => {
    const searchText = card.querySelector("#searchtext");
    const loading = card.querySelector("#loading");

    if (searchText && loading) {
      searchText.classList.add("hidden");
      loading.classList.remove("hidden");
    }
  });

  return true;
}

// Define available sites with their labels and values
document.addEventListener("DOMContentLoaded", function () {
  const sites = [
    { value: "bsj", label: "berlinstartupjobs.com" },
    { value: "wwr", label: "weworkremotely.com" },
    { value: "ssd", label: "stepstone.de" },
  ];

  // Get the toggle button element by ID
  const button = document.getElementById("siteToggleBtn");

  // Exit if the button does not exist
  if (!button) return;

  // Read URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const keyword = urlParams.get("keyword");
  const currentSiteValue = urlParams.get("site") || "bsj";

  // Find the index of the current site
  let currentIndex = sites.findIndex((site) => site.value === currentSiteValue);
  if (currentIndex === -1) currentIndex = 0;

  // Set the initial button text
  button.textContent = sites[currentIndex].label;

  // Handle button click to cycle through sites
  button.addEventListener("click", () => {
    // Move to the next site in the list
    currentIndex = (currentIndex + 1) % sites.length;
    const nextSite = sites[currentIndex];

    // Generate a new URL with the updated site
    const newURL = `/result?keyword=${encodeURIComponent(keyword)}&site=${
      nextSite.value
    }`;

    // Redirect to the new result page
    window.location.href = newURL;
  });
});
