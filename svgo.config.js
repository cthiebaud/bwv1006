// svgo.config.js - Conservative optimization for LilyPond-generated SVGs
module.exports = {
  plugins: [
    // Safe optimizations that won't break music notation
    'removeDoctype',
    'removeComments',
    'removeMetadata',
    'cleanupAttrs',
    'removeEmptyAttrs',
    'removeEmptyContainers',
    'cleanupNumericValues',
    'collapseGroups',
    'removeUselessStrokeAndFill',
    
    // AVOID these plugins that could break your score:
    // 'cleanupIds',           // Don't touch IDs - your JS needs them
    // 'removeUnusedNS',       // Keep all namespaces
    // 'mergeStyles',          // Don't merge CSS classes
    // 'inlineStyles',         // Keep styles separate
    // 'removeDimensions',     // Keep width/height for proper scaling  
    // 'removeViewBox',        // Essential for responsive behavior
    // 'convertPathData',      // Might affect precise note positioning
    // 'removeUnknownAttrs',   // This would remove data-* attributes!
  ]
};