/**
 * Diamond Hill Resort — Nature Background Animations
 * Falling leaves + floating particles via HTML5 Canvas
 * Highly optimized with off-screen rendering
 * Cursor Physics + Parallax Ready
 */

console.log('[Nature Animations] 📜 Script loading...');
console.log('[Nature Animations] Current time:', new Date().toLocaleTimeString());

(function () {
  'use strict';
  
  // ── Configuration ──────────────────────────────────
  const CONFIG = {
    leaves: {
      count: 18,
      mobileCount: 8,
      minSize: 18,
      maxSize: 32,
      minSpeed: 1.0,
      maxSpeed: 1.2,
      drift: 1.0,
      rotationSpeed: 0.02,
      opacity: { min: 0.4, max: 0.8 },
    },
    particles: {
      count: 30,
      mobileCount: 15,
      minSize: 1.5,
      maxSize: 4.5,
      minSpeed: 0.5,
      maxSpeed: 1.8,
      opacity: { min: 0.3, max: 0.7 },
    },
    physics: {
      radius: 120, // Distance within which the cursor repels items
      force: 6, // Base ejection power
      friction: 0.94, // Inertia decay (1 = slippery, 0 = immediate stop)
    },
    colors: {
      leaves: [
        { r: 45, g: 107, b: 74 },
        { r: 26, g: 60, b: 42 },
        { r: 80, g: 140, b: 90 },
        { r: 160, g: 138, b: 56 },
        { r: 201, g: 168, b: 76 },
      ],
      particles: [
        { r: 201, g: 168, b: 76 },
        { r: 224, g: 201, b: 127 },
        { r: 255, g: 255, b: 255 },
      ],
    },
    fps: 60, // Smooth 60fps
    pauseWhenHidden: true,
  };

  // ── Utility ────────────────────────────────────────
  function rand(min, max) {
    return Math.random() * (max - min) + min;
  }

  function isMobile() {
    return window.innerWidth <= 768;
  }

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  // ── Pre-render Leaf Sprites ────────────────────────
  const leafSprites = [];

  function initSprites() {
    const baseSize = 60; // Render at high res
    
    if (leafSprites.length > 0) {
      console.log('[Sprites] Already initialized with', leafSprites.length, 'sprites');
      return; // Already initialized
    }
    
    console.log('[Sprites] 🎨 Starting sprite initialization...');
    console.log('[Sprites] CONFIG.colors.leaves =', CONFIG.colors.leaves);
    
    CONFIG.colors.leaves.forEach((color, idx) => {
      try {
        const canvas = document.createElement('canvas');
        canvas.width = baseSize;
        canvas.height = baseSize;
        const ctx = canvas.getContext('2d');
        if (!ctx) {
          console.warn('[Sprites] Failed to get 2D context for sprite', idx);
          return;
        }
        
        const cx = baseSize / 2;
        const cy = baseSize / 2;
        const size = baseSize * 0.8; // Leave margin
        
        ctx.translate(cx, cy);
        
        ctx.beginPath();
        ctx.moveTo(0, -size * 0.5);
        ctx.bezierCurveTo(
          size * 0.35, -size * 0.45,
          size * 0.4,  -size * 0.05,
          0,            size * 0.5
        );
        ctx.bezierCurveTo(
          -size * 0.4,  -size * 0.05,
          -size * 0.35, -size * 0.45,
          0,            -size * 0.5
        );
        ctx.fillStyle = `rgb(${color.r}, ${color.g}, ${color.b})`;
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(0, -size * 0.4);
        ctx.lineTo(0, size * 0.4);
        ctx.strokeStyle = `rgba(${Math.min(255, color.r + 30)}, ${Math.min(255, color.g + 30)}, ${Math.min(255, color.b + 20)}, 0.8)`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
        
        leafSprites.push(canvas);
        console.log('[Sprites] ✓ Sprite', idx, 'created:', canvas);
      } catch (e) {
        console.error('[Sprites] ❌ Error creating sprite', idx, ':', e);
      }
    });
    
    console.log(`[Sprites] ✅ Sprites initialized: ${leafSprites.length} leaf sprites created`);
    if (leafSprites.length === 0) {
      console.error('[Sprites] 🔴 CRITICAL: No leaf sprites were created! CONFIG.colors.leaves.length =', CONFIG.colors.leaves.length);
    }
  }

  // ── Particle Classes ───────────────────────────────
  class Leaf {
    constructor(canvasW, canvasH) {
      this.canvasW = canvasW;
      this.canvasH = canvasH;
      this.reset(true);
    }

    reset(initial = false) {
      const cfg = CONFIG.leaves;
      this.x = rand(-50, this.canvasW + 50);
      this.y = initial ? rand(-50, this.canvasH) : rand(-150, -50);
      this.vx = 0; // Kinetic velocity X
      this.vy = 0; // Kinetic velocity Y
      this.size = rand(cfg.minSize, cfg.maxSize);
      this.speed = rand(cfg.minSpeed, cfg.maxSpeed);
      this.drift = rand(-cfg.drift, cfg.drift);
      this.rotation = rand(0, Math.PI * 2);
      this.rotSpeed = rand(-cfg.rotationSpeed, cfg.rotationSpeed);
      this.sway = rand(0.5, 1.5);
      this.swayOffset = rand(0, Math.PI * 2);
      this.opacity = rand(cfg.opacity.min, cfg.opacity.max);
      
      // Assign sprite with error checking
      if (leafSprites.length > 0) {
        this.sprite = leafSprites[Math.floor(Math.random() * leafSprites.length)];
      } else {
        console.error('[Leaf] No sprites available! leafSprites array is empty.');
        this.sprite = null;
      }
    }

    update(time, frameDelta, mouse, parallaxOffset) {
      const timeScale = Math.min(frameDelta / 16.66, 3);
      
      // Calculate true visual position on screen given parallax rendering offset
      const exactScreenY = this.y + parallaxOffset;
      
      // Mouse Interaction Physics
      if (mouse.x > 0 && mouse.y > 0) {
        const dx = this.x - mouse.x;
        const dy = exactScreenY - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < CONFIG.physics.radius) {
          // Add reactive push force based on mouse coordinates closing in
          const push = (CONFIG.physics.radius - dist) / CONFIG.physics.radius; // Scale 0 to 1
          this.vx += (dx / dist) * push * CONFIG.physics.force;
          this.vy += (dy / dist) * push * CONFIG.physics.force;
        }
      }

      // Apply frictional decay to momentum
      this.vx *= CONFIG.physics.friction;
      this.vy *= CONFIG.physics.friction;

      // Base translation + Physics momentum
      this.y += (this.speed * timeScale) + (this.vy * timeScale);
      this.x += (Math.sin(time * 0.002 * this.sway + this.swayOffset) * this.drift * timeScale) + (this.vx * timeScale);
      
      // Induce dramatic spin when blown aggressively
      const extraSpin = (this.vx * 0.05) + (this.vy * 0.02);
      this.rotation += (this.rotSpeed * timeScale) + extraSpin;

      // Wrap Bounds
      if (this.y > this.canvasH + 50 || this.x < -100 || this.x > this.canvasW + 100) {
        this.reset();
      }
    }

    draw(ctx) {
      if (!this.sprite) {
        // Fallback: draw simple circle if sprite is missing
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = 'rgba(45, 107, 74, 0.6)';
        ctx.beginPath();
        ctx.arc(0, 0, this.size / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
        return;
      }
      
      // Draw sprite
      try {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.opacity;
        ctx.drawImage(this.sprite, -this.size / 2, -this.size / 2, this.size, this.size);
        ctx.restore();
      } catch (e) {
        console.error('[Leaf.draw] Error drawing sprite:', e);
        // Fall back to circle on error
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = 'rgba(45, 107, 74, 0.6)';
        ctx.beginPath();
        ctx.arc(0, 0, this.size / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }
  }

  class Particle {
    constructor(canvasW, canvasH) {
      this.canvasW = canvasW;
      this.canvasH = canvasH;
      this.reset(true);
    }

    reset(initial = false) {
      const cfg = CONFIG.particles;
      this.x = rand(0, this.canvasW);
      this.y = initial ? rand(0, this.canvasH) : rand(-20, -5);
      this.vx = 0;
      this.vy = 0;
      this.size = rand(cfg.minSize, cfg.maxSize);
      this.speed = rand(cfg.minSpeed, cfg.maxSpeed);
      this.driftX = rand(-0.3, 0.3);
      this.opacity = rand(cfg.opacity.min, cfg.opacity.max);
      this.twinkleSpeed = rand(0.002, 0.005);
      this.twinkleOffset = rand(0, Math.PI * 2);
      this.color = CONFIG.colors.particles[Math.floor(Math.random() * CONFIG.colors.particles.length)];
    }

    update(time, frameDelta, mouse, parallaxOffset) {
      const timeScale = Math.min(frameDelta / 16.66, 3);
      
      const exactScreenY = this.y + parallaxOffset;
      if (mouse.x > 0 && mouse.y > 0) {
        const dx = this.x - mouse.x;
        const dy = exactScreenY - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < CONFIG.physics.radius * 0.8) {
          const push = (CONFIG.physics.radius * 0.8 - dist) / (CONFIG.physics.radius * 0.8);
          this.vx += (dx / dist) * push * (CONFIG.physics.force * 0.6);
          this.vy += (dy / dist) * push * (CONFIG.physics.force * 0.6);
        }
      }

      this.vx *= CONFIG.physics.friction;
      this.vy *= CONFIG.physics.friction;

      this.y += (this.speed * timeScale) + this.vy;
      this.x += (this.driftX * timeScale) + this.vx;

      if (this.y > this.canvasH + 20 || this.x < -30 || this.x > this.canvasW + 30) {
        this.reset();
      }
    }

    draw(ctx, time) {
      const twinkle = 0.5 + 0.5 * Math.sin(time * this.twinkleSpeed + this.twinkleOffset);
      const alpha = this.opacity * twinkle;

      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      // Optimization: use rect for very small particles to avoid arc math
      if (this.size < 2.5) {
        ctx.fillStyle = `rgb(${this.color.r}, ${this.color.g}, ${this.color.b})`;
        ctx.fillRect(this.x - this.size/2, this.y - this.size/2, this.size, this.size);
      } else {
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgb(${this.color.r}, ${this.color.g}, ${this.color.b})`;
        ctx.fill();
      }
      ctx.restore();
    }
  }

  // ── Main Animation Controller ──────────────────────
  class NatureAnimation {
    constructor() {
      this.canvas = null;
      this.ctx = null;
      this.leaves = [];
      this.particles = [];
      this.animId = null;
      this.lastFrame = 0;
      this.frameInterval = 1000 / CONFIG.fps;
      this.isRunning = false;
      this.scrollY = 0;
      this.mouse = { x: -1000, y: -1000 };
    }

    init() {
      console.log('[Init] 📍 init() called');

      // Disabled: Allow animation even with reduced motion pref for now (testing)
      // if (prefersReducedMotion()) {
      //   console.log('[Init] ⚠️  Reduced motion preference detected - aborting');
      //   return;
      // }

      this.canvas = document.getElementById('natureCanvas');
      console.log('[Init] Canvas lookup result:', this.canvas ? '✓ Found' : '✗ Not found');
      
      if (!this.canvas) {
        console.error('[Init] ❌ CRITICAL: Canvas #natureCanvas NOT FOUND in DOM!');
        return;
      }
      
      console.log('[Init] ✓ Canvas found:', this.canvas);

      this.ctx = this.canvas.getContext('2d', { alpha: true });
      if (!this.ctx) {
        console.error('[Init] ❌ Failed to get canvas 2D context!');
        return;
      }
      
      console.log('[Init] ✓ 2D context obtained');

      try {
        console.log('[Init] 🎨 Initializing sprites...');
        initSprites();
        console.log('[Init] 🎨 Resizing canvas...');
        this.resize();
        console.log('[Init] 🎨 Creating elements...');
        this.createElements();
        console.log('[Init] 🎨 Binding events...');
        this.bindEvents();
        
        // Start animation
        this.isRunning = true;
        this.lastFrame = window.performance ? performance.now() : Date.now();
        console.log('[Init] ▶️ Starting animation loop');
        this.animate(this.lastFrame);
        
        console.log('[Init] ✅ FULLY INITIALIZED - Canvas:', this.canvas.width, 'x', this.canvas.height, 'Leaves:', this.leaves.length);
      } catch (e) {
        console.error('[Init] ❌ Error during initialization:', e);
        console.error('[Init] Stack:', e.stack);
        throw e;
      }
    }

    resize() {
      const dpr = window.devicePixelRatio || 1;
      this.w = window.innerWidth;
      this.h = window.innerHeight;
      
      console.log('[Resize] Setting canvas to ' + this.w + ' x ' + this.h);
      
      // Set canvas to CSS pixels (not device pixels)
      this.canvas.width = this.w;
      this.canvas.height = this.h;
      
      console.log('[Resize] Canvas actual size:', this.canvas.width, 'x', this.canvas.height);
      console.log('[Resize] ✓ Canvas ready');
      
      // Draw test green square to verify canvas works
      this.ctx.fillStyle = '#00FF00';
      this.ctx.fillRect(10, 10, 100, 100);
      this.ctx.fillStyle = '#FFFFFF';
      this.ctx.font = '16px Arial';
      this.ctx.fillText('Canvas Ready', 10, 135);
    }

    createElements() {
      const mobile = isMobile();
      const leafCount = mobile ? CONFIG.leaves.mobileCount : CONFIG.leaves.count;
      const particleCount = mobile ? CONFIG.particles.mobileCount : CONFIG.particles.count;

      this.leaves = [];
      this.particles = [];

      console.log('[Elements] 🍃 Creating elements...');
      console.log('[Elements] Mobile?', mobile, '| Leaf count:', leafCount, '| Particle count:', particleCount);
      console.log('[Elements] leafSprites available?', leafSprites.length);
      
      for (let i = 0; i < leafCount; i++) {
        try {
          const leaf = new Leaf(this.w, this.h);
          this.leaves.push(leaf);
          if (i === 0) console.log('[Elements] First leaf created:', leaf, '| Has sprite?', !!leaf.sprite);
        } catch (e) {
          console.error('[Elements] Error creating leaf', i, ':', e);
        }
      }
      console.log('[Elements] ✓ Created ' + this.leaves.length + ' leaves');
      
      for (let i = 0; i < particleCount; i++) {
        try {
          this.particles.push(new Particle(this.w, this.h));
        } catch (e) {
          console.error('[Elements] Error creating particle', i, ':', e);
        }
      }
      console.log('[Elements] ✓ Created ' + this.particles.length + ' particles');
      
      if (this.leaves.length === 0) {
        console.error('[Elements] 🔴 ERROR: No leaves were created!');
      }
      if (this.leaves.length > 0 && !this.leaves[0].sprite) {
        console.error('[Elements] 🔴 ERROR: Leaves have no sprites! leafSprites.length =', leafSprites.length);
      }
    }

    bindEvents() {
      let resizeTimer;
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          this.resize();
          this.createElements();
        }, 300);
      }, { passive: true });

      window.addEventListener('scroll', () => {
        this.scrollY = window.scrollY;
      }, { passive: true });
      
      // Cursor Physics Tethers
      window.addEventListener('mousemove', (e) => {
        this.mouse.x = e.clientX;
        this.mouse.y = e.clientY;
      }, { passive: true });

      window.addEventListener('mouseleave', () => {
        // Sweep cursor array off-screen smoothly so logic doesn't hover indefinitely
        this.mouse.x = -1000;
        this.mouse.y = -1000;
      });

      if (CONFIG.pauseWhenHidden) {
        document.addEventListener('visibilitychange', () => {
          if (document.hidden) {
            this.pause();
          } else {
            this.resume();
          }
        });
      }
    }

    pause() {
      this.isRunning = false;
      if (this.animId) {
        cancelAnimationFrame(this.animId);
        this.animId = null;
      }
    }

    resume() {
      if (!this.isRunning) {
        this.isRunning = true;
        this.lastFrame = window.performance ? performance.now() : Date.now();
        this.animate(this.lastFrame);
      }
    }

    animate(timestamp) {
      if (!this.isRunning) return;

      this.animId = requestAnimationFrame((t) => this.animate(t));

      const elapsed = timestamp - this.lastFrame;
      if (elapsed < this.frameInterval) return;
      
      const frameDelta = Math.min(elapsed, 100); 
      this.lastFrame = timestamp - (elapsed % this.frameInterval);

      // Clear canvas simply
      this.ctx.clearRect(0, 0, this.w, this.h);

      const parallaxOffset = this.scrollY * 0.05;

      // Draw particles
      const pOffsetRender = parallaxOffset * 0.2;
      this.ctx.save();
      this.ctx.translate(0, pOffsetRender);
      for (const p of this.particles) {
        p.update(timestamp, frameDelta, this.mouse, pOffsetRender);
        p.draw(this.ctx, timestamp);
      }
      this.ctx.restore();

      // Draw leaves
      const lOffsetRender = parallaxOffset * 0.4;
      this.ctx.save();
      this.ctx.translate(0, lOffsetRender);
      
      console.log('[Animate] Drawing ' + this.leaves.length + ' leaves');
      
      for (let i = 0; i < this.leaves.length; i++) {
        const leaf = this.leaves[i];
        leaf.update(timestamp, frameDelta, this.mouse, lOffsetRender);
        try {
          leaf.draw(this.ctx);
        } catch (e) {
          console.error('[Animate] Error drawing leaf', i, ':', e);
        }
      }
      this.ctx.restore();
    }
    
    destroy() {
      this.pause();
      this.leaves = [];
      this.particles = [];
      this.mouse = null;
    }
  }

  // ── Bootstrap ──────────────────────────────────────
  let animation;

  function startAnimation() {
    console.log('[Nature Animations] 🚀 startAnimation() called');
    
    // Check if canvas exists in DOM RIGHT NOW
    const canvas = document.getElementById('natureCanvas');
    console.log('[Nature Animations] Canvas found in DOM?', canvas ? '✓ YES' : '✗ NO');
    if (canvas) {
      console.log('[Nature Animations] Canvas element:', canvas);
      console.log('[Nature Animations] Canvas visible?', {
        display: canvas.style.display,
        width: canvas.width,
        height: canvas.height,
        clientWidth: canvas.clientWidth,
        clientHeight: canvas.clientHeight,
        offsetParent: canvas.offsetParent ? 'visible' : 'hidden',
        computedDisplay: window.getComputedStyle(canvas).display
      });
    }
    
    animation = new NatureAnimation();
    animation.init();
  }

  if (document.readyState === 'loading') {
    console.log('[Nature Animations] ⏳ Waiting for DOM to load...');
    document.addEventListener('DOMContentLoaded', startAnimation);
  } else {
    console.log('[Nature Animations] ✓ DOM already loaded, starting now');
    startAnimation();
  }
})();
