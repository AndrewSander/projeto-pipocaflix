document.addEventListener('DOMContentLoaded', () => {
  const carrossel = document.querySelector('.carrossel');
  let isDown = false;
  let startX;
  let scrollLeft;

  carrossel.addEventListener('mousedown', (e) => {
    isDown = true;
    carrossel.style.cursor = 'grabbing';
    startX = e.pageX - carrossel.offsetLeft;
    scrollLeft = carrossel.scrollLeft;
  });

  carrossel.addEventListener('mouseleave', () => {
    isDown = false;
    carrossel.style.cursor = 'grab';
  });

  carrossel.addEventListener('mouseup', () => {
    isDown = false;
    carrossel.style.cursor = 'grab';
  });

  carrossel.addEventListener('mousemove', (e) => {
    if(!isDown) return;
    e.preventDefault();
    const x = e.pageX - carrossel.offsetLeft;
    const walk = (x - startX) * 2; 
    carrossel.scrollLeft = scrollLeft - walk;
  });

  carrossel.addEventListener('touchstart', (e) => {
    isDown = true;
    startX = e.touches[0].pageX - carrossel.offsetLeft;
    scrollLeft = carrossel.scrollLeft;
  });

  carrossel.addEventListener('touchend', () => {
    isDown = false;
  });

  carrossel.addEventListener('touchmove', (e) => {
    if(!isDown) return;
    const x = e.touches[0].pageX - carrossel.offsetLeft;
    const walk = (x - startX) * 2;
    carrossel.scrollLeft = scrollLeft - walk;
  });
});

function toggleMenu() {
  document.getElementById("perfilMenu").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.perfil-icone')) {
    let menu = document.getElementById("perfilMenu");
    if (menu.classList.contains("show")) {
      menu.classList.remove("show");
    }
  }
}

/* favorita todos os filmes dentro de um classe chamada .filme-card */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".filme-card .fav-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const card = btn.closest(".filme-card");
      const filmeId = card.getAttribute("data-filme-id");

      try {
        const resp = await fetch("/favoritos/filmes/toggle", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filme_id: filmeId })
        });

        const data = await resp.json();
        if (data.favoritado) {
          btn.classList.add("is-active");
        } else {
          btn.classList.remove("is-active");
        }
      } catch (err) {
        console.error("Erro ao favoritar:", err);
      }
    });
  });
});

/* favorita todos os filmes dentro de um classe chamada .banner__info */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".banner__info .fav-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const card = btn.closest(".banner__info");
      const filmeId = card.getAttribute("data-filme-id");

      try {
        const resp = await fetch("/favoritos/filmes/toggle", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filme_id: filmeId })
        });

        const data = await resp.json();
        if (data.favoritado) {
          btn.classList.add("is-active");
        } else {
          btn.classList.remove("is-active");
        }
      } catch (err) {
        console.error("Erro ao favoritar:", err);
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".cast-card .fav-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const card = btn.closest(".cast-card");
      const atorId = card.getAttribute("data-ator-id");

      try {
        const resp = await fetch("/favoritos/atores/toggle", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ator_id: atorId })
        });

        const data = await resp.json();
        if (data.favoritado) {
          btn.classList.add("is-active");
        } else {
          btn.classList.remove("is-active");
        }
      } catch (err) {
        console.error("Erro ao favoritar:", err);
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('.perfil-nav');
  let isDown = false;
  let startX;
  let scrollLeft;

  nav.addEventListener('mousedown', (e) => {
    isDown = true;
    nav.style.cursor = 'grabbing';
    startX = e.pageX - nav.offsetLeft;
    scrollLeft = nav.scrollLeft;
    e.preventDefault(); // previne seleção de texto e scroll da página
  });

  nav.addEventListener('mouseup', () => isDown = false);
  nav.addEventListener('mouseleave', () => isDown = false);

  nav.addEventListener('mousemove', (e) => {
    if(!isDown) return;
    e.preventDefault();
    const x = e.pageX - nav.offsetLeft;
    const walk = x - startX; // velocidade natural
    nav.scrollLeft = scrollLeft - walk;
  });

  // Touch
  nav.addEventListener('touchstart', (e) => {
    isDown = true;
    startX = e.touches[0].pageX - nav.offsetLeft;
    scrollLeft = nav.scrollLeft;
  });

  nav.addEventListener('touchmove', (e) => {
    if(!isDown) return;
    e.preventDefault(); // evita scroll da página
    const x = e.touches[0].pageX - nav.offsetLeft;
    const walk = x - startX;
    nav.scrollLeft = scrollLeft - walk;
  });

  nav.addEventListener('touchend', () => isDown = false);
});

document.addEventListener('DOMContentLoaded', () => {

  // Encontra os botões e o menu no HTML
  const botaoAbrir = document.querySelector(".header__menu");
  const botaoFechar = document.querySelector(".btn-fechar");
  const menu = document.querySelector(".menu-lateral");

  // Adiciona a função de clique no botão de abrir
  botaoAbrir.addEventListener("click", () => {
    menu.classList.add("aberto"); // Mostra o menu
  });

  // Adiciona a função de clique no botão de fechar
  botaoFechar.addEventListener("click", () => {
    menu.classList.remove("aberto"); // Esconde o menu
  });
});

const btn = document.querySelector(".button-avaliar");
const box = document.querySelector(".janela-avaliacao");

btn.addEventListener("click", () => {
  box.classList.toggle("show");

  if (box.classList.contains("show")) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "";       
  }
});

const btn_fechar = document.querySelector(".fechar-janela");

btn_fechar.addEventListener("click", () => {
  box.classList.remove("show");
  document.body.style.overflow = "";
})
