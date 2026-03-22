/**
 * Diamond Hill Resort — Nature Background Animations
 * Falling leaves + floating particles via HTML5 Canvas
 * Highly optimized with off-screen rendering
 */

console.log('[Nature Animations] Script loading...');

(function () {
  'use strict';
  
  // ── Configuration ──────────────────────────────────
  const CONFIG = {
    leaves: {
      count: 18,
      mobileCount: 8,
      minSize: 18,
      maxSize: 32,
      minSpeed: 1.5,
      maxSpeed: 3.5,
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
    
    CONFIG.colors.leaves.forEach(color => {
      const canvas = document.createElement('canvas');
      canvas.width = baseSize;
      canvas.height = baseSize;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
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
    });
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
      // Spawn somewhat evenly across screen initially so they are immediately visible
      this.y = initial ? rand(-50, this.canvasH) : rand(-150, -50);
      this.size = rand(cfg.minSize, cfg.maxSize);
      this.speed = rand(cfg.minSpeed, cfg.maxSpeed);
      this.drift = rand(-cfg.drift, cfg.drift);
      this.rotation = rand(0, Math.PI * 2);
      this.rotSpeed = rand(-cfg.rotationSpeed, cfg.rotationSpeed);
      this.sway = rand(0.5, 1.5);
      this.swayOffset = rand(0, Math.PI * 2);
      this.opacity = rand(cfg.opacity.min, cfg.opacity.max);
      this.sprite = leafSprites[Math.floor(Math.random() * leafSprites.length)];
    }

    update(time, frameDelta) {
      // Normalize speed based on 60fps (16.66ms per frame)
      const timeScale = Math.min(frameDelta / 16.66, 3);
      
      this.y += this.speed * timeScale;
      this.x += Math.sin(time * 0.002 * this.sway + this.swayOffset) * this.drift * timeScale;
      this.rotation += this.rotSpeed * timeScale;

      if (this.y > this.canvasH + 50 || this.x < -100 || this.x > this.canvasW + 100) {
        this.reset();
      }
    }

    draw(ctx) {
      if (!this.sprite) return;
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      ctx.globalAlpha = this.opacity;
      // draw bounds centered
      ctx.drawImage(this.sprite, -this.size / 2, -this.size / 2, this.size, this.size);
      ctx.restore();
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
      this.size = rand(cfg.minSize, cfg.maxSize);
      this.speed = rand(cfg.minSpeed, cfg.maxSpeed);
      this.driftX = rand(-0.3, 0.3);
      this.opacity = rand(cfg.opacity.min, cfg.opacity.max);
      this.twinkleSpeed = rand(0.002, 0.005);
      this.twinkleOffset = rand(0, Math.PI * 2);
      this.color = CONFIG.colors.particles[Math.floor(Math.random() * CONFIG.colors.particles.length)];
    }

    update(time, frameDelta) {
      const timeScale = Math.min(frameDelta / 16.66, 3);
      this.y += this.speed * timeScale;
      this.x += this.driftX * timeScale;

      if (this.y > this.canvasH + 20) {
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
    }

    init() {
      console.log('[Nature Animations] init() called');

      if (prefersReducedMotion()) {
        console.log('[Nature Animations] Reduced motion preference detected - aborting');
        return;
      }

      this.canvas = document.getElementById('natureCanvas');
      if (!this.canvas) {
        console.warn('[Nature Animations] Canvas #natureCanvas not found!');
        return;
      }

      this.ctx = this.canvas.getContext('2d', { alpha: true });
      if (!this.ctx) {
        console.error('[Nature Animations] Failed to get canvas 2D context!');
        return;
      }

      try {
        initSprites();
        this.resize();
        this.createElements();
        this.bindEvents();
        this.isRunning = true;
        this.lastFrame = window.performance ? performance.now() : Date.now();
        this.animate(this.lastFrame);
        console.log('[Nature Animations] initialized successfully.');
      } catch (e) {
        console.error('[Nature Animations] Init error:', e);
      }
    }

    resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.w = window.innerWidth;
      this.h = window.innerHeight;
      this.canvas.width = this.w * dpr;
      this.canvas.height = this.h * dpr;
      
      // Setting CSS width/height to 100vw/vh might create scrolling bars if not careful, 
      // but inline styling usually overrides this. Using 100% prevents layout scrollbugs 
      // across major browsers and devices.
      this.canvas.style.width = '100%';
      this.canvas.style.height = '100%';
      
      this.ctx.scale(dpr, dpr);
    }

    createElements() {
      const mobile = isMobile();
      const leafCount = mobile ? CONFIG.leaves.mobileCount : CONFIG.leaves.count;
      const particleCount = mobile ? CONFIG.particles.mobileCount : CONFIG.particles.count;

      this.leaves = [];
      this.particles = [];

      for (let i = 0; i < leafCount; i++) {
        this.leaves.push(new Leaf(this.w, this.h));
      }
      for (let i = 0; i < particleCount; i++) {
        this.particles.push(new Particle(this.w, this.h));
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
      
      // Calculate properly independent of framerate drops
      const frameDelta = Math.min(elapsed, 100); 
      this.lastFrame = timestamp - (elapsed % this.frameInterval);

      // Clear the screen for next paints
      this.ctx.clearRect(0, 0, this.w, this.h);

      const parallaxOffset = this.scrollY * 0.05;

      // Soft parallax for particles behind
      this.ctx.save();
      this.ctx.translate(0, parallaxOffset * 0.2);
      for (const p of this.particles) {
        p.update(timestamp, frameDelta);
        p.draw(this.ctx, timestamp);
      }
      this.ctx.restore();

      // Stronger parallax for leaves in front
      this.ctx.save();
      this.ctx.translate(0, parallaxOffset * 0.4);
      for (const leaf of this.leaves) {
        leaf.update(timestamp, frameDelta);
        leaf.draw(this.ctx);
      }
      this.ctx.restore();
    }
    
    destroy() {
      this.pause();
      this.leaves = [];
      this.particles = [];
    }
  }

  // ── Bootstrap ──────────────────────────────────────
  let animation;

  function startAnimation() {
    console.log('[Nature Animations] startAnimation() called');
    animation = new NatureAnimation();
    animation.init();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startAnimation);
  } else {
    startAnimation();
  }
})();
