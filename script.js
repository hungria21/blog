import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// 1. Cena e Câmera
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xdddddd); // Fundo cinza claro

const camera = new THREE.PerspectiveCamera(
    75, // Campo de visão (em graus)
    window.innerWidth / window.innerHeight, // Proporção da tela
    0.1, // Plano de corte próximo
    1000 // Plano de corte distante
);
camera.position.set(0, 1.5, 5); // Posição inicial da câmera

// 2. Renderizador
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true; // Habilitar sombras

// 3. Iluminação
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // Luz ambiente suave
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // Luz direcional (sol)
directionalLight.position.set(5, 10, 7.5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// 4. Controles de Órbita
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Suaviza o movimento
controls.target.set(0, 1, 0); // Focar no centro do personagem

// 5. Carregador de Modelo
const loader = new GLTFLoader();
loader.load(
    'character.glb', // Caminho para o modelo 3D
    function (gltf) {
        const model = gltf.scene;
        model.position.set(0, 0, 0);
        model.scale.set(0.5, 0.5, 0.5); // Ajustar a escala do modelo

        // Ativar sombra para todos os objetos do modelo
        model.traverse(function (node) {
            if (node.isMesh) {
                node.castShadow = true;
            }
        });

        scene.add(model);
    },
    undefined, // Função de progresso (opcional)
    function (error) {
        console.error('Ocorreu um erro ao carregar o modelo.', error);
    }
);

// Adicionar um chão simples para receber sombras
const planeGeometry = new THREE.PlaneGeometry(20, 20);
const planeMaterial = new THREE.MeshStandardMaterial({ color: 0xcccccc });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.position.y = 0;
plane.receiveShadow = true;
scene.add(plane);

// 6. Loop de Animação
function animate() {
    requestAnimationFrame(animate);

    controls.update(); // Atualiza os controles de órbita

    renderer.render(scene, camera);
}

// 7. Responsividade da Janela
window.addEventListener('resize', () => {
    // Atualiza o tamanho do renderizador
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // Atualiza a proporção da câmera
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

// Inicia a animação
animate();
