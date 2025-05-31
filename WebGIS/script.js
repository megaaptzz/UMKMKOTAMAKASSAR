document.addEventListener("DOMContentLoaded", function () {
    // Cari elemen map di halaman
    const mapContainer = document.getElementById("map");

    if (mapContainer) {
        // Buat elemen iframe
        const iframe = document.createElement("iframe");

        // Tentukan sumber file HTML interaktif
        iframe.src = "./interactive_hotspot_map_with_ratings_combined.html"; // Sesuaikan path file

        // Tambahkan atribut dan gaya iframe
        iframe.style.width = "100%";
        iframe.style.height = "100%";
        iframe.style.border = "none";
        iframe.style.borderRadius = "10px";
        iframe.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";

        // Tambahkan iframe ke dalam elemen map
        mapContainer.appendChild(iframe);

        console.log("Peta interaktif berhasil dimuat!");
    } else {
        console.error("Elemen #map tidak ditemukan di halaman.");
    }
});
