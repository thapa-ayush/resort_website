/**
 * ULTRA MINIMAL TEST - Verify Canvas Works
 */
console.log('[TEST] Canvas test script loading...');

(function() {
  'use strict';
  
  function testCanvas() {
    console.log('[TEST] testCanvas() called');
    
    const canvas = document.getElementById('natureCanvas');
    if (!canvas) {
      console.error('[TEST] ❌ Canvas NOT found!');
      return;
    }
    
    console.log('[TEST] ✓ Canvas found:', canvas);
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('[TEST] ❌ Context NOT obtained!');
      return;
    }
    
    console.log('[TEST] ✓ Context obtained');
    
    // Set canvas size to window size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    console.log('[TEST] Canvas dimensions:', canvas.width, 'x', canvas.height);
    
    // Fill entire canvas with bright red
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    console.log('[TEST] ✓ Filled canvas with RED');
    
    // Draw green square
    ctx.fillStyle = '#00FF00';
    ctx.fillRect(20, 20, 200, 200);
    console.log('[TEST] ✓ Drew GREEN SQUARE at (20,20)');
    
    // Draw blue circle
    ctx.fillStyle = '#0000FF';
    ctx.beginPath();
    ctx.arc(window.innerWidth / 2, window.innerHeight / 2, 100, 0, Math.PI * 2);
    ctx.fill();
    console.log('[TEST] ✓ Drew BLUE CIRCLE in center');
    
    // Draw text
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 24px Arial';
    ctx.fillText('CANVAS WORKING!', 50, 300);
    console.log('[TEST] ✓ Drew TEXT');
    
    console.log('[TEST] ✅ ALL TESTS PASSED - Canvas is functioning!');
  }
  
  if (document.readyState === 'loading') {
    console.log('[TEST] Waiting for DOMContentLoaded...');
    document.addEventListener('DOMContentLoaded', testCanvas);
  } else {
    console.log('[TEST] DOM already loaded, running test...');
    testCanvas();
  }
})();
