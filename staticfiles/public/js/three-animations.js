// Three.js Animations untuk Background Muslim Theme

let scene, camera, renderer, particles;
let animationId;

function initThreeJS() {
    // Scene
    scene = new THREE.Scene();
    scene.background = null; // Transparent background
    
    // Camera
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = 5;
    
    // Renderer
    const canvas = document.getElementById('three-canvas');
    if (!canvas) return;
    
    renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Create Islamic Geometric Pattern
    createGeometricPattern();
    
    // Create Floating Particles
    createParticles();
    
    // Handle Resize
    window.addEventListener('resize', onWindowResize);
    
    // Start Animation
    animate();
}

function createGeometricPattern() {
    const geometry = new THREE.RingGeometry(0.5, 1, 32);
    const material = new THREE.MeshBasicMaterial({
        color: 0x16a34a,
        transparent: true,
        opacity: 0.1,
        side: THREE.DoubleSide
    });
    
    // Create multiple rings
    for (let i = 0; i < 5; i++) {
        const ring = new THREE.Mesh(geometry, material.clone());
        ring.position.set(
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 5
        );
        ring.rotation.x = Math.random() * Math.PI;
        ring.rotation.y = Math.random() * Math.PI;
        ring.userData = {
            speed: 0.001 + Math.random() * 0.002,
            rotationSpeed: 0.001 + Math.random() * 0.002
        };
        scene.add(ring);
    }
}

function createParticles() {
    const particleCount = 100;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    const color1 = new THREE.Color(0x16a34a); // Green
    const color2 = new THREE.Color(0x2563eb); // Blue
    
    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        
        // Positions
        positions[i3] = (Math.random() - 0.5) * 20;
        positions[i3 + 1] = (Math.random() - 0.5) * 20;
        positions[i3 + 2] = (Math.random() - 0.5) * 10;
        
        // Colors
        const color = Math.random() > 0.5 ? color1 : color2;
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    const material = new THREE.PointsMaterial({
        size: 0.1,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });
    
    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

function animate() {
    animationId = requestAnimationFrame(animate);
    
    // Rotate rings
    scene.children.forEach(child => {
        if (child.userData.speed) {
            child.rotation.x += child.userData.rotationSpeed;
            child.rotation.y += child.userData.speed;
        }
    });
    
    // Rotate particles
    if (particles) {
        particles.rotation.y += 0.001;
        particles.rotation.x += 0.0005;
    }
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThreeJS);
} else {
    initThreeJS();
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    if (renderer) {
        renderer.dispose();
    }
});

