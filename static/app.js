const API = "http://127.0.0.1:8000";

async function api(url, options = {}) {
    const res = await fetch(API + url, {
    headers: { "Content-Type": "application/json"},
    ...options,
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Request failed");
    }
    return res.json();
}

async function loadProducts() {
    const products = await api("/products/");
    const list = document.getElementById("product-list");
    if (products.length === 0) {
        list.innerHTML = "<p>Товаров пока нет</p>";
        return;
    }
    list.innerHTML = "<ul>" + products.map(p =>
        `<li>${p.name} (${p.url}) — id: ${p.id}</li>`
    ).join("") + "</ul>";

    fillSelect("alert-product", products);
    fillSelect("history-product", products);
}

function fillSelect(selectId, products) {
    const select = document.getElementById(selectId);
    select.innerHTML = '<option value="">Выберите товар</option>' +
        products.map(p => `<option value="${p.id}">${p.name}</option>`).join("");
}

async function init() {
    document.getElementById("product-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("product-name").value;
        const symbol = document.getElementById("product-symbol").value.trim().toLowerCase();
        try {
            await api("/products/", {
                method: "POST",
                body: JSON.stringify({ name: name, url: symbol }),
            });
            document.getElementById("product-form").reset();
            await loadProducts();
        } catch (err) {
            alert(err.message);
        }
    });

    document.getElementById("alert-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const product_id = Number(document.getElementById("alert-product").value);
        const email = document.getElementById("alert-email").value;
        const target_price = Number(document.getElementById("alert-target").value);
        try {
            await api("/alerts/", {
                method: "POST",
                body: JSON.stringify({ product_id, email, target_price }),
            });
            document.getElementById("alert-form").reset();
        } catch (err) {
            alert(err.message);
        }
    });

    await loadProducts();
}

init();

async function loadHistory() {
    const productId = document.getElementById("history-product").value;
    const canvas = document.getElementById("price-chart");
    const ctx = canvas.getContext("2d");

    if (!productId) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        return;
    }

    const history = await api(`/history/?product_id=${productId}`);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const prices = history.map(h => h.price);
    if (prices.length === 0) return;

    const min = Math.min(...prices);
    const max = Math.max(...prices);

    const width = canvas.width;
    const height = canvas.height;
    const padding = 30;

    // Координаты точек
    const points = history.map((h, i) => {
        const x = padding + (i / (prices.length - 1 || 1)) * (width - 2 * padding);
        const y = height - padding - ((h.price - min) / (max - min || 1)) * (height - 2 * padding);
        return { x, y };
    });

    // Линия
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.strokeStyle = "#28a745";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Надписи минимума и максимума
    ctx.fillStyle = "#333";
    ctx.font = "12px Arial";
    ctx.fillText(`max ${max.toFixed(2)}`, padding, padding - 5);
    ctx.fillText(`min ${min.toFixed(2)}`, padding, height - padding + 15);
}

document.getElementById("history-product").addEventListener("change", loadHistory);
