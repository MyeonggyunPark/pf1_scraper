
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

  return true; // form 제출 계속 진행
}
