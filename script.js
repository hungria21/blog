import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// --- CONFIGURAÇÕES E VARIÁVEIS DO JOGO ---
const GRID_SIZE = 20;
const TICK_RATE = 150; // Velocidade inicial em ms
let gameActive = false;
let score = 0;
let lastTickTime = 0;

// Elementos da UI
const scoreElement = document.getElementById('score');
const finalScoreElement = document.getElementById('final-score');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const overlay = document.getElementById('overlay');
const startButton = document.getElementById('start-button');
const restartButton = document.getElementById('restart-button');

// --- CONFIGURAÇÃO DO THREE.JS ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b0e14); // Fundo escuro

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 15, 12); // Posição angular para ver o tabuleiro
camera.lookAt(0, 0, 0);

const canvas = document.getElementById('game-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;

// Iluminação
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 20, 10);
directionalLight.castShadow = true;
// Configurar sombras de alta qualidade
directionalLight.shadow.mapSize.width = 1024;
directionalLight.shadow.mapSize.height = 1024;
directionalLight.shadow.camera.left = -15;
directionalLight.shadow.camera.right = 15;
directionalLight.shadow.camera.top = 15;
directionalLight.shadow.camera.bottom = -15;
scene.add(directionalLight);

// Plano de Chão (Tabuleiro)
const planeGeometry = new THREE.PlaneGeometry(GRID_SIZE, GRID_SIZE);
const planeMaterial = new THREE.MeshStandardMaterial({
    color: 0x1a1f29,
    roughness: 0.8,
    metalness: 0.2
});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.receiveShadow = true;
scene.add(plane);

// Grade Auxiliar para estilo visual
const gridHelper = new THREE.GridHelper(GRID_SIZE, GRID_SIZE, 0x00ffff, 0x333333);
gridHelper.position.y = 0.01;
scene.add(gridHelper);

// Bordas do Tabuleiro (Neon)
const edgeBox = new THREE.BoxGeometry(GRID_SIZE + 0.5, 0.2, GRID_SIZE + 0.5);
const edgeMaterial = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true });
const edges = new THREE.Mesh(edgeBox, edgeMaterial);
edges.position.y = 0;
scene.add(edges);

// --- LÓGICA DA COBRA ---
let snake = [];
let direction = new THREE.Vector3(1, 0, 0);
let nextDirection = new THREE.Vector3(1, 0, 0);
let headModel = null;

const loader = new GLTFLoader();
loader.load('character.glb', (gltf) => {
    headModel = gltf.scene;
    headModel.scale.set(0.4, 0.4, 0.4);
    headModel.traverse(node => {
        if (node.isMesh) node.castShadow = true;
    });
}, undefined, (error) => console.error('Erro ao carregar modelo:', error));

const snakeSegmentGeometry = new THREE.BoxGeometry(0.9, 0.9, 0.9);
const snakeHeadMaterial = new THREE.MeshStandardMaterial({ color: 0xff00ff, emissive: 0x330033 });
const snakeBodyMaterial = new THREE.MeshStandardMaterial({ color: 0x00ffff, emissive: 0x003333 });

function createSnakeSegment(x, z, isHead = false) {
    let mesh;
    if (isHead && headModel) {
        mesh = headModel.clone();
    } else {
        mesh = new THREE.Mesh(
            snakeSegmentGeometry,
            isHead ? snakeHeadMaterial : snakeBodyMaterial
        );
    }
    mesh.position.set(x, isHead && headModel ? 0 : 0.5, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    scene.add(mesh);
    return { mesh, pos: new THREE.Vector3(x, 0.5, z) };
}

function initSnake() {
    // Limpar cobra anterior se houver
    snake.forEach(segment => scene.remove(segment.mesh));
    snake = [];

    // Criar nova cobra no centro (alinhada ao grid de 0.5)
    const startX = 0.5;
    const startZ = 0.5;

    snake.push(createSnakeSegment(startX, startZ, true));
    snake.push(createSnakeSegment(startX - 1, startZ));
    snake.push(createSnakeSegment(startX - 2, startZ));

    direction.set(1, 0, 0);
    nextDirection.set(1, 0, 0);
}

function moveSnake() {
    direction.copy(nextDirection);

    const head = snake[0];
    const newPos = head.pos.clone().add(direction);

    // Adicionar novo segmento na frente (como nova cabeça)
    const newHead = createSnakeSegment(newPos.x, newPos.z, true);

    // Rotacionar a cabeça para a direção certa
    if (direction.x === 1) newHead.mesh.rotation.y = Math.PI / 2;
    if (direction.x === -1) newHead.mesh.rotation.y = -Math.PI / 2;
    if (direction.z === 1) newHead.mesh.rotation.y = 0;
    if (direction.z === -1) newHead.mesh.rotation.y = Math.PI;

    // Transformar a cabeça antiga em corpo
    if (headModel && head.mesh.type !== 'Mesh') {
        // Se a cabeça antiga era o modelo GLB, precisamos substituí-la por um cubo
        const bodySegment = new THREE.Mesh(snakeSegmentGeometry, snakeBodyMaterial);
        bodySegment.position.copy(head.pos);
        bodySegment.castShadow = true;
        bodySegment.receiveShadow = true;
        scene.remove(head.mesh);
        head.mesh = bodySegment;
        scene.add(bodySegment);
    } else {
        head.mesh.material = snakeBodyMaterial;
    }

    snake.unshift(newHead);

    // Verificar colisão com comida
    if (newPos.x === food.pos.x && newPos.z === food.pos.z) {
        score += 10;
        scoreElement.innerText = score;
        spawnFood();
        // Não remove o rabo, então a cobra cresce
    } else {
        // Remover o rabo
        const tail = snake.pop();
        scene.remove(tail.mesh);
    }
}

// --- LÓGICA DE COMIDA ---
let food = null;
const foodGeometry = new THREE.SphereGeometry(0.4, 16, 16);
const foodMaterial = new THREE.MeshStandardMaterial({
    color: 0xffff00,
    emissive: 0x333300,
    metalness: 0.5,
    roughness: 0.2
});

function spawnFood() {
    if (food) {
        scene.remove(food.mesh);
    }

    let x, z;
    let collision;

    do {
        collision = false;
        x = Math.floor(Math.random() * GRID_SIZE) - GRID_SIZE / 2 + 0.5;
        z = Math.floor(Math.random() * GRID_SIZE) - GRID_SIZE / 2 + 0.5;

        // Evitar spawn na cobra
        for (let segment of snake) {
            if (segment.pos.x === x && segment.pos.z === z) {
                collision = true;
                break;
            }
        }
    } while (collision);

    const mesh = new THREE.Mesh(foodGeometry, foodMaterial);
    mesh.position.set(x, 0.5, z);
    mesh.castShadow = true;
    scene.add(mesh);
    food = { mesh, pos: new THREE.Vector3(x, 0.5, z) };
}

// --- DETECÇÃO DE COLISÃO ---
function checkCollisions() {
    const head = snake[0];

    // Colisão com paredes
    const halfGrid = GRID_SIZE / 2;
    if (head.pos.x < -halfGrid || head.pos.x > halfGrid ||
        head.pos.z < -halfGrid || head.pos.z > halfGrid) {
        return true;
    }

    // Auto-colisão
    for (let i = 1; i < snake.length; i++) {
        if (head.pos.x === snake[i].pos.x && head.pos.z === snake[i].pos.z) {
            return true;
        }
    }

    return false;
}

// --- GERENCIAMENTO DE ESTADO E CONTROLES ---
function startGame() {
    score = 0;
    scoreElement.innerText = score;
    gameActive = true;
    lastTickTime = performance.now();
    overlay.classList.add('hidden');
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');

    initSnake();
    spawnFood();
}

function gameOver() {
    gameActive = false;
    finalScoreElement.innerText = score;
    overlay.classList.remove('hidden');
    gameOverScreen.classList.remove('hidden');
}

function handleInput(key) {
    if (!gameActive) return;

    switch(key) {
        case 'ArrowUp':
            if (direction.z !== 1) nextDirection.set(0, 0, -1);
            break;
        case 'ArrowDown':
            if (direction.z !== -1) nextDirection.set(0, 0, 1);
            break;
        case 'ArrowLeft':
            if (direction.x !== 1) nextDirection.set(-1, 0, 0);
            break;
        case 'ArrowRight':
            if (direction.x !== -1) nextDirection.set(1, 0, 0);
            break;
    }
}

// Event Listeners
window.addEventListener('keydown', (e) => handleInput(e.key));

document.getElementById('btn-up').addEventListener('click', () => handleInput('ArrowUp'));
document.getElementById('btn-down').addEventListener('click', () => handleInput('ArrowDown'));
document.getElementById('btn-left').addEventListener('click', () => handleInput('ArrowLeft'));
document.getElementById('btn-right').addEventListener('click', () => handleInput('ArrowRight'));

startButton.addEventListener('click', startGame);
restartButton.addEventListener('click', startGame);

// Redimensionamento
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Loop de renderização e animação
function animate(time) {
    requestAnimationFrame(animate);

    if (gameActive && time - lastTickTime > TICK_RATE) {
        moveSnake();
        if (checkCollisions()) {
            gameOver();
        }
        lastTickTime = time;
    }

    // Animação leve na comida
    if (food) {
        food.mesh.position.y = 0.5 + Math.sin(time * 0.005) * 0.1;
        food.mesh.rotation.y += 0.02;
    }

    renderer.render(scene, camera);
}

animate(0);
