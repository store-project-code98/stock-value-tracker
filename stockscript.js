document.getElementById("searchForm").addEventListener("submit", function(event) {
    event.preventDefault();  
    let query = document.getElementById("searchInput").value.trim();

    if (query) {
        window.location.href = "/?s=" + encodeURIComponent(query);
    } 
});

let urlParams = new URLSearchParams(window.location.search);
document.getElementById('searchQuery').innerText = "View Stock Prices Live!"; 
let searchQuery = urlParams.get('s');
if (searchQuery)
    document.getElementById('searchQuery').innerText = decodeURIComponent(searchQuery).replace(/%20/g, ' ');
// } else {
//     document.getElementById('searchQuery').innerText = "Search For Your Stock!";
// }
