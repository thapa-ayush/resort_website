/**
 * Diamond Hill Resort — Nature Background Animations
 * Falling leaves + floating particles via HTML5 Canvas
 * Lightweight, performant, GPU-accelerated
 */

(function () {
  'use strict';

  // ── Configuration ──────────────────────────────────
  const CONFIG = {
    leaves: {
      count: 14,            // Number of leaves on screen
      mobileCount: 8,       // Mobile count (increased for visibility)
      minSize: 16,
      maxSize: 30,
      minSpeed: 0.3,
      maxSpeed: 0.9,
      drift: 0.4,           // Horizontal sway amplitude
      rotationSpeed: 0.008,
      opacity: { min: 0.25, max: 0.55 },
    },
    particles: {
      count: 22,
      mobileCount: 10,
      minSize: 1.5,
      maxSize: 4,
      minSpeed: 0.08,
      maxSpeed: 0.25,
      opacity: { min: 0.10, max: 0.28 },
    },
    colors: {
      leaves: [
        { r: 45, g: 107, b: 74 },    // Forest green
        { r: 26, g: 60, b: 42 },     // Deep green
        { r: 80, g: 140, b: 90 },    // Light green
        { r: 160, g: 138, b: 56 },   // Gold-green
        { r: 201, g: 168, b: 76 },   // Gold accent
      ],
      particles: [
        { r: 201, g: 168, b: 76 },   // Gold pollen
        { r: 224, g: 201, b: 127 },  // Light gold
        { r: 180, g: 176, b: 160 },  // Soft stone
      ],
    },
    fps: 30,                 // Cap to 30fps for efficiency
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

  // ── Leaf Shape Drawing ─────────────────────────────
  function drawLeaf(ctx, x, y, size, rotation, color, opacity) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);
    ctx.globalAlpha = opacity;

    // Organic leaf shape using bezier curves
    ctx.beginPath();
    ctx.moveTo(0, -size * 0.5);

    // Right side curve
    ctx.bezierCurveTo(
      size * 0.35, -size * 0.45,
      size * 0.4,  -size * 0.05,
      0,            size * 0.5
    );

    // Left side curve
    ctx.bezierCurveTo(
      -size * 0.4,  -size * 0.05,
      -size * 0.35, -size * 0.45,
      0,            -size * 0.5
    );

    ctx.fillStyle = `rgb(${color.r}, ${color.g}, ${color.b})`;
    ctx.fill();

    // Leaf vein (center line)
    ctx.beginPath();
    ctx.moveTo(0, -size * 0.4);
    ctx.lineTo(0, size * 0.4);
    ctx.strokeStyle = `rgba(${Math.min(255, color.r + 30)}, ${Math.min(255, color.g + 30)}, ${Math.min(255, color.b + 20)}, ${opacity * 0.6})`;
    ctx.lineWidth = 0.6;
    ctx.stroke();

    ctx.restore();
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
      this.y = initial ? rand(-this.canvasH, 0) : rand(-80, -20);
      this.size = rand(cfg.minSize, cfg.maxSize);
      this.speed = rand(cfg.minSpeed, cfg.maxSpeed);
      this.drift = rand(-cfg.drift, cfg.drift);
      this.rotation = rand(0, Math.PI * 2);
      this.rotSpeed = rand(-cfg.rotationSpeed, cfg.rotationSpeed);
      this.sway = rand(0.5, 1.5);
      this.swayOffset = rand(0, Math.PI * 2);
      this.opacity = rand(cfg.opacity.min, cfg.opacity.max);
      this.color = CONFIG.colors.leaves[
        Math.floor(Math.random() * CONFIG.colors.leaves.length)
      ];
      // Blur factor (smaller leaves = more blur = more depth)
      this.blur = this.size < 18 ? 1 : 0;
    }

    update(time) {
      this.y += this.speed;
      this.x += Math.sin(time * 0.001 * this.sway + this.swayOffset) * this.drift;
      this.rotation += this.rotSpeed;

      if (this.y > this.canvasH + 40 || this.x < -60 || this.x > this.canvasW + 60) {
        this.reset();
      }
    }

    draw(ctx, time) {
      drawLeaf(ctx, this.x, this.y, this.size, this.rotation, this.color, this.opacity);
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
      this.y = initial ? rand(0, this.canvasH) : rand(-20, 0);
      this.size = rand(cfg.minSize, cfg.maxSize);
      this.speed = rand(cfg.minSpeed, cfg.maxSpeed);
      this.driftX = rand(-0.15, 0.15);
      this.opacity = rand(cfg.opacity.min, cfg.opacity.max);
      this.twinkleSpeed = rand(0.002, 0.005);
      this.twinkleOffset = rand(0, Math.PI * 2);
      this.color = CONFIG.colors.particles[
        Math.floor(Math.random() * CONFIG.colors.particles.length)
      ];
    }

    update(time) {
      this.y += this.speed;
      this.x += this.driftX;

      if (this.y > this.canvasH + 10) {
        this.reset();
      }
    }

    draw(ctx, time) {
      const twinkle = 0.5 + 0.5 * Math.sin(time * this.twinkleSpeed + this.twinkleOffset);
      const alpha = this.opacity * twinkle;

      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgb(${this.color.r}, ${this.color.g}, ${this.color.b})`;
      ctx.fill();
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
      // Respect prefers-reduced-motion
      if (prefersReducedMotion()) return;

      this.canvas = document.getElementById('natureCanvas');
      if (!this.canvas) return;

      this.ctx = this.canvas.getContext('2d');
      this.resize();
      this.createElements();
      this.bindEvents();
      this.isRunning = true;
      this.animate(0);
    }

    resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.canvas.width = window.innerWidth * dpr;
      this.canvas.height = window.innerHeight * dpr;
      this.canvas.style.width = '100vw';
      this.canvas.style.height = '100vh';
      this.ctx.scale(dpr, dpr);
      this.w = window.innerWidth;
      this.h = window.innerHeight;
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
      // Debounced resize
      let resizeTimer;
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          this.resize();
          this.createElements();
        }, 250);
      }, { passive: true });

      // Track scroll for parallax offset
      window.addEventListener('scroll', () => {
        this.scrollY = window.scrollY;
      }, { passive: true });

      // Pause when tab hidden
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
        this.lastFrame = 0;
        this.animate(0);
      }
    }

    animate(timestamp) {
      if (!this.isRunning) return;

      this.animId = requestAnimationFrame((t) => this.animate(t));

      // Frame rate limiting
      const elapsed = timestamp - this.lastFrame;
      if (elapsed < this.frameInterval) return;
      this.lastFrame = timestamp - (elapsed % this.frameInterval);

      this.ctx.clearRect(0, 0, this.w, this.h);

      // Subtle parallax offset
      const parallaxOffset = this.scrollY * 0.05;

      // Draw particles first (behind leaves)
      this.ctx.save();
      this.ctx.translate(0, parallaxOffset * 0.3);
      for (const p of this.particles) {
        p.update(timestamp);
        p.draw(this.ctx, timestamp);
      }
      this.ctx.restore();

      // Draw leaves
      this.ctx.save();
      this.ctx.translate(0, parallaxOffset * 0.15);
      for (const leaf of this.leaves) {
        leaf.update(timestamp);
        leaf.draw(this.ctx, timestamp);
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
    animation = new NatureAnimation();
    animation.init();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startAnimation);
  } else {
    startAnimation();
  }
})();
