document.addEventListener('DOMContentLoaded', () => {
  const carrosseis = document.querySelectorAll('.carrossel');

  carrosseis.forEach(carrossel => {
    const main = carrossel.querySelector('.carrossel__main');
    const btnPrev = carrossel.querySelector('.carrossel-btn.prev');
    const btnNext = carrossel.querySelector('.carrossel-btn.next');

    let isDown = false;
    let startX;
    let scrollLeft;

    // --- Drag com mouse ---
    main.addEventListener('mousedown', (e) => {
      isDown = true;
      main.style.cursor = 'grabbing';
      startX = e.pageX - main.offsetLeft;
      scrollLeft = main.scrollLeft;
    });

    main.addEventListener('mouseleave', () => {
      isDown = false;
      main.style.cursor = 'grab';
    });

    main.addEventListener('mouseup', () => {
      isDown = false;
      main.style.cursor = 'grab';
    });

    main.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - main.offsetLeft;
      const walk = (x - startX) * 2;
      main.scrollLeft = scrollLeft - walk;
    });

    // --- Touch no mobile ---
    main.addEventListener('touchstart', (e) => {
      isDown = true;
      startX = e.touches[0].pageX - main.offsetLeft;
      scrollLeft = main.scrollLeft;
    });

    main.addEventListener('touchend', () => {
      isDown = false;
    });

    main.addEventListener('touchmove', (e) => {
      if (!isDown) return;
      const x = e.touches[0].pageX - main.offsetLeft;
      const walk = (x - startX) * 2;
      main.scrollLeft = scrollLeft - walk;
    });

    // --- Botões prev/next ---
    const scrollAmount = 200; // ajuste conforme o tamanho dos cards

    if (btnPrev && btnNext) {
      btnPrev.addEventListener('click', () => {
        main.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
      });

      btnNext.addEventListener('click', () => {
        main.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      });
    }
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

/* favorita todos os filmes dentro de um classe chamada .filme--nome */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".filme--nome .fav-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const card = btn.closest(".filme--nome");
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

/* favorita todos os atores dentro de um classe chamada .cast-card */
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

/* favorita todos os atores dentro de um classe chamada .ator--nome */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".ator--nome .fav-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const card = btn.closest(".ator--nome");
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

document.getElementById("abrirForm").addEventListener("click", function() {
        document.getElementById("formSalvar").style.display = "block";
        this.style.display = "none"; // esconde o botão depois de abrir o form
    });

    function setStatus(status) {
        document.getElementById("statusInput").value = status;
    }