
fetch('../music')
    .then(result => {
        return result.json();
    })
    .then(data => {
        const dados = data;
        console.log(dados);
        let musica = document.querySelector('audio');
        let indexMusica = 0;

        let duracaoMusica = document.querySelector('.fim');
        let imagem = document.querySelector('img');
        let nomeMusica = document.querySelector('.descricao h2');
        let nomeArtista = document.querySelector('.descricao i');

        renderizarMusica(indexMusica);

        document.querySelector('i.botao-play').addEventListener('click', tocarMusica);

        document.querySelector('i.botao-pause').addEventListener('click', pausarMusica);

        musica.addEventListener('timeupdate', atualizarBarra);

        document.querySelector('i.anterior').addEventListener('click', () => {
            indexMusica--;
            if (indexMusica < 0) {
                indexMusica = 2;
            }
            renderizarMusica(indexMusica);
        });

        document.querySelector('.proxima').addEventListener('click', () => {
            indexMusica++;
            if (indexMusica > 2) {
                indexMusica = 0;
            }
            renderizarMusica(indexMusica);
        });

        function renderizarMusica(index) {
            musica.setAttribute('src', data[index].src);
            musica.addEventListener('loadeddata', () => {
                nomeMusica.textContent = data[index].titulo;
                nomeArtista.textContent = data[index].artista;
                imagem.src = data[index].img;
                duracaoMusica.textContent = segundosParaMinutos(Math.floor(musica.duration));
            });
        }

        function tocarMusica() {
            musica.play();
            document.querySelector('.botao-pause').style.display = 'block';
            document.querySelector('.botao-play').style.display = 'none';
        }

        function pausarMusica() {
            musica.pause();
            document.querySelector('.botao-pause').style.display = 'none';
            document.querySelector('.botao-play').style.display = 'block';
        }

        function atualizarBarra() {
            let barra = document.querySelector('progress');
            barra.style.width = Math.floor((musica.currentTime / musica.duration) * 100) + '%';
            let tempoDecorrido = document.querySelector('.inicio');
            tempoDecorrido.textContent = segundosParaMinutos(Math.floor(musica.currentTime));
        }

        function segundosParaMinutos(segundos) {
            let campoMinutos = Math.floor(segundos / 60);
            let campoSegundos = segundos % 60;
            if (campoSegundos < 10) {
                campoSegundos = '0' + campoSegundos;
            }

            return campoMinutos + ':' + campoSegundos;
        }

    })
    .catch(error => {
        console.error('Erro:', error);
    });

let musicas = [
    { titulo: 'Boiadeira', artista: 'AnaCastela', src: '.\\static\\musicas\\Boiadeira.mp3', img: '.\\static\\imagens\\Boiadeira.jpg' },
    { titulo: 'Muié, Chapéu e Butina (Ao Vivo)', artista: 'Lubet', src: '.\\static\\musicas\\Muié Chapéu e Butina (Ao Vivo).mp3', img: '.\\static\\imagens\\Muié, Chapéu e Butina (Ao Vivo).jpg' },
    { titulo: 'A Roça Venceu', artista: 'Antny&Gabrel', src: '.\\static\\musicas\\A Roça Venceu.mp3', img: '.\\static\\imagens\\A Roça Venceu.jpg' }
];
let musica = document.querySelector('audio');
let indexMusica = 0;

let duracaoMusica = document.querySelector('.fim');
let imagem = document.querySelector('img');
let nomeMusica = document.querySelector('.descricao h2');
let nomeArtista = document.querySelector('.descricao i');

renderizarMusica(indexMusica);

document.querySelector('i.botao-play').addEventListener('click', tocarMusica);

document.querySelector('i.botao-pause').addEventListener('click', pausarMusica);

musica.addEventListener('timeupdate', atualizarBarra);

document.querySelector('i.anterior').addEventListener('click', () => {
    indexMusica--;
    if (indexMusica < 0) {
        indexMusica = 2;
    }
    renderizarMusica(indexMusica);
});

document.querySelector('.proxima').addEventListener('click', () => {
    indexMusica++;
    if (indexMusica > 2) {
        indexMusica = 0;
    }
    renderizarMusica(indexMusica);
});

function renderizarMusica(index) {
    musica.setAttribute('src', musicas[index].src);
    musica.addEventListener('loadeddata', () => {
        nomeMusica.textContent = musicas[index].titulo;
        nomeArtista.textContent = musicas[index].artista;
        imagem.src = musicas[index].img;
        duracaoMusica.textContent = segundosParaMinutos(Math.floor(musica.duration));
    });
}

function tocarMusica() {
    musica.play();
    document.querySelector('.botao-pause').style.display = 'block';
    document.querySelector('.botao-play').style.display = 'none';
}

function pausarMusica() {
    musica.pause();
    document.querySelector('.botao-pause').style.display = 'none';
    document.querySelector('.botao-play').style.display = 'block';
}

function atualizarBarra() {
    let barra = document.querySelector('progress');
    barra.style.width = Math.floor((musica.currentTime / musica.duration) * 100) + '%';
    let tempoDecorrido = document.querySelector('.inicio');
    tempoDecorrido.textContent = segundosParaMinutos(Math.floor(musica.currentTime));
}

function segundosParaMinutos(segundos) {
    let campoMinutos = Math.floor(segundos / 60);
    let campoSegundos = segundos % 60;
    if (campoSegundos < 10) {
        campoSegundos = '0' + campoSegundos;
    }

    return campoMinutos + ':' + campoSegundos;
}
